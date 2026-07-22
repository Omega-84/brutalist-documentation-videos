#!/usr/bin/env python3
"""
capture_sim.py — Playwright headless Chromium recorder for D3 HTML simulations.

Loads a sim <slug>.html, waits for first paint, then records:
  <output_dir>/media/output.mp4  — BASELINE hold (defaults, no interaction)
  <output_dir>/media/change.mp4  — animated sweep of the card's "change" control

Serves the file via a local HTTP server so CDN requests (D3 v7) are not blocked
by Chromium's cross-origin restrictions on file:// URLs.

Usage:
  python3 capture_sim.py <sim_html_path> <reel_dir>
    [--duration SECS]      baseline hold in seconds (default: 6)
    [--change-dur SECS]    change animation in seconds (default: 8)
    [--fps INT]            output fps (default: 24)
    [--width INT]          viewport width (default: 1280)
    [--height INT]         viewport height (default: 720)
    [--selector CSS]       CSS selector of the control to drive (default: first input[type=range])
    [--smoke-test]         write smoke-test marker file and exit 0 on success

Exit 0 on success, 1 on failure.
"""

import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"


# ── local HTTP server ────────────────────────────────────────────────────────

def find_free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_server(directory: Path):
    """Start a SimpleHTTPRequestHandler in a daemon thread. Returns (server, port)."""
    port = find_free_port()

    class QuietHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)
        def log_message(self, *_):
            pass  # suppress access logs

    server = HTTPServer(("127.0.0.1", port), QuietHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server, port


# ── ffmpeg conversion ─────────────────────────────────────────────────────────

def webm_to_mp4(src: Path, dst: Path, fps: int):
    """Convert a .webm Playwright recording to a well-muxed .mp4."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        FFMPEG, "-y", "-i", str(src),
        "-vf", f"fps={fps},scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",  # no audio in screen recordings
        str(dst),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed:\n{r.stderr[-800:]}")
    size = dst.stat().st_size
    if size < 4096:
        raise RuntimeError(f"output mp4 suspiciously small: {size} bytes")
    return size


# ── Playwright capture ────────────────────────────────────────────────────────

def capture(sim_html: Path, reel_dir: Path, *,
            duration: float, change_dur: float,
            fps: int, width: int, height: int,
            selector: str | None,
            smoke_test: bool):
    """Main capture: records output.mp4 and change.mp4 into reel_dir/media/."""
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        sys.exit("[capture_sim] playwright not installed — pip install playwright")

    serve_dir = sim_html.parent
    server, port = start_server(serve_dir)
    url = f"http://127.0.0.1:{port}/{sim_html.name}"
    media_dir = reel_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    tmp_dir = Path(tempfile.mkdtemp(prefix="capture_sim_"))
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage",
                      "--autoplay-policy=no-user-gesture-required"],
            )

            # ── BASELINE (output.mp4) ────────────────────────────────────────
            print(f"[capture_sim] recording baseline: {url}", flush=True)
            ctx_out = browser.new_context(
                viewport={"width": width, "height": height},
                record_video_dir=str(tmp_dir / "out"),
                record_video_size={"width": width, "height": height},
            )
            (tmp_dir / "out").mkdir(parents=True, exist_ok=True)
            page_out = ctx_out.new_page()
            page_out.goto(url, wait_until="networkidle", timeout=30_000)
            # Extra settle time — D3 animations may still be running
            time.sleep(1.5)
            # Hold for the full baseline duration
            time.sleep(duration)
            page_out.close()
            ctx_out.close()

            # Find the webm file that Playwright wrote
            webm_files = list((tmp_dir / "out").glob("*.webm"))
            if not webm_files:
                raise RuntimeError("Playwright produced no .webm for baseline")
            out_webm = webm_files[0]
            out_mp4 = media_dir / "output.mp4"
            size = webm_to_mp4(out_webm, out_mp4, fps)
            print(f"[capture_sim] output.mp4 written ({size//1024} KB)", flush=True)

            # ── CHANGE (change.mp4) ──────────────────────────────────────────
            print(f"[capture_sim] recording change animation", flush=True)
            ctx_chg = browser.new_context(
                viewport={"width": width, "height": height},
                record_video_dir=str(tmp_dir / "chg"),
                record_video_size={"width": width, "height": height},
            )
            (tmp_dir / "chg").mkdir(parents=True, exist_ok=True)
            page_chg = ctx_chg.new_page()
            page_chg.goto(url, wait_until="networkidle", timeout=30_000)
            time.sleep(1.5)  # let D3 settle

            # Determine the control to animate
            ctrl_sel = selector or "input[type=range]"
            try:
                ctrl = page_chg.locator(ctrl_sel).first
                ctrl.wait_for(timeout=5_000)

                # Read min/max/step
                attrs = page_chg.evaluate("""sel => {
                    const el = document.querySelector(sel);
                    if (!el) return null;
                    return {
                        min: parseFloat(el.min || 0),
                        max: parseFloat(el.max || 100),
                        step: parseFloat(el.step || 1)
                    };
                }""", ctrl_sel)

                if attrs:
                    mn, mx = attrs["min"], attrs["max"]
                    steps = 40  # number of animation steps
                    delay = change_dur / steps

                    # Sweep from min to max
                    for i in range(steps + 1):
                        val = mn + (mx - mn) * i / steps
                        page_chg.evaluate("""([sel, v]) => {
                            const el = document.querySelector(sel);
                            if (!el) return;
                            el.value = v;
                            el.dispatchEvent(new Event('input', {bubbles: true}));
                            el.dispatchEvent(new Event('change', {bubbles: true}));
                        }""", [ctrl_sel, val])
                        time.sleep(delay)

                    # Hold at max for a beat
                    time.sleep(1.0)
                else:
                    # No range input found — just hold and try clicking any button
                    btns = page_chg.locator("button").all()
                    if btns:
                        btns[0].click()
                        time.sleep(change_dur)
                    else:
                        time.sleep(change_dur)

            except PWTimeout:
                print(f"[capture_sim] control '{ctrl_sel}' not found — holding {change_dur}s", flush=True)
                time.sleep(change_dur)

            page_chg.close()
            ctx_chg.close()

            webm_files_chg = list((tmp_dir / "chg").glob("*.webm"))
            if not webm_files_chg:
                raise RuntimeError("Playwright produced no .webm for change")
            chg_mp4 = media_dir / "change.mp4"
            size2 = webm_to_mp4(webm_files_chg[0], chg_mp4, fps)
            print(f"[capture_sim] change.mp4 written ({size2//1024} KB)", flush=True)

            browser.close()

    finally:
        server.shutdown()
        shutil.rmtree(tmp_dir, ignore_errors=True)

    if smoke_test:
        marker = reel_dir / "media" / "smoke_test_passed.txt"
        marker.write_text(f"capture_sim smoke test passed\noutput.mp4: {out_mp4}\nchange.mp4: {chg_mp4}\n")
        print(f"[capture_sim] SMOKE TEST PASSED — marker written", flush=True)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sim_html", help="path to the sim .html file")
    ap.add_argument("reel_dir", help="reel directory (media/ will be created inside it)")
    ap.add_argument("--duration",    type=float, default=6.0, help="baseline hold seconds")
    ap.add_argument("--change-dur",  type=float, default=8.0, help="change animation seconds")
    ap.add_argument("--fps",         type=int,   default=24,  help="output fps")
    ap.add_argument("--width",       type=int,   default=1280)
    ap.add_argument("--height",      type=int,   default=720)
    ap.add_argument("--selector",    default=None, help="CSS selector of the control to drive")
    ap.add_argument("--smoke-test",  action="store_true")
    args = ap.parse_args()

    sim_html = Path(args.sim_html).resolve()
    reel_dir = Path(args.reel_dir).resolve()

    if not sim_html.exists():
        sys.exit(f"[capture_sim] ERROR: sim not found: {sim_html}")

    print(f"[capture_sim] sim={sim_html.name}  reel={reel_dir}", flush=True)
    try:
        capture(
            sim_html, reel_dir,
            duration=args.duration,
            change_dur=args.change_dur,
            fps=args.fps,
            width=args.width,
            height=args.height,
            selector=args.selector,
            smoke_test=args.smoke_test,
        )
    except Exception as e:
        print(f"[capture_sim] FAILED: {e}", file=sys.stderr, flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
