import type { FC } from "react";
import { Composition } from "remotion";
import { CourseIntro, courseIntroDefaultProps } from "./CourseIntro";
import {
  CourseIntroVertical,
  courseIntroVerticalDefaultProps,
} from "./CourseIntroVertical";

export const RemotionRoot: FC = () => {
  return (
    <>
      <Composition
        id="CourseIntro"
        component={CourseIntro}
        durationInFrames={150}
        fps={30}
        width={1280}
        height={720}
        defaultProps={courseIntroDefaultProps}
      />
      {/* Variante 9:16 (1080x1920) para criativos de video de ads */}
      <Composition
        id="CourseIntroVertical"
        component={CourseIntroVertical}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={courseIntroVerticalDefaultProps}
      />
    </>
  );
};
