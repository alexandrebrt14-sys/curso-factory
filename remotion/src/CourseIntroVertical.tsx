/**
 * CourseIntroVertical — variante 9:16 (1080x1920) da abertura de curso, para
 * criativos de video de ads (Meta/Google/Shorts/Reels). Espelha
 * landing-page-geo/src/remotion/compositions/CourseIntroVertical.
 */
import type { FC } from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { CourseIntroProps } from "./CourseIntro";

export type CourseIntroVerticalProps = CourseIntroProps & {
  cta: string;
};

export const courseIntroVerticalDefaultProps: CourseIntroVerticalProps = {
  titulo: "Geografia da IA para Educacao",
  nivel: "intermediario",
  modulos: 12,
  duracao: "~280 min",
  corDestaque: "#0176d3",
  cta: "Comece gratis em brasilgeo.ai",
};

const Pill: FC<{ label: string; opacity: number }> = ({ label, opacity }) => (
  <div
    style={{
      padding: "16px 30px",
      borderRadius: 999,
      border: "1px solid rgba(255,255,255,0.18)",
      background: "rgba(255,255,255,0.06)",
      color: "#e2e8f0",
      fontSize: 38,
      opacity,
    }}
  >
    {label}
  </div>
);

export const CourseIntroVertical: FC<CourseIntroVerticalProps> = ({
  titulo,
  nivel,
  modulos,
  duracao,
  corDestaque,
  cta,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const t = spring({ frame, fps, config: { damping: 200 } });
  const tituloY = interpolate(t, [0, 1], [70, 0]);
  const modAnim = Math.round(
    interpolate(spring({ frame: frame - 18, fps }), [0, 1], [0, modulos], {
      extrapolateRight: "clamp",
    })
  );
  const pillsOpacity = spring({ frame: frame - 28, fps });
  const ctaOpacity = spring({ frame: frame - 44, fps });

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(160deg, #032d60 0%, #0a1b3a 100%)",
        fontFamily:
          'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
        justifyContent: "space-between",
        padding: "140px 80px",
      }}
    >
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 50% 30%, ${corDestaque}33, transparent 60%)`,
        }}
      />
      <div>
        <div
          style={{
            color: corDestaque,
            fontSize: 40,
            fontWeight: 700,
            letterSpacing: "0.18em",
            textTransform: "uppercase",
            opacity: t,
          }}
        >
          Brasil GEO Educacao
        </div>
        <h1
          style={{
            fontSize: 110,
            lineHeight: 1.03,
            fontWeight: 800,
            color: "#fff",
            margin: "28px 0 0",
            letterSpacing: "-0.03em",
            opacity: t,
            transform: `translateY(${tituloY}px)`,
          }}
        >
          {titulo}
        </h1>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 22,
          alignItems: "flex-start",
        }}
      >
        <Pill label={`Nivel ${nivel}`} opacity={pillsOpacity} />
        <Pill label={`${modAnim} modulos`} opacity={pillsOpacity} />
        <Pill label={duracao} opacity={pillsOpacity} />
      </div>
      <div
        style={{
          opacity: ctaOpacity,
          background: corDestaque,
          color: "#fff",
          fontSize: 46,
          fontWeight: 700,
          padding: "32px 44px",
          borderRadius: 24,
          textAlign: "center",
        }}
      >
        {cta}
      </div>
    </AbsoluteFill>
  );
};
