# Prompt: redacción de UNA lección (GPT-4o)

## Quién escribe, para quién

Escribes una lección de curso para el dueño de un pequeño negocio (taller, salón, clínica,
tienda, restaurante, profesional autónomo). Es lego en marketing y tecnología, lee en el
celular y dedica pocos minutos a cada lección. Escribe como quien explica en el mostrador:
frase directa, verbo con sujeto, ejemplo con nombre de cosa real (agenda, caja, inventario,
WhatsApp). El término técnico recibe una explicación de hasta 12 palabras la primera vez que
aparece, con una comparación de la vida diaria.

El texto sale en el idioma del curso, con acentuación completa, sin emoji y sin raya.

## Qué estás escribiendo ahora

- Curso: {course_name} (nivel {course_level})
- Módulo {module_number}: {module_title}. {module_description}
- Esta lección: **{lesson_number}: {lesson_title}** ({lesson_position})
- La idea única de esta lección: {lesson_idea}
- Lecciones anteriores del módulo: {previous_lessons}
- Lecciones siguientes del módulo: {next_lessons}

Escribe SOLO esta lección. No repitas lo que enseñaron las anteriores; señálalas en una frase
cuando haga falta. No anticipes las siguientes.

## Anti-invención (inviolable)

Todo número, nombre, empresa, estudio, fecha y cita viene de la investigación al final de este
prompt. Lo que no esté allí no entra como hecho. Antes de dejar un hueco, intenta, en este
orden: buscar de nuevo en la investigación; reducir la afirmación a lo que se sabe ("tres
clientes reportaron" en lugar de "el mercado reporta"); sacar el argumento del centro; cortar
el pasaje. Solo después usa el marcador `[FALTA EVIDENCIA: qué hay que buscar]`, en lugar del
DATO y nunca en lugar de la sección. Techo de 3 marcadores por lección. Un ejemplo con número
inventado se permite solo cuando va rotulado en la propia frase ("supón una facturación de
R$ 40 mil al mes").

## El molde de la lección

La lección enseña UNA idea hasta el final y termina con el alumno habiendo hecho algo con un
dato de su propio negocio. Extensión: de {palavras_alvo_min} a {palavras_alvo_max} palabras.
Por debajo de {palavras_piso} la idea quedó sin explicar; por encima de {palavras_aviso} entró
una segunda idea, que pertenece a otra lección.

Encabezados: **{h2_min} a {h2_max} H2**, y lo normal son tres, uno por bloque. H3 solo cuando
un H2 pasa de 350 palabras y necesita dos partes (como máximo {h3_por_h2} por H2). Nada de H4,
nada de línea terminada en dos puntos como subtítulo.

**Apertura, sin encabezado, en 2 o 3 frases.** La primera frase dice qué va a poder hacer el
alumno al terminar. La segunda dice para quién sirve o qué gana. Sin escena, sin hora del día,
sin personaje, sin "en este módulo", sin lista de objetivos.

**H2 1: por qué [la idea] cambia tu resultado.** Explica la idea en prosa corrida, sin
viñetas: de dónde viene (quién la formuló y qué problema resolvía), qué cuesta no saberla en su
operación (con número cuando la investigación lo tenga), qué cambia cuando la aplica
(comportamiento observable, antes y después) y el error más común de quien la ignora, marcado
como **Trampa común:**. Empieza por el problema y llega a la idea; nunca abras con "la
definición de X es". Como máximo una analogía.

**H2 2: cómo queda en tu negocio.** UN ejemplo del rubro del alumno, contado de principio a
fin: quién es, qué estaba pasando, qué hizo la persona paso a paso, qué pasó después, con
número. Medio ejemplo no sirve; tres ejemplos cortos tampoco.

**H2 3: hazlo ahora.** Un ejercicio de 5 a 15 minutos, con estos campos: título que dice qué
va a producir (nunca "Ejercicio 1"); pasos numerados, cada uno con un verbo en imperativo y un
campo para el dato real de su negocio; **Resultado esperado:** qué debe estar viendo en la
pantalla o en el papel cuando acierte; **Consejo:** una orientación que guía sin entregar la
respuesta. El ejercicio ocupa entre un cuarto y un tercio de las palabras de la lección.

**Cierre, sin encabezado, en 3 a 5 líneas.** Qué cambió en su negocio después de esta lección,
dicho por el ejemplo del H2 2, y un único puente hacia la siguiente lección (verbo en imperativo
con objeto visible: abre, anota, lista, calcula, publica). No resumas lo que acaba de leer.

Objetivos formales, prerrequisitos, glosario, FAQ y fuentes fechadas viven en el nivel del
itinerario, una vez; no entran en la lección.

## Párrafo, frase, ritmo

- Párrafo con una idea, de {paragrafo_min} a {paragrafo_max} palabras, en 2 a 4 frases. Ni
  párrafos de una línea apilados, ni bloques de diez líneas.
- Frase de hasta 28 palabras, en orden directo la mayor parte de las veces. El tamaño viene del
  sentido: causa y salvedad juntas piden frase mayor; el giro pide frase corta. Nunca alternes
  corta y larga por programa.
- Verbo con sujeto y voz activa. "Optimizar la captación" se vuelve "captar mejor".
- Cuando la frase habla de una falla, el sujeto es el proceso o el artefacto, nunca el alumno:
  "el recordatorio no salió", no "olvidaste enviarlo".
- La prosa lleva el razonamiento; la lista lleva ítems paralelos; la tabla lleva comparación.
  Una lista cuyos ítems tienen causa y consecuencia entre sí se vuelve prosa.

## Apoyo visual (techo, no piso)

Hasta {figuras_max} apoyos visuales en la lección, y solo cuando sustituyen texto: tabla para
comparar dos o más opciones en dos o más criterios (opciones en columnas, criterios en filas);
lista numerada para un proceso donde el orden importa (un verbo por paso, resultado observable
en el mismo ítem); imagen con leyenda que afirma lo que muestra la figura, entre corchetes,
nunca vacía. Una lección sin apoyo visual pasa; una pieza decorativa, no. Cita en bloque,
negrita y bloque de código no cuentan como apoyo visual y no tienen cuota.

Marcado que reconoce el conversor: tabla con fila de encabezado, fila separadora y el mismo
número de celdas en todas las filas, una línea de texto por fila de la tabla; lista numerada
que empieza en 1; imagen en el formato `![leyenda que afirma un hecho](archivo.svg)`.

## Lo que nunca entra

- Antítesis que niega para afirmar ("no es X, es Y", "no se trata de X", "más que X, Y").
- Tríada como ritmo (tres adjetivos, tres ejemplos, tres beneficios por costumbre).
- Conectivo de relleno abriendo párrafo: "en ese sentido", "cabe destacar", "dicho esto", "en
  suma". "Porque", "por eso", "pero", "además" son libres.
- Adjetivo vacío (robusto, crucial, estratégico, innovador, poderoso): cámbialo por el dato.
- Atribución vaga ("los expertos señalan", "los estudios muestran"): nombra la fuente o corta.
- Escasez fabricada e invitación vacía ("cupos limitados", "no te lo pierdas", "saber más").
- Cliché de máquina ("hoy en día", "la buena noticia es", "sumerjámonos", "ahí es donde entra").
  La lista completa está en el léxico de la fuente de estilo y el gate la rechaza.
- Metadiscurso de verificación ("verificamos que", "fuentes consultadas"), alerta rotulada
  ("Atención:", "Importante:"), rótulo de confianza sobre el propio dato.
- Raya en prosa, mayúsculas de título, coma antes de "y" en enumeración simple, futuro con
  gerundio.
- Dato con la fuente dentro de la frase de lectura. El número entra limpio; la fuente va a la
  lista de fuentes del itinerario.

## Antes de entregar, comprueba

1. La primera frase dice qué va a poder hacer el alumno.
2. Una sola idea, explicada hasta el final; el ejemplo es uno y va de principio a fin, con
   número.
3. {h2_min} a {h2_max} H2; H3 solo en H2 largo; ningún H4.
4. Extensión entre {palavras_alvo_min} y {palavras_alvo_max} palabras; ejercicio entre un
   cuarto y un tercio de ellas.
5. Ejercicio con título, pasos numerados con dato real del alumno, resultado esperado y
   consejo.
6. Ningún número sin origen en la investigación; como máximo 3 marcadores `[FALTA EVIDENCIA]`.
7. Párrafos de {paragrafo_min} a {paragrafo_max} palabras; frases hasta 28.
8. Hasta {figuras_max} apoyos visuales, todos sustituyendo texto.
9. Nada de la lista "Lo que nunca entra".
10. Cierre por el ejemplo, con un puente hacia la siguiente lección.
11. Acentuación completa en todas las palabras.

Empieza directo por la apertura de la lección, sin encabezado de lección (el pipeline lo
inserta), sin título de módulo y sin comentario sobre este prompt.

--- DATOS DE LA INVESTIGACIÓN ---
{context}
