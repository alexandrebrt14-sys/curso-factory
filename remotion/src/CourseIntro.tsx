/**
 * CourseIntro — abertura animada de curso, parametrizada por props.
 *
 * Espelha src/components/CourseVideoPlayer / src/remotion/compositions/CourseIntro
 * do landing-page-geo. Renderiza no Studio e via `remotion render` (export MP4).
 * As props vem do CourseDefinition do curso-factory (titulo/nivel/modulos/duracao),
 * passadas pelo video_generator.py como --props.
 */
import type { FC } from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// `type` (nao `interface`): Remotion exige props compativeis com Record<string, unknown>.
export type CourseIntroProps = {
  titulo: string;
  nivel: string;
  modulos: number;
  duracao: string;
  corDestaque: string;
};

export const courseIntroDefaultProps: CourseIntroProps = {
  titulo: "Geografia da IA para Educacao",
  nivel: "intermediario",
  modulos: 12,
  duracao: "~280 min",
  corDestaque: "#0176d3",
};

const Pill: FC<{ label: string; opacity: number }> = ({ label, opacity }) => (
  <div
    style={{
      padding: "10px 20px",
      borderRadius: 999,
      border: "1px solid rgba(255,255,255,0.18)",
      background: "rgba(255,255,255,0.06)",
      color: "#e2e8f0",
      fontSize: 24,
      opacity,
    }}
  >
    {label}
  </div>
);

export const CourseIntro: FC<CourseIntroProps> = ({
  titulo,
  nivel,
  modulos,
  duracao,
  corDestaque,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const t = spring({ frame, fps, config: { damping: 200 } });
  const tituloY = interpolate(t, [0, 1], [50, 0]);
  const modAnim = Math.round(
    interpolate(spring({ frame: frame - 18, fps }), [0, 1], [0, modulos], {
      extrapolateRight: "clamp",
    })
  );
  const pillsOpacity = spring({ frame: frame - 28, fps });

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #032d60 0%, #0a1b3a 100%)",
        fontFamily:
          'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
        justifyContent: "center",
        padding: 90,
      }}
    >
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 20% 20%, ${corDestaque}2e, transparent 55%)`,
        }}
      />
      <div
        style={{
          color: corDestaque,
          fontSize: 26,
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
          fontSize: 76,
          lineHeight: 1.04,
          fontWeight: 800,
          color: "#fff",
          margin: "18px 0 0",
          maxWidth: 1100,
          letterSpacing: "-0.03em",
          opacity: t,
          transform: `translateY(${tituloY}px)`,
        }}
      >
        {titulo}
      </h1>
      <div
        style={{
          display: "flex",
          gap: 16,
          marginTop: 48,
          flexWrap: "wrap",
          alignItems: "center",
        }}
      >
        <Pill label={`Nivel ${nivel}`} opacity={pillsOpacity} />
        <Pill label={`${modAnim} modulos`} opacity={pillsOpacity} />
        <Pill label={duracao} opacity={pillsOpacity} />
      </div>
    </AbsoluteFill>
  );
};
