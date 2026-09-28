import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { createTikTokStyleCaptions, type Caption } from "@remotion/captions";
import captionsData from "./data/captions.json";

const ACCENT = "#ffcf4d"; // warm gold highlight for the spoken word

export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const nowMs = (frame / fps) * 1000;

  const pages = useMemo(() => {
    if (!captionsData || (captionsData as Caption[]).length === 0) return [];
    const { pages } = createTikTokStyleCaptions({
      captions: captionsData as Caption[],
      combineTokensWithinMilliseconds: 1200,
    });
    return pages;
  }, []);

  const page = useMemo(
    () => pages.find((pg) => nowMs >= pg.startMs && nowMs < pg.startMs + pg.durationMs),
    [pages, nowMs],
  );

  if (!page) return null;

  // Scale caption size with the video height so it reads well at any resolution.
  const fontSize = Math.round(height * 0.06);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: Math.round(height * 0.09),
      }}
    >
      <div
        style={{
          maxWidth: "82%",
          textAlign: "center",
          fontFamily: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
          fontWeight: 800,
          fontSize,
          lineHeight: 1.18,
          letterSpacing: 0.3,
          textShadow: "0 2px 8px rgba(0,0,0,0.9), 0 0 3px rgba(0,0,0,0.95)",
        }}
      >
        {page.tokens.map((token, i) => {
          const active = nowMs >= token.fromMs && nowMs < token.toMs;
          return (
            <span
              key={i}
              style={{
                color: active ? ACCENT : "#ffffff",
                WebkitTextStroke: "1.5px rgba(0,0,0,0.85)",
              }}
            >
              {token.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
