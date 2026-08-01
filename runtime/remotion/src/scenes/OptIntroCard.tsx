import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import { SAFE, safeX, safeY } from '../tokens/layout';

/**
 * OptIntroCard — the executive summary, beat two.
 *
 * Answers the two questions a reviewer has before they will watch anything
 * else: who is speaking, and what is this. Name and role up top, the month
 * stated plainly, then three lines of what the video covers.
 *
 * Deliberately the only first-person card in the set.
 */

export const optIntroCardSchema = z.object({
  name: z.string().default('Varun Nayyar'),
  role: z.string().default('Volunteer · Medhavy · Humanitarians AI'),
  month: z.string().default('Month one — May 2026'),
  summary: z.array(z.string()).default([]),
  folderLabel: z.string().default('@HumanitariansAI'),
});
export type OptIntroCardProps = z.infer<typeof optIntroCardSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

const Spark: React.FC<{ size?: number }> = ({ size = 44 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" style={{ flexShrink: 0 }}>
    {Array.from({ length: 8 }, (_, i) => (
      <line key={i} x1={12} y1={12}
        x2={12 + 10 * Math.cos((i * Math.PI) / 4 + 0.2)}
        y2={12 + 10 * Math.sin((i * Math.PI) / 4 + 0.2)}
        stroke={CLAUDE.SPARK} strokeWidth={3.2} strokeLinecap="round" />
    ))}
  </svg>
);

export const OptIntroCard: React.FC<OptIntroCardProps> = ({
  name, role, month, summary, folderLabel,
}) => {
  const frame = useCurrentFrame();
  const inAt = (start: number) => clamp(interpolate(frame, [start, start + 14], [0, 1]), 0, 1);
  const shown = summary.slice(0, 3);

  return (
    <AbsoluteFill style={{ background: CLAUDE.PAGE }}>
      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(0),
        width: SAFE.w, height: SAFE.h,
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
      }}>
        {/* who */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 20, opacity: inAt(0) }}>
            <Spark size={44} />
            <div style={{
              fontFamily: SANS, fontSize: 30, letterSpacing: '0.16em', color: CLAUDE.INK_SOFT,
            }}>
              EXECUTIVE SUMMARY
            </div>
          </div>
          <div style={{
            marginTop: 30, fontFamily: SERIF, fontSize: 128, lineHeight: 1.02,
            color: CLAUDE.INK, opacity: inAt(4),
          }}>
            {name}
          </div>
          <div style={{
            marginTop: 20, fontFamily: SANS, fontSize: 38, color: CLAUDE.INK_SOFT,
            opacity: inAt(12),
          }}>
            {role}
          </div>
          <div style={{
            width: 300, height: 6, background: CLAUDE.SPARK, marginTop: 26,
            transform: `scaleX(${inAt(16)})`, transformOrigin: 'left center',
          }} />
        </div>

        {/* what */}
        <div>
          <div style={{
            fontFamily: SERIF, fontSize: 62, color: CLAUDE.INK, opacity: inAt(22),
            marginBottom: 34,
          }}>
            {month}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
            {shown.map((s, i) => (
              <div key={i} style={{
                display: 'flex', gap: 22, alignItems: 'baseline', opacity: inAt(30 + i * 12),
              }}>
                <div style={{
                  width: 14, height: 14, flexShrink: 0, borderRadius: 7,
                  background: CLAUDE.SPARK, transform: 'translateY(-2px)',
                }} />
                <div style={{
                  fontFamily: SANS, fontSize: 44, lineHeight: 1.3,
                  color: CLAUDE.INK, maxWidth: SAFE.w - 60,
                }}>
                  {s}
                </div>
              </div>
            ))}
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
