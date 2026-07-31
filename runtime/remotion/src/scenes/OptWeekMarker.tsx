import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import { SAFE, safeX, safeY } from '../tokens/layout';

/**
 * OptWeekMarker — the spine beat of the Medhavy OPT monthly recaps.
 *
 * Marks WHERE in the month we are (a pip timeline across the top), WHICH week
 * (date range in the serif + the week ordinal), and WHAT that week was (a
 * thesis line and up to four evidence bullets that wipe in one at a time).
 *
 * The one terracotta moment is the active pip and the rule beneath the date.
 */

export const optWeekMarkerSchema = z.object({
  week: z.number().default(1),
  // weeks: 0 hides the timeline rail entirely — used when the card carries a
  // topic rather than a position in the month.
  weeks: z.number().default(4),
  // label overrides the default "WEEK n OF m" eyebrow. Set it for topic cards.
  label: z.string().default(''),
  dates: z.string().default('May 1–7, 2026'),
  thesis: z.string().default('Two workstreams, from day one.'),
  bullets: z.array(z.string()).default([]),
  folderLabel: z.string().default('@HumanitariansAI'),
});
export type OptWeekMarkerProps = z.infer<typeof optWeekMarkerSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const OptWeekMarker: React.FC<OptWeekMarkerProps> = ({
  week, weeks, label, dates, thesis, bullets, folderLabel,
}) => {
  const frame = useCurrentFrame();
  const inAt = (start: number) => clamp(interpolate(frame, [start, start + 12], [0, 1]), 0, 1);

  const pipGap = 18;
  // The rail spans the full safe width whatever the week count, so May (4 pips)
  // and June (5 pips) read as the same graphic at different resolutions.
  const pipW = (SAFE.w - (weeks - 1) * pipGap) / weeks;

  const shown = bullets.slice(0, 4);
  // FILL-THE-CANVAS: the blocks are distributed down the full safe height by
  // space-between rather than stacked from the top, so a 2-bullet beat and a
  // 4-bullet beat both occupy the frame. Type scales down only as the bullet
  // count grows, which is when the extra rows take up the slack.
  const bulletSize = shown.length >= 4 ? 40 : 46;
  const dateSize = shown.length >= 4 ? 116 : 128;
  const thesisSize = shown.length >= 4 ? 62 : 70;

  return (
    <AbsoluteFill style={{ background: CLAUDE.PAGE }}>
      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(0),
        width: SAFE.w, height: SAFE.h,
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
      }}>
        {/* timeline rail + week ordinal + date range */}
        <div>
          {weeks > 0 && (
            <div style={{ display: 'flex', gap: pipGap, width: SAFE.w }}>
              {Array.from({ length: weeks }, (_, i) => (
                <div key={i} style={{
                  width: pipW, height: 10, borderRadius: 5,
                  background: i + 1 === week ? CLAUDE.SPARK : CLAUDE.PILL,
                  opacity: i + 1 <= week ? 1 : 0.45,
                  transform: `scaleX(${i + 1 === week ? inAt(6) : 1})`,
                  transformOrigin: 'left center',
                }} />
              ))}
            </div>
          )}
          <div style={{ opacity: inAt(0), marginTop: weeks > 0 ? 62 : 0 }}>
            <div style={{ fontFamily: SANS, fontSize: 30, letterSpacing: '0.16em', color: CLAUDE.INK_SOFT }}>
              {label || `WEEK ${week} OF ${weeks}`}
            </div>
            <div style={{
              fontFamily: SERIF, fontSize: dateSize, lineHeight: 1.04, color: CLAUDE.INK,
              marginTop: 6, maxWidth: SAFE.w,
            }}>
              {dates}
            </div>
            <div style={{
              width: 260, height: 6, background: CLAUDE.SPARK, marginTop: 20,
              transform: `scaleX(${inAt(10)})`, transformOrigin: 'left center',
            }} />
          </div>
        </div>

        {/* thesis */}
        <div style={{
          maxWidth: SAFE.w, fontFamily: SERIF, fontSize: thesisSize, lineHeight: 1.22,
          color: CLAUDE.INK, opacity: inAt(18),
        }}>
          {thesis}
        </div>

        {/* evidence bullets */}
        <div style={{
          maxWidth: SAFE.w, display: 'flex', flexDirection: 'column',
          gap: shown.length >= 4 ? 24 : 32,
        }}>
          {shown.map((b, i) => (
            <div key={i} style={{ display: 'flex', gap: 22, alignItems: 'baseline', opacity: inAt(30 + i * 14) }}>
              <div style={{
                width: 18, height: 18, flexShrink: 0, borderRadius: 9,
                border: `3px solid ${CLAUDE.INK_SOFT}`, transform: 'translateY(2px)',
              }} />
              <div style={{
                fontFamily: SANS, fontSize: bulletSize, lineHeight: 1.3,
                color: CLAUDE.INK, maxWidth: SAFE.w - 60,
              }}>
                {b}
              </div>
            </div>
          ))}
        </div>

        {/* channel chip */}
        <div style={{
          fontFamily: SANS, fontSize: 26, color: CLAUDE.GHOST, letterSpacing: '0.06em',
        }}>
          {folderLabel}
        </div>
      </div>
    </AbsoluteFill>
  );
};
