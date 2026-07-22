import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * ClaudeTitleOutro — reusable title-restate outro for claude-musinique (and all claude-* channels).
 * Per OUTRO LAW: poster-style serif title, terracotta period, handle beneath, subline.
 * Simple fade-in; clean hold; cream ground.
 */

export const claudeTitleOutroSchema = z.object({
  title: z.string().default('Claude, In Your Corner.'),
  handle: z.string().default('@Musinique'),
  subline: z.string().default('bot vs bot, season one'),
});
export type ClaudeTitleOutroProps = z.infer<typeof claudeTitleOutroSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const ClaudeTitleOutro: React.FC<ClaudeTitleOutroProps> = ({ title, handle, subline }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const o = clamp(interpolate(frame, [0, 14], [0, 1]), 0, 1);

  // Render the title's terminal punctuation (. ? !) in terracotta. A question
  // keeps its question mark; a title with no terminal mark gets a period.
  const _pm = title.match(/^([\s\S]*?)\s*([.?!\u2026]+)\s*$/);
  const titleBody = _pm ? _pm[1] : title;
  const titlePunct = _pm ? _pm[2] : '.';

  return (
    <AbsoluteFill style={{
      background: CLAUDE.PAGE,
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'column',
      gap: 0,
      opacity: o,
    }}>
      {/* Title line */}
      <div style={{
        fontFamily: SERIF,
        fontWeight: 700,
        fontSize: 72,
        color: CLAUDE.INK,
        letterSpacing: '-0.02em',
        textAlign: 'center',
        lineHeight: 1.08,
        maxWidth: 1080,
        padding: '0 60px',
      }}>
        {titleBody}
        <span style={{ color: CLAUDE.SEND }}>{titlePunct}</span>
      </div>

      {/* Handle */}
      <div style={{
        fontFamily: SERIF,
        fontSize: 38,
        color: CLAUDE.INK,
        marginTop: 28,
        opacity: 0.9,
      }}>
        {handle}
      </div>

      {/* Subline */}
      <div style={{
        fontFamily: SANS,
        fontSize: 22,
        color: CLAUDE.INK_SOFT,
        marginTop: 14,
        textAlign: 'center',
        maxWidth: 640,
      }}>
        {subline}
      </div>
    </AbsoluteFill>
  );
};
