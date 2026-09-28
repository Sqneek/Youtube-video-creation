import React from "react";
import { Composition } from "remotion";
import { Enhanced } from "./Enhanced";
import timeline from "./data/timeline.json";

// The composition is fully data-driven: dimensions, fps and duration all come
// from src/data/timeline.json, which scripts/prepare.py regenerates for whichever
// video is being enhanced. Re-running prepare.py + re-rendering is all that's
// needed to point this at a different video — no code edits.
export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Enhanced"
      component={Enhanced}
      durationInFrames={Math.max(1, timeline.totalFrames)}
      fps={timeline.fps}
      width={timeline.width}
      height={timeline.height}
    />
  );
};
