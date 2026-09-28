import React from "react";
import { AbsoluteFill, Audio, interpolate, Series, staticFile, useVideoConfig } from "remotion";
import timeline from "./data/timeline.json";
import config from "./data/config.json";
import { KenBurns } from "./KenBurns";
import { Captions } from "./Captions";

const Music: React.FC<{ src: string; volume: number }> = ({ src, volume }) => {
  const { durationInFrames, fps } = useVideoConfig();
  return (
    <Audio
      src={staticFile(src)}
      loop
      volume={(f) =>
        interpolate(
          f,
          [0, fps * 2, durationInFrames - fps * 4, durationInFrames],
          [0, volume, volume, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        )
      }
    />
  );
};

export const Enhanced: React.FC = () => {
  const scenes = timeline.scenes ?? [];
  const music = (config as { music: string | null }).music;
  const musicVolume = (config as { musicVolume?: number }).musicVolume ?? 0.14;
  const narration = (config as { narration: string | null }).narration;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {scenes.length > 0 && (
        <Series>
          {scenes.map((scene, i) => (
            <Series.Sequence key={i} durationInFrames={scene.durationInFrames}>
              <KenBurns src={scene.file} index={i} durationInFrames={scene.durationInFrames} />
            </Series.Sequence>
          ))}
        </Series>
      )}

      {narration && <Audio src={staticFile(narration)} />}
      {music && <Music src={music} volume={musicVolume} />}

      <Captions />
    </AbsoluteFill>
  );
};
