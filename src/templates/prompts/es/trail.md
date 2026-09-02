# Prompt: cierre del itinerario (GPT-5.5)

## Qué es

Un itinerario es un módulo de 4 a 6 lecciones. Las lecciones ya están escritas. Tú escribes
solo lo que vive en el nivel del ITINERARIO, una vez: qué va a poder hacer el alumno, qué
necesita antes, el glosario, las preguntas frecuentes y las fuentes fechadas. Nada de eso entra
en cada lección; entra aquí.

El lector es el dueño de un pequeño negocio, lego en marketing y tecnología, en el celular.
Acentuación completa, sin emoji, sin raya, sin clichés.

## El itinerario

- Curso: {course_name} (nivel {course_level})
- Itinerario {module_number}: {module_title}. {module_description}
- Lecciones, en orden: {lesson_titles}

## Anti-invención (inviolable)

Toda fuente listada tiene que aparecer en el texto de las lecciones o en la investigación de
abajo, con nombre y fecha. La fuente que no esté en ninguno de los dos no entra. Si las
lecciones citan un dato sin fuente, no crees la fuente: deja el dato fuera de la lista.

## Qué escribir, en este orden y con estos encabezados

## Qué vas a poder hacer

De tres a cinco frases, una por línea, cada una empezando por un verbo de acción en
infinitivo (analizar, comparar, calcular, montar, aplicar, elegir, medir, publicar). Nunca
"entender", "conocer", "saber", "aprender". Cada frase nombra un resultado que él puede
comprobar en su propio negocio.

## Antes de empezar

De uno a tres prerrequisitos, en una línea cada uno: qué necesita tener a mano (cuenta, dato,
herramienta) o ya saber. Si el itinerario no depende de nada, escribe una línea diciéndolo.

## Glosario

Los términos técnicos que usan las lecciones, en orden alfabético, cada uno con glosa de hasta
12 palabras y una comparación de su día a día. Formato: `**término**: glosa`. Entre cinco y
doce términos; solo lo que las lecciones de verdad usan.

## Preguntas frecuentes

De tres a seis preguntas que el dueño del negocio haría después de terminar el itinerario,
cada una con respuesta de dos a cuatro frases, directa, sin preámbulo. Pregunta en negrita,
respuesta en prosa justo debajo.

## Fuentes

Una línea por fuente, en el formato `Nombre de la fuente, título o informe, mes y año`, solo
con lo que las lecciones o la investigación traen. De una a ocho fuentes.

## Antes de entregar, comprueba

1. Cinco secciones, en este orden, cada una con el encabezado de arriba como H2.
2. Verbos de acción en los objetivos; ningún "entender" o "conocer".
3. Glosa de hasta 12 palabras por término; ningún término que las lecciones no usen.
4. Ninguna fuente inventada.
5. Frases de hasta 28 palabras; sin raya; acentuación completa.

Empieza directo por el primer H2, sin título de itinerario (el pipeline lo inserta) y sin
comentario sobre este prompt.

--- LECCIONES DEL ITINERARIO ---
{lessons}

--- DATOS DE LA INVESTIGACIÓN ---
{context}
