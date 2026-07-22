import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { claudeTitleOutroSchema } from './ClaudeTitleOutro';
import type { ClaudeTitleOutroProps } from './ClaudeTitleOutro';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * ClaudeTitleOutro916 — portrait 9:16 (1080×1920) version of ClaudeTitleOutro.
 * Same schema, same logic. Font sizes derived from height so they fill portrait.
 * Per REFLOW rule: fill the width, distribute content down the height.
 * Safe zone: top 12% (~230px) and bottom 25% (~480px) reserved for platform UI.
 * Active band: y 230–1440, x 54–1026.
 */

export const claudeTitleOutro916Schema = claudeTitleOutroSchema;
export type ClaudeTitleOutro916Props = ClaudeTitleOutroProps;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const ClaudeTitleOutro916: React.FC<ClaudeTitleOutro916Props> = ({ title, handle, subline }) => {
  const frame = useCurrentFrame();
  const { height } = useVideoConfig();
  const o = clamp(interpolate(frame, [0, 14], [0, 1]), 0, 1);

  const _pm = title.match(/^([\s\S]*?)\s*([.?!…]+)\s*$/);
  const titleBody = _pm ? _pm[1] : title;
  const titlePunct = _pm ? _pm[2] : '.';

  // Portrait: top 12% = 230px, bottom 25% = 480px safe zones
  // Center content in active band (230–1440px)
  const TITLE_FONT = height * 0.055;    // ~106px in 1920
  const HANDLE_FONT = height * 0.030;   // ~58px
  const SUBLINE_FONT = height * 0.018;  // ~35px
  const PAD_X = 72; // ~6.7% of 1080

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
        fontSize: TITLE_FONT,
        color: CLAUDE.INK,
        letterSpacing: '-0.02em',
        textAlign: 'center',
        lineHeight: 1.08,
        maxWidth: 1080 - PAD_X * 2,
        padding: `0 ${PAD_X}px`,
      }}>
        {titleBody}
        <span style={{ color: CLAUDE.SEND }}>{titlePunct}</span>
      </div>

      {/* Handle */}
      <div style={{
        fontFamily: SERIF,
        fontSize: HANDLE_FONT,
        color: CLAUDE.INK,
        marginTop: height * 0.022,
        opacity: 0.9,
        textAlign: 'center',
      }}>
        {handle}
      </div>

      {/* Subline */}
      <div style={{
        fontFamily: SANS,
        fontSize: SUBLINE_FONT,
        color: CLAUDE.INK_SOFT,
        marginTop: height * 0.012,
        textAlign: 'center',
        maxWidth: 1080 - PAD_X * 2,
        padding: `0 ${PAD_X}px`,
        lineHeight: 1.4,
      }}>
        {subline}
      </div>
    </AbsoluteFill>
  );
};
