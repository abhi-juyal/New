import { AbsoluteFill, Composition, interpolate, useCurrentFrame } from "remotion";

// Starter: a vertical 9:16 title card. Duplicate this file for new motion graphics.
export const MyComponent: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });
  const scale = interpolate(frame, [0, 15], [0.9, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "#111", justifyContent: "center", alignItems: "center" }}>
      <div style={{ color: "white", fontSize: 110, fontWeight: 800, fontFamily: "sans-serif", opacity, transform: `scale(${scale})` }}>
        Remotion works
      </div>
    </AbsoluteFill>
  );
};

export const MyComposition = () => (
  <Composition id="MyComp" component={MyComponent} durationInFrames={60} fps={30} width={1080} height={1920} />
);
