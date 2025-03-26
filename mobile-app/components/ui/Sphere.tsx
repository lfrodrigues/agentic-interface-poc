import React, { useState, useEffect } from "react";
import { View } from "react-native";
import Animated, { useSharedValue, withRepeat, withTiming, useAnimatedProps, Easing } from "react-native-reanimated";
import Svg, { Circle } from "react-native-svg";

const AnimatedCircle = Animated.createAnimatedComponent(Circle);

const NUM_DOTS = 600;
const RADIUS = 100;
const DEPTH = 450;
const CENTER_X = 200;
const CENTER_Y = 200;

interface Dot {
  theta: number;
  phi: number;
  depthOffset: number;
  size: number;
  color: string;
}

const generateDots = (): Dot[] => {
  return Array.from({ length: NUM_DOTS }, () => {
    const baseSize = 0.5 + Math.random() * 0.5;
    const color = 'white';
    return {
      theta: Math.random() * Math.PI * 2,
      phi: Math.acos(2 * Math.random() - 1),
      depthOffset: Math.random() * 60 - 30,
      size: baseSize,
      color,
    };
  });
};

export const VortexSphere = () => {
  const [dots] = useState<Dot[]>(generateDots);
  const rotation = useSharedValue(0);

  useEffect(() => {
    rotation.value = withRepeat(
      withTiming(Math.PI * 2, { duration: 20000, easing: Easing.linear }),
      -1
    );
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }} className="opacity-70">
      <Svg width={400} height={400}>
        {dots.map((dot, index) => {
          const animatedProps = useAnimatedProps(() => {
            const angle = rotation.value;
            const newTheta = dot.theta + angle * 0.02;
            const x = RADIUS * Math.sin(dot.phi) * Math.cos(newTheta);
            const y = RADIUS * Math.sin(dot.phi) * Math.sin(newTheta);
            const z = RADIUS * Math.cos(dot.phi) + dot.depthOffset;

            const xRot = x * Math.cos(angle) - z * Math.sin(angle);
            const zRot = x * Math.sin(angle) + z * Math.cos(angle);
            const scale = DEPTH / (DEPTH - zRot);
            const screenX = CENTER_X + xRot * scale;
            const screenY = CENTER_Y + y * scale;
            const opacity = Math.max(0.05, scale * 1.1);
            const size = dot.size * scale * 1.5;

            return {
              cx: screenX,
              cy: screenY,
              r: size,
              fill: dot.color,
              fillOpacity: opacity,
              mixBlendMode: 'overlay', // Apply to each circle
            };
          });

          return <AnimatedCircle key={index} animatedProps={animatedProps} />;
        })}
      </Svg>
    </View>
  );
};
