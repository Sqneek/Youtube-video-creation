import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";

// Six gentle Ken Burns movements. Scale stays >= ~1.08 and translation is kept
// within the covered margin so the image edges never expose the background.
type Move = { fromScale: number; toScale: number; fromX: number; toX: number; fromY: number; toY: number };

const MOVES: Move[] = [
  { fromScale: 1.06, toScale: 1.2, fromX: 0, toX: 0, fromY: 0, toY: 0 }, // slow zoom in
  { fromScale: 1.2, toScale: 1.06, fromX: 0, toX: 0, fromY: 0, toY: 0 }, // slow zoom out
  { fromScale: 1.14, toScale: 1.14, fromX: -5, toX: 5, fromY: 0, toY: 0 }, // pan left -> right
  { fromScale: 1.14, toScale: 1.14, fromX: 5, toX: -5, fromY: 0, toY: 0 }, // pan right -> left
  { fromScale: 1.12, toScale: 1.2, fromX: -3, toX: 3, fromY: 3, toY: -3 }, // diagonal + zoom
  { fromScale: 1.12, toScale: 1.2, fromX: 3, toX: -3, fromY: -3, toY: 3 }, // diagonal + zoom
];

export const KenBurns: React.FC<{ src: string; index: number; durationInFrames: number }> = ({
  src,
  index,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const m = MOVES[index % MOVES.length];
  const p = durationInFrames <= 1 ? 0 : frame / (durationInFrames - 1);

  const scale = interpolate(p, [0, 1], [m.fromScale, m.toScale]);
  const x = interpolate(p, [0, 1], [m.fromX, m.toX]);
  const y = interpolate(p, [0, 1], [m.fromY, m.toY]);

  // Short fade-in to soften each hard cut without altering scene timing.
  const opacity = interpolate(frame, [0, 8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#000" }}>
      <Img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${x}%, ${y}%)`,
          transformOrigin: "center center",
          opacity,
        }}
      />
    </AbsoluteFill>
  );
};
