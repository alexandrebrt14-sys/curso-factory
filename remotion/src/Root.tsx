import type { FC } from "react";
import { Composition } from "remotion";
import { CourseIntro, courseIntroDefaultProps } from "./CourseIntro";

export const RemotionRoot: FC = () => {
  return (
    <Composition
      id="CourseIntro"
      component={CourseIntro}
      durationInFrames={150}
      fps={30}
      width={1280}
      height={720}
      defaultProps={courseIntroDefaultProps}
    />
  );
};
