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

La lección enseña UNA idea hasta el final y es LECTURA: el alumno termina sabiendo qué cambia
en su negocio y cuál es el próximo paso, dicho en prosa. Extensión: de {palavras_alvo_min} a {palavras_alvo_max} palabras.
Por debajo de {palavras_piso} la idea quedó sin explicar; por encima de {palavras_aviso} entró
una segunda idea, que pertenece a otra lección.

Encabezados: **{h2_min} a {h2_max} H2**, y lo normal son dos, uno por bloque. H3 solo cuando
un H2 pasa de 350 palabras y necesita dos partes (como máximo {h3_por_h2} por H2). Nada de H4,
nada de línea terminada en dos puntos como subtítulo.

**Apertura, en este orden exacto, sin nada en medio (regla R1).** El pipeline inserta el título
(H1). Tú empiezas por el **subtítulo: UNA frase, en línea propia, de hasta 25 palabras**, que
dice qué va a poder hacer el alumno al terminar. Después de una línea en blanco, **dos o tres
párrafos de apertura**, directos al punto: el problema que vive hoy, qué cuesta no resolverlo y
qué cambia al terminar la lección. El primer elemento después del subtítulo es siempre un
párrafo. Sin escena, sin hora del día, sin personaje, sin "en este módulo", sin lista de
objetivos, sin "qué vas a aprender", sin "para quién es", sin índice, sin botón, sin tarjeta,
sin tabla antes del primer párrafo.

**H2 1: por qué [la idea] cambia tu resultado.** Explica la idea en prosa corrida, sin
viñetas: de dónde viene (quién la formuló y qué problema resolvía), qué cuesta no saberla en su
operación (con número cuando la investigación lo tenga), qué cambia cuando la aplica
(comportamiento observable, antes y después) y el error más común de quien la ignora, marcado
como **Trampa común:**. Empieza por el problema y llega a la idea; nunca abras con "la
definición de X es". Una analogía del día a día del ramo del alumno ayuda; dos, si la
segunda explica lo que la primera no explicó.

**H2 2: un caso de tu rubro, de principio a fin.** UN ejemplo del rubro del alumno, contado
entero: quién es, qué estaba pasando, qué hizo la persona paso a paso, qué pasó después, con
número. Medio ejemplo no sirve; tres ejemplos cortos tampoco. El encabezado nombra el caso
("Cómo el taller de Sergio dejó de perder presupuestos"); nunca "cómo queda en tu negocio",
"aplícalo en tu negocio" ni "mockup".

**Cierre, sin encabezado, en 3 a 5 líneas.** Qué cambió en su negocio después de esta lección,
dicho por el ejemplo del H2 2, y un único puente hacia la siguiente lección (verbo en imperativo
con objeto visible: abre, anota, lista, calcula, publica). No resumas lo que acaba de leer.

Objetivos formales, prerrequisitos, glosario, FAQ y fuentes fechadas viven en el nivel del
itinerario, una vez; no entran en la lección.

## Apertura y distracción (R1 a R9): lo que la lección NUNCA lleva

Pedido del dueño, 08/09/2026: el inicio cargado dispersa al lector y la tarjeta en el medio
compite con la lectura. El gate rechaza cada ítem de abajo y la página no se publica con él.

- R1. Cualquier cosa entre el título, el subtítulo y el primer párrafo.
- R2. Botón, invitación o llamada a la acción antes del cuerpo. Si hay, es una sola, al final.
- R3. Recorrido alternativo: "elige tu camino", "si eres X ve a Y", "empieza por aquí", pestañas
  por perfil. Un solo camino, lineal.
- R4. Segunda descripción, lead o resumen repetido arriba.
- R5. Bloque "mockup en tu negocio" y variantes ("en tu negocio", "aplícalo en tu negocio",
  "simula", "maqueta") como sección o rótulo.
- R6. Ejercicio: "hazlo ahora", "ejercicio", "manos a la obra", "tu turno", "practica", "tarea",
  "desafío", "checklist de acción", "Resultado esperado:", "Si te trabas:". La lección es
  lectura, no cuaderno de ejercicios. El próximo paso va en prosa, en el cierre.
- R7. Fuente en medio de la lección: línea "Fuente:", encabezado "Fuentes", cita en tarjeta o
  callout. La fuente va al bloque "Fuentes" del final del itinerario, una línea corta por fuente.
- R8. Tarjeta "checkpoint", "recapitulando", "resumen del capítulo", "aprendiste", "quiz".
- R9. Marcador visible de verificación ("requiere verificación", "a verificar", "[verificar]",
  "dato no confirmado", "fuente pendiente") y CUALQUIER mención a la ley de protección de datos
  por su nombre (LGPD, Lei 13.709), incluso entre comillas. La verificación es bastidor; la
  protección de datos entra como conducta práctica.

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

## Libertad de forma

El molde de arriba fija lo que la lección necesita tener, no cómo decirlo. Analogía del día a
día del ramo del alumno, escena de dos frases dentro del H2 2, contraste entre la forma antigua
y la nueva, la pregunta que él haría en voz alta, humor ligero, primera persona cuando habla la
empresa: usa lo que acorte el camino hasta que él lo haga. Dos lecciones del mismo curso pueden
tener ritmo distinto. Lo que reprueba es el vicio (cliché, escasez fabricada, culpa al alumno),
nunca la figura.

## Lo que nunca entra

- Bastidor: cualquier frase sobre la propia lección, la regla que seguiste, la verificación que
  hiciste o el método de la estimación ("esta lección fue", "los datos fueron verificados",
  "según nuestra metodología", "estimación calculada", "nota del revisor"). El alumno recibe el
  hecho y el paso.
- Rótulo de la investigación ([Alta], [Media], [Baja], "nivel de confianza"): te sirve para
  elegir el dato; en la lección el número entra limpio o no entra.
- Aviso legal genérico ("consulte a un abogado", "conforme a la legislación vigente", "exención
  de responsabilidad"). La ley entra solo cuando cambia la decisión del alumno, y entra con
  número: qué ley, qué artículo, qué plazo, qué valor. Excepción fija (R9): la ley de protección
  de datos no se nombra de ninguna forma; la conducta entra, el nombre de la ley no.

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

1. La primera línea es el subtítulo: una sola frase, que dice qué va a poder hacer el alumno.
2. Justo después del subtítulo viene un párrafo, y después uno o dos más, antes del primer H2.
3. Una sola idea, explicada hasta el final; el ejemplo es uno y va de principio a fin, con
   número.
4. {h2_min} a {h2_max} H2; H3 solo en H2 largo; ningún H4.
5. Extensión entre {palavras_alvo_min} y {palavras_alvo_max} palabras.
6. Ningún ejercicio, checkpoint, mockup, "requiere verificación" ni ley de datos por su nombre (R1 a R9).
7. Ninguna línea "Fuente:" y ningún encabezado "Fuentes" dentro de la lección.
8. Ningún número sin origen en la investigación; como máximo 3 marcadores `[FALTA EVIDENCIA]`.
9. Párrafos de {paragrafo_min} a {paragrafo_max} palabras; frases hasta 28.
10. Hasta {figuras_max} apoyos visuales, todos sustituyendo texto.
11. Nada de la lista "Lo que nunca entra".
12. Cierre por el ejemplo, con un puente hacia la siguiente lección.
13. Acentuación completa en todas las palabras.

Empieza directo por el subtítulo de la lección, sin encabezado de lección (el pipeline lo
inserta), sin título de módulo y sin comentario sobre este prompt.

--- DATOS DE LA INVESTIGACIÓN ---
{context}
