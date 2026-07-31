import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import { SAFE, safeX, safeY } from '../tokens/layout';

/**
 * OptBlockerCard — the candor register of the OPT recaps.
 *
 * A blocker gets its own visual treatment so honesty reads as a deliberate
 * editorial choice rather than something buried in narration: a heavier ground
 * than the week markers, a rule across the top, the two dates that bound it, a
 * span bar that fills as the days count up, whose court the ball was in, and
 * how it resolved.
 *
 * Pass `closed: ""` for a blocker still open at the video's end; the closing
 * date is then omitted, the bar stops short of the right edge, and the day
 * count reads "— and counting".
 */

export const optBlockerCardSchema = z.object({
  label: z.string().default('Repo access'),
  opened: z.string().default('Requested May 7'),
  closed: z.string().default('Resolved May 14'),
  days: z.number().default(7),
  resolution: z.string().default('The invite was sent May 11. It was unread.'),
  court: z.string().default("Varun's inbox"),
  folderLabel: z.string().default('@HumanitariansAI'),
});
export type OptBlockerCardProps = z.infer<typeof optBlockerCardSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const OptBlockerCard: React.FC<OptBlockerCardProps> = ({
  label, opened, closed, days, resolution, court, folderLabel,
}) => {
  const frame = useCurrentFrame();
  const inAt = (start: number) => clamp(interpolate(frame, [start, start + 14], [0, 1]), 0, 1);
  const fill = inAt(22);
  const open = closed.trim() === '';

  return (
    <AbsoluteFill style={{ background: CLAUDE.FOOTER }}>
      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(0),
        width: SAFE.w, height: SAFE.h,
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
      }}>
        {/* the heavy rule + label that mark this register */}
        <div>
          <div style={{
            height: 14, width: SAFE.w, background: CLAUDE.INK,
            transform: `scaleX(${inAt(0)})`, transformOrigin: 'left center',
          }} />
          <div style={{
            marginTop: 34, fontFamily: SANS, fontSize: 28, letterSpacing: '0.2em',
            color: CLAUDE.INK_SOFT, opacity: inAt(2),
          }}>
            BLOCKER
          </div>
          <div style={{
            marginTop: 12, maxWidth: SAFE.w, fontFamily: SERIF, fontSize: 104,
            lineHeight: 1.08, color: CLAUDE.INK, opacity: inAt(6),
          }}>
            {label}
          </div>
        </div>

        {/* span bar */}
        <div style={{ width: SAFE.w }}>
          <div style={{
            display: 'flex', justifyContent: 'space-between',
            fontFamily: SANS, fontSize: 32, color: CLAUDE.INK, opacity: inAt(16),
          }}>
            <span>{opened}</span>
            <span style={{ opacity: open ? 0 : 1 }}>{closed}</span>
          </div>
          <div style={{ marginTop: 16, width: SAFE.w, height: 30, background: CLAUDE.PILL, borderRadius: 4 }}>
            <div style={{
              width: SAFE.w * fill * (open ? 0.72 : 1), height: 30,
              background: CLAUDE.SPARK, borderRadius: 4,
            }} />
          </div>
          <div style={{
            marginTop: 20, fontFamily: SERIF, fontSize: 64,
            color: CLAUDE.INK, opacity: inAt(24),
          }}>
            {Math.round(days * fill)} days{open ? ' — and counting' : ''}
          </div>
        </div>

        {/* whose court, and how it ended */}
        <div>
          <div style={{
            fontFamily: SANS, fontSize: 30, color: CLAUDE.INK_SOFT, opacity: inAt(30),
          }}>
            Ball in: {court}
          </div>
          <div style={{
            marginTop: 20, maxWidth: SAFE.w, fontFamily: SERIF, fontSize: 54,
            lineHeight: 1.28, color: CLAUDE.INK, opacity: inAt(36),
          }}>
            {resolution}
          </div>
        </div>

        <div style={{
          fontFamily: SANS, fontSize: 26, color: CLAUDE.GHOST, letterSpacing: '0.06em',
        }}>
          {folderLabel}
        </div>
      </div>
    </AbsoluteFill>
  );
};
