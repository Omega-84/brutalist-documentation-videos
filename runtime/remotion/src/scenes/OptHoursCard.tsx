import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import { SAFE, safeX, safeY } from '../tokens/layout';

/**
 * OptHoursCard — the month's documented OPT hours, one row per week.
 *
 * A typographic LEDGER, not a bar chart. Every week in the source reports is
 * exactly 20 hours, so bars would draw four identical full-width blocks —
 * implying a variance that does not exist and adding motion that decorates
 * rather than enacts. The rows rule in one at a time and the numerals count
 * up; the total is the one terracotta moment.
 *
 * HONESTY: these are hours DOCUMENTED in the weekly reports, not hours
 * measured by a tracker. The caption prop carries that qualification and is
 * not optional — a bare hours figure would overclaim.
 */

export const optHoursCardSchema = z.object({
  heading: z.string().default('Documented hours'),
  rows: z.array(z.object({ label: z.string(), hours: z.number() })).default([]),
  total: z.number().default(80),
  // status renders as a standalone compliance line beneath the total.
  status: z.string().default('In compliance'),
  caption: z.string().default(''),
  folderLabel: z.string().default('@HumanitariansAI'),
});
export type OptHoursCardProps = z.infer<typeof optHoursCardSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const OptHoursCard: React.FC<OptHoursCardProps> = ({
  heading, rows, total, status, caption, folderLabel,
}) => {
  const frame = useCurrentFrame();
  const inAt = (start: number) => clamp(interpolate(frame, [start, start + 14], [0, 1]), 0, 1);


  // Five rows (June) need tighter rhythm than three (July) to leave the total
  // block its room.
  const rowPad = rows.length >= 5 ? 22 : 30;
  const rowSize = rows.length >= 5 ? 42 : 48;
  const totalReveal = 10 + rows.length * 10 + 8;

  return (
    <AbsoluteFill style={{ background: CLAUDE.PAGE }}>
      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(0),
        width: SAFE.w, height: SAFE.h,
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
      }}>
        <div>
          <div style={{
            fontFamily: SANS, fontSize: 30, letterSpacing: '0.16em',
            color: CLAUDE.INK_SOFT, opacity: inAt(0),
          }}>
            {heading.toUpperCase()}
          </div>

          <div style={{ marginTop: 40, display: 'flex', flexDirection: 'column' }}>
            {rows.map((r, i) => {
              const p = inAt(10 + i * 10);
              return (
                <div key={i} style={{
                  display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
                  gap: 28, paddingTop: rowPad, paddingBottom: rowPad,
                  borderBottom: `2px solid ${CLAUDE.BORDER}`,
                  opacity: p,
                }}>
                  <div style={{ fontFamily: SANS, fontSize: rowSize, color: CLAUDE.INK }}>
                    {r.label}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: 14 }}>
                    <div style={{ fontFamily: SERIF, fontSize: rowSize + 14, color: CLAUDE.INK }}>
                      {Math.round(r.hours * p)}
                    </div>
                    <div style={{ fontFamily: SANS, fontSize: 26, color: CLAUDE.GHOST }}>hrs</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 26, opacity: inAt(totalReveal) }}>
            <div style={{ fontFamily: SERIF, fontSize: 150, lineHeight: 1, color: CLAUDE.SPARK }}>
              {Math.round(total * inAt(totalReveal))}
            </div>
            <div style={{ fontFamily: SANS, fontSize: 42, color: CLAUDE.INK }}>hours documented</div>
          </div>
          {status !== '' && (
            <div style={{
              marginTop: 26, display: 'inline-flex', alignItems: 'center', gap: 16,
              opacity: inAt(totalReveal + 8),
            }}>
              <div style={{ width: 16, height: 16, borderRadius: 8, background: CLAUDE.SPARK }} />
              <div style={{
                fontFamily: SANS, fontSize: 44, letterSpacing: '0.04em', color: CLAUDE.INK,
              }}>
                Status: {status}
              </div>
            </div>
          )}
        </div>

        <div>
          {caption !== '' && (
            <div style={{
              maxWidth: SAFE.w, fontFamily: SANS, fontSize: 28, lineHeight: 1.35,
              color: CLAUDE.INK_SOFT, opacity: inAt(totalReveal + 10),
            }}>
              {caption}
            </div>
          )}
          <div style={{
            marginTop: 22, fontFamily: SANS, fontSize: 26,
            color: CLAUDE.GHOST, letterSpacing: '0.06em',
          }}>
            {folderLabel}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
