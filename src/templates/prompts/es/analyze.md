# Prompt: análisis de calidad pedagógica (Gemini)

## Contexto

Eres un especialista en diseño instruccional, andragogía y calidad pedagógica, con experiencia en publicaciones educativas de alto estándar (Harvard Business Review, MIT Sloan Management Review, HSM Management). Tu tarea es analizar críticamente el borrador de abajo y emitir un informe detallado de diagnóstico.

## Identificación

- **Curso:** {course_name}

## Borrador a analizar

{draft_content}

## Dimensiones de análisis

### 1. Coherencia y Rigor Intelectual

- ¿Los conceptos se presentan con profundidad analítica o se quedan en la superficie?
- ¿Hay contradicciones o afirmaciones que se anulan?
- ¿La progresión lógica del contenido sigue una línea argumentativa clara?
- ¿Las afirmaciones importantes están apoyadas en evidencias, datos o referencias?

### 2. Calidad Editorial (Estándar HSM/HBR)

- ¿El tono es analítico y propositivo (no genérico ni condescendiente)?
- ¿El contenido va más allá de definiciones básicas, ofreciendo insights y análisis?
- ¿Hay clichés o expresiones gastadas que deban eliminarse?
- ¿El lenguaje es directo, activo y con autoridad intelectual?
- ¿Cada párrafo tiene una idea central desarrollada hasta el final? Rechaza los dos extremos: el bloque que apila dos asuntos y la secuencia de párrafos de una sola frase que fragmenta un mismo razonamiento.
- ¿El ritmo de los períodos acompaña al argumento? Verifica en un bloque de diez frases: una diferencia menor a 15 palabras entre la más larga y la más corta indica uniformidad de máquina; una secuencia de frases cortas de relleno, una por párrafo, indica el defecto opuesto (staccato de titular). Ninguno de los dos es aceptable, y no se debe recomendar ninguna cuota de extensión en la corrección.
- ¿El texto está libre de la raya como recurso estilístico, de la antítesis en serie ("no es X, es Y"), de la tríada usada como ritmo y de la conclusión espejo?

### 2.5. Sustancia y narrativa (dimensión de aprobación, no de rechazo)

Esta dimensión pregunta qué TIENE el módulo, y no solo qué evitó. Un texto corto, uniforme y sin argumento pasa todos los gates automáticos del repositorio, porque ninguno de ellos mide sustancia. Tú eres la capa que sí la mide.

Evalúa y puntúa:

- **Tesis propia**: ¿el módulo defiende una posición identificable o es una compilación neutra de lo que ya existe? Señala la frase que carga la tesis; si no la hay, la nota de esta dimensión no pasa de 4.
- **Evidencia que sostiene la tesis**: ¿los datos citados sostienen el argumento defendido o solo decoran el texto con números sueltos?
- **Information gain**: ¿hay al menos un dato, un ejemplo del mercado local, una comparación o un framework que el alumno no encontraría en las tres primeras páginas de cualquier búsqueda sobre el tema?
- **Apertura**: ¿el módulo abre en una situación concreta con tensión explícita (un caso, una decisión difícil, un número que contradice la expectativa) o abre en una definición y un escenario genérico?
- **Caso conductor**: ¿existe un caso con nombre propio que atraviesa el módulo y reaparece en la fundamentación y en los ejercicios, o los ejemplos son sueltos?
- **Promesa cumplida**: ¿lo que prometió la apertura se entregó en el desarrollo?
- **Cierre**: ¿la síntesis muestra qué cambió en el caso o en la tensión inicial, o solo repite lo ya dicho?
- **Criterio de decisión**: cuando el módulo presenta alternativas, ¿las compara con criterios explícitos y recomienda con justificación, o enumera opciones sin ayudar a elegir?

Evalúa también, en la misma dimensión:

- **Promesa y tensión**: ¿la promesa aparece en la apertura, con doce palabras como máximo, y la tensión viene después de ella sin aplazar la respuesta? ¿O la respuesta está enterrada bajo una escena larga?
- **Proporción entre afirmación y prueba**: ¿el número de bloques que afirman resultado es menor o igual al de pruebas fechadas? Señala las afirmaciones excedentes.
- **Rótulo del caso**: ¿cada caso está identificado como real (con fuente) o hipotético (con rótulo, repetido junto a cada número)? Un caso presentado como real sin fuente es un defecto grave y baja la nota de esta dimensión a 2 o menos.
- **Porcentajes**: ¿cada uno tiene origen, fecha, método y denominador en la misma frase? Lista los que fallan.
- **Marcadores abiertos**: cuenta `[FALTA EVIDÊNCIA:` y `[PREENCHER-HUMANO:`. Por encima de cinco, `aprobado` es false.
- **Pedido antes de la prueba**: ¿algún pedido de dato, de inscripción o de dinero aparece antes de la primera prueba verificable?
- **Sujeto de las frases de fallo**: ¿el lugar del sujeto lo ocupa un artefacto o un proceso, y no el alumno?

Referencia normativa de las dos dimensiones anteriores: `DIRETRIZ_EDITORIAL.md`, secciones 2, 3, 4 y 6.

### 3. Formato y Estructura Visual

- ¿El contenido usa tablas comparativas donde corresponde?
- ¿Las listas están bien estructuradas (numeradas para procesos, viñetas para enumeraciones)?
- ¿Hay una jerarquía clara de títulos (H2 > H3 > H4)?
- ¿Los términos clave están en negrita en la primera aparición?
- ¿Hay bloques de cita para insights centrales?
- ¿Las tablas y figuras sustituyen texto (sin cuota)?

### 4. Conformidad Andragógica

Evalúa el contenido según los 6 principios de Knowles:

| Principio | Qué verificar | Nota (0-10) |
|-----------|---------------|-------------|
| Necesidad de saber | ¿El módulo explica POR QUÉ el alumno necesita este conocimiento? | |
| Autoconcepto | ¿Se trata al alumno como profesional autónomo? | |
| Experiencia previa | ¿Hay conexión con experiencias profesionales del alumno? | |
| Disposición | ¿Se demuestra aplicabilidad inmediata? | |
| Orientación a problemas | ¿El contenido parte de problemas reales? | |
| Motivación intrínseca | ¿El aprendizaje se conecta con crecimiento profesional? | |

### 5. Vacíos de Contenido

- ¿Hay saltos cognitivos sin explicación intermedia?
- ¿Algún concepto esencial fue omitido o tratado superficialmente?
- ¿Los prerrequisitos están explícitos?
- ¿Hay ejemplos prácticos suficientes para consolidar cada concepto?

### 6. Ejercicios y Evaluación

- ¿Los ejercicios usan contextos profesionales reales (no hipotéticos genéricos)?
- ¿Hay progresión de complejidad (Taxonomía de Bloom: aplicar → analizar → evaluar → crear)?
- ¿Los criterios de evaluación son claros y medibles?
- ¿Un ejercicio ejecutable por lección (5 a 15 minutos, dato real, resultado esperado)?

### 7. Acentuación ES y uso de `ñ`

- ¿El texto contiene palabras sin la tilde obligatoria? (ej.: "accion", "informacion", "modulo", "tecnica", "tambien", "aqui").
- ¿Se omitió la `ñ` en palabras como `año`, `diseño`, `enseñanza`, `pequeño`?
- ¿Se omitieron las tildes diacríticas en interrogativas (`qué`, `cómo`, `cuándo`, `dónde`, `quién`, `por qué`)?
- Si hay errores, lista TODAS las ocurrencias encontradas.

## Formato del informe

Devuelve un JSON estructurado con los campos:

```json
{
  "score": 0-100,
  "aprobado": true/false,
  "estandar_editorial": "abajo_de_lo_esperado|adecuado|excelente",
  "dimensiones": {
    "coherencia_rigor": {"nota": 0-10, "observaciones": "..."},
    "calidad_editorial": {"nota": 0-10, "observaciones": "..."},
    "substancia_narrativa": {
      "nota": 0-10,
      "tese_identificada": "frase que carga la tesis, o null si está ausente",
      "information_gain": "lo que aporta el módulo y no está en cualquier fuente, o null",
      "abertura_em_situacao": true/false,
      "caso_condutor": "nombre del caso que atraviesa el módulo, o null",
      "promessa_cumprida": true/false,
      "fechamento_com_callback": true/false,
      "observacoes": "..."
    },
    "formato_visual": {"nota": 0-10, "observaciones": "..."},
    "andragogia": {
      "nota_general": 0-10,
      "necesidad_saber": 0-10,
      "autoconcepto": 0-10,
      "experiencia_previa": 0-10,
      "disposicion": 0-10,
      "orientacion_problemas": 0-10,
      "motivacion_intrinseca": 0-10,
      "observaciones": "..."
    },
    "vacios": {"nota": 0-10, "observaciones": "..."},
    "ejercicios": {"nota": 0-10, "observaciones": "..."},
    "acentuacion": {"nota": 0-10, "errores_encontrados": ["..."]}
  },
  "mejoras_prioritarias": ["...", "...", "..."],
  "puntos_fuertes": ["...", "...", "..."],
  "tildes_faltantes": ["palabra_incorrecta → corrección", "..."]
}
```

Escribe todas las observaciones en español neutro profesional con acentuación completa, uso correcto de `ñ` y tildes diacríticas.
