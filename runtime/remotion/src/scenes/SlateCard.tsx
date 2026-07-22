import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate,
} from 'remotion';
import { z } from 'zod';
import { VOX, FONT, SPRING_SMOOTH } from '../tokens/vox';

/**
 * SlateCard — general-purpose kinetic text fill for slate beats.
 * Replaces a grey slate with a branded motion-graphic card: CREAM ground,
 * TEAL eyebrow (act name), large INK display text (truncated narration),
 * GOLD rule. Works for any act / any topic. Duration-driven.
 * Content injected per beat by the vox fill-slates driver.
 */
export const slateCardSchema = z.object({
  headline: z.string(),
  eyebrow:  z.string().default(''),
  topic:    z.string().default(''),
});
export type SlateCardProps = z.infer<typeof slateCardSchema>;

export const SlateCard: React.FC<SlateCardProps> = ({ headline, eyebrow, topic }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const topicIn   = spring({ frame,        fps, config: SPRING_SMOOTH });
  const eyeIn     = spring({ frame: frame - 4,  fps, config: SPRING_SMOOTH });
  const headIn    = spring({ frame: frame - 10, fps, config: SPRING_SMOOTH });
  const ruleIn    = spring({ frame: frame - 18, fps, config: SPRING_SMOOTH });

  // Subtle geometric accent: a large SLATE circle, mostly off-screen bottom-right
  const circleR = height * 1.1;
  const circleOpacity = interpolate(frame, [0, 20], [0, 0.06], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: VOX.CREAM, overflow: 'hidden' }}>

      {/* Background circle accent */}
      <div style={{
        position: 'absolute',
        width: circleR * 2,
        height: circleR * 2,
        borderRadius: '50%',
        backgroundColor: VOX.SLATE,
        bottom: -circleR * 0.7,
        right: -circleR * 0.7,
        opacity: circleOpacity,
      }} />

      {/* Content block — left-aligned, vertically centered */}
      <div style={{
        position: 'absolute',
        left: width * 0.10,
        right: width * 0.10,
        top: '50%',
        transform: 'translateY(-50%)',
      }}>

        {/* Topic eyebrow (series name) */}
        {topic ? (
          <div style={{
            fontFamily: FONT.display,
            fontSize: height * 0.020,
            fontWeight: 700,
            letterSpacing: 3,
            textTransform: 'uppercase' as const,
            color: VOX.SLATE,
            marginBottom: height * 0.016,
            opacity: topicIn * 0.65,
            transform: `translateY(${(1 - topicIn) * 8}px)`,
          }}>
            {topic}
          </div>
        ) : null}

        {/* Act eyebrow */}
        {eyebrow ? (
          <div style={{
            fontFamily: FONT.display,
            fontSize: height * 0.022,
            fontWeight: 700,
            letterSpacing: 2,
            textTransform: 'uppercase' as const,
            color: VOX.TEAL,
            marginBottom: height * 0.022,
            opacity: eyeIn,
            transform: `translateY(${(1 - eyeIn) * 10}px)`,
          }}>
            {eyebrow}
          </div>
        ) : null}

        {/* Headline */}
        <div style={{
          fontFamily: FONT.display,
          fontSize: height * 0.074,
          fontWeight: 800,
          color: VOX.INK,
          lineHeight: 1.08,
          letterSpacing: -1.5,
          opacity: headIn,
          transform: `translateY(${(1 - headIn) * 22}px)`,
          marginBottom: height * 0.030,
        }}>
          {headline}
        </div>

        {/* GOLD rule */}
        <div style={{
          width: width * 0.10,
          height: 3,
          backgroundColor: VOX.GOLD,
          opacity: ruleIn,
          transform: `scaleX(${ruleIn})`,
          transformOrigin: 'left',
        }} />
      </div>
    </AbsoluteFill>
  );
};
