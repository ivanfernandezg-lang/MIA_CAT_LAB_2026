# Tema Beamer USACH v2.0

Tema institucional para presentaciones académicas de la Universidad de Santiago
de Chile. Arquitectura Beamer estándar (color / font / inner / outer separados),
compila con **pdfLaTeX**, **XeLaTeX** o **LuaLaTeX**.

```
usach-beamer/
├── beamerthemeusach.sty          # tema maestro: opciones + componentes
├── beamercolorthemeusach.sty     # paleta MNG + roles semánticos
├── beamerfontthemeusach.sty      # tipografía y escala modular
├── beamerinnerthemeusach.sty     # portada, portadillas, bloques, listas
├── beamerouterthemeusach.sty     # título de lámina, pie, progreso
├── main.tex                      # plantilla de trabajo (esqueleto de presentación)
├── galeria.tex                   # catálogo de componentes para copiar y pegar
└── assets/                       # imagotipo e imágenes de ejemplo
```

Compilar:

```bash
latexmk -pdf     -outdir=build main.tex     # Nimbus Sans (clon Helvetica)
latexmk -xelatex -outdir=build main.tex     # usa las fuentes corporativas si están instaladas
```

---

## 1. Decisiones de diseño

**El problema del template anterior:** cromo decorativo repetido en cada
lámina (logo + banda + reglas), tipografía por defecto y color usado como
adorno. Resultado: mucha tinta institucional y poca jerarquía.

**El sistema nuevo tiene un solo elemento estructural: la pleca.** Es la barra
vertical que dentro del propio imagotipo separa el blasón del texto
«UNIVERSIDAD DE SANTIAGO DE CHILE». Se reutiliza a la izquierda de todo título
—portada, portadilla, título de lámina, cita— y vive **en el margen**, de modo
que el texto queda siempre a ras de la caja de contenido. No hay más adornos.

| Token       | Valor                | Rol                                                        |
| ----------- | -------------------- | ---------------------------------------------------------- |
| `usachgris` | `#394049` (432 C)    | estructura: texto, superficies oscuras, títulos de bloque  |
| `usachrojo` | `#C8102E` (186 C)    | acento único: pleca, marcador de lista, progreso, alertas  |
| `usachtinta`| `#22272E`            | titulares sobre blanco                                     |
| `usachgris10`| `#F2F4F5`           | fondo de bloque                                            |
| `usachgris70`| `#6B7280`           | metadatos, fuentes, notas                                  |
| PEI 2030    | 5 colores oficiales  | opcional (`pei`), solo datos y gráficos                    |

**Dos superficies, no cinco.** Fondo oscuro (`#2F353D`) para portada,
portadillas, afirmaciones y cierre; blanco para todo el contenido. El rojo
nunca se usa como masa: aparece en reglas de 1,6 pt y marcadores.

**Relieve, no decoración.** Los bloques llevan esquinas de 4 pt y una sombra
corta (0,9 mm de desplazamiento, difusión 0,4 mm, gris institucional al 45 %):
lo justo para separarlos del fondo. El MNG prohíbe sombras y degradados **sobre
el imagotipo**, no sobre los elementos de interfaz; aun así la sombra se
mantiene baja porque en proyección las sombras largas se ven sucias. Con
`bloquesplanos` se vuelve a la versión sin relieve.

**Ritmo.** Margen 0,90 cm; escala tipográfica 1,25 sobre base 11 pt
(21 / 15 / 12,5 / 11 / 9 / 7,5 pt). Medida de línea bajo 80 caracteres a
dos columnas.

**Navegación.** No hay lámina de agenda repetida: la portadilla de cada
sección muestra el índice completo con la sección activa marcada, y el pie
lleva una barra de avance proporcional. El número de lámina va a la derecha,
en negrita, para que sirva en la ronda de preguntas.

---

## 2. Cumplimiento normativo

| Norma (MNG 2024-2S / Guía de titulación)          | Implementación                                                                                 |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Colores institucionales con Pantone de origen      | Declarados en `beamercolorthemeusach.sty`, cada uno con su referencia                            |
| Tipografía: Bebas Neue Pro / Nunito Sans / Helvetica Neue LT | Sustitución por motor (§3). Con XeLaTeX se usan las corporativas si están instaladas   |
| Imagotipo indivisible, sin sombras, degradados ni deformación | Se inserta el archivo oficial sin transformaciones; el escalado es proporcional        |
| Área de resguardo del imagotipo                    | `\usachlogoaire` = 0,45 × alto del imagotipo, aplicada en portada, portadillas y cierre          |
| Versión negativa sobre fondo oscuro                | `\usachimagotipoblanco` para portada/cierre; positiva (`\usachimagotipo`) para fondos claros     |
| Contraste mínimo WCAG AA 4,5:1 / 3:1               | Verificado, tabla abajo                                                                          |
| Fuente obligatoria en figuras y tablas             | `\usachfuente{...}`                                                                              |
| Datos de portada (facultad, departamento, programa)| `\usachfacultad`, `\usachdepartamento`, `\usachprograma`, `\usachasignatura`, `\usachprofesor`   |
| Título sin mayúsculas completas (exento 02968/2008)| La plantilla no aplica `\MakeUppercase` en ningún punto                                          |

Contrastes medidos (WCAG 2.1, sRGB):

| Combinación                          | Ratio    | Uso permitido                       |
| ------------------------------------ | -------- | ----------------------------------- |
| `usachgris` sobre blanco             | 10,48:1  | texto normal ✔                      |
| `usachtinta` sobre blanco            | 15,02:1  | titulares ✔                         |
| `usachrojo` sobre blanco             | 5,88:1   | texto normal ✔                      |
| blanco sobre `usachgris`             | 10,48:1  | texto normal ✔                      |
| `usachgris70` sobre blanco           | 4,83:1   | texto normal ✔ (metadatos ≥ 8,5 pt) |
| blanco sobre fondo oscuro `#2F353D`  | 12,37:1  | texto normal ✔                      |
| `usachgris40` sobre fondo oscuro     | 5,76:1   | etiquetas ✔                         |
| `usachazul` (279 C) sobre blanco     | 3,60:1   | **solo gráfico**                    |
| `usachverde` (3272 C) sobre blanco   | 3,10:1   | **solo gráfico**                    |
| `usachamarillo` (124 C) sobre blanco | 2,05:1   | **nunca texto**; sí como fondo con texto gris (5,12:1) |

Por eso el tema define dos derivados **no institucionales**, usados
exclusivamente donde el color oficial no alcanza 4,5:1 en texto:
`usachazultexto` `#2E6BA8` (5,55:1, enlaces) y `usachverdetexto` `#00776F`
(5,43:1, bloques de ejemplo y citas bibliográficas).

La pleca es **blanca sobre fondo oscuro** y roja sobre blanco: el rojo
institucional solo alcanza 2,1:1 contra el gris de fondo, así que ahí no puede
portar información. Es la misma lógica del imagotipo en negativo.

---

## 3. Tipografía: qué se usa realmente

Ninguna de las tres familias del MNG está en TeX Live. Sustitución automática:

| Motor              | Cuerpo                                                | Titulares                                     |
| ------------------ | ----------------------------------------------------- | --------------------------------------------- |
| pdfLaTeX           | Nimbus Sans (`helvet`), clon métrico de Helvetica      | Nimbus Sans Bold                              |
| XeLaTeX / LuaLaTeX | Nunito Sans → Atkinson Hyperlegible → TeX Gyre Heros   | Bebas Neue Pro → TeX Gyre Heros Cn Bold       |

La cadena de respaldo se resuelve con `\IfFontExistsTF`, así que basta instalar
Nunito Sans y Bebas Neue Pro en el sistema y compilar con XeLaTeX para obtener
la tipografía corporativa exacta, sin tocar el `.tex`.

### Matemática

Por defecto la notación va **serif sobre texto sans**, que es la convención de
los papers: la lámina se lee como interfaz y la fórmula como matemática.

| Motor              | Fuente matemática                                                        |
| ------------------ | ------------------------------------------------------------------------ |
| pdfLaTeX           | Times (`mathptmx`)                                                       |
| XeLaTeX / LuaLaTeX | TeX Gyre Termes Math si está instalada; si no, Latin Modern Math          |

Beamer sustituye la matemática por sans por defecto, así que el tema activa
`\usefonttheme[onlymath]{serif}` en esta modalidad. Con la opción `matesans`
la notación toma la familia del texto vía `mathastext`.

Los espacios de display (`\abovedisplayskip`, `\jot`) se abren a 0,95 em para
que las ecuaciones respiren como en un artículo; la numeración de `equation` y
`align` funciona normalmente.

---

## 4. API

### Opciones

```latex
\usetheme[sinprogreso,logolamina,sinportadillas,pei]{usach}
```

| Opción           | Efecto                                                              |
| ---------------- | ------------------------------------------------------------------- |
| `sinprogreso`    | quita la barra de avance del pie                                    |
| `logolamina`     | repite el imagotipo (2,4 cm) arriba a la derecha en cada lámina     |
| `sinportadillas` | desactiva la portadilla automática al iniciar cada sección          |
| `pei`            | ciclo de colores PEI 2030 para `pgfplots`                           |
| `bloquesplanos`  | bloques sin esquinas redondeadas ni sombra                          |
| `matesans`       | matemática en la misma familia sans del texto (por defecto va serif)|

### Metadatos

```latex
\title[Título corto para el pie]{Título completo}
\subtitle{...}  \author{...}  \date{...}
\usachfacultad{Facultad de Ingeniería}
\usachdepartamento{Departamento de Ingeniería Informática}
\usachprograma{Magíster en Ingeniería Informática}
\usachasignatura{Computación Científica}
\usachprofesor{Prof. ...}
\usachimagotipo{assets/Usach P2.png}        % positivo, fondo claro
\usachimagotipoblanco{assets/Usach PB.png}  % negativo, fondo oscuro
```

### Láminas y componentes

| Macro                       | Qué hace                                                        |
| --------------------------- | --------------------------------------------------------------- |
| `\usachportada`             | portada oscura con imagotipo, pleca y ficha de metadatos         |
| `\usachpaginaseccion`       | portadilla de sección (automática, salvo `sinportadillas`)       |
| `\usachdestacado{texto}`    | lámina de afirmación sobre fondo oscuro                          |
| `\usachcierre[Gracias]{contacto}` | lámina de cierre                                           |
| `\usachdato{8 %}{etiqueta}` | cifra destacada con regla roja                                   |
| `\usachdatos{...}`          | fila de cifras destacadas                                        |
| `\usachcita{texto}{fuente}` | cita textual con pleca gris                                      |
| `\usachfuente{...}`         | atribución bajo figura o tabla                                   |
| `\usachcab{...}`            | celda de cabecera de tabla (texto blanco sobre la fila gris)      |
| `\usachlaminaimagen[opacidad]{archivo}{texto}` | imagen a sangre con velo institucional y texto blanco |
| `usachformula` (entorno)    | panel para la ecuación que sostiene el argumento                 |
| `usachcaja` (entorno)       | caja neutra sin título, misma elevación que los bloques          |
| `\usachpleca[color]{...}`   | primitiva: contenido con pleca a la izquierda                    |
| `\usachaire`                | dentro de `itemize`: separa los ítems 0,55 em                    |
| `\usachlaminaoscura`        | entorno: cualquier `frame` sobre fondo institucional oscuro      |

Bloques: `block` (gris), `alertblock` (rojo), `exampleblock` (verde), todos
planos, sin sombra ni degradado.

### Paquetes que el tema estiliza solo

Si el documento los carga, el tema los configura sin que haya que tocar nada:

| Paquete       | Qué aplica                                                                                     |
| ------------- | ---------------------------------------------------------------------------------------------- |
| `pgfplots`    | estilo `usach` (`\begin{axis}[usach, ...]`): ejes abiertos a la izquierda e inferior, grilla gris, leyenda sin marco, coma decimal y separador de miles. Ciclos `usachciclo` (líneas y marcas) y `usachciclobarras` (barras, con relleno) |
| `listings`    | estilo `usach` aplicado por defecto: pleca roja a la izquierda, fondo gris, palabras clave en rojo, comentarios en gris, numeración de líneas |
| `algorithm2e` | palabras clave en rojo, comentarios en gris, título del algoritmo en la tipografía de titulares  |

Para barras: `\begin{axis}[usach, ybar, cycle list name=usachciclobarras]`.
Para filas alternadas en tablas: `\documentclass[...,xcolor=table]{beamer}` y
`\rowcolors{2}{usachgris10}{white}`.

Cabecera sobre fila gris: `\rowcolor{usachgris}` y cada celda con
`\usachcab{...}`. Importa el detalle: si se escribe `\color{white}Descripción`
dentro de una columna de párrafo (`p`, `X`), el `\color` inicial deja una línea
vacía y hunde esa celda una línea respecto del resto de la cabecera.
`\usachcab` usa `\textcolor`, que no tiene ese efecto.

---

## 5. `galeria.tex`: catálogo de componentes

Segundo documento, con una lámina por cada cosa que se suele necesitar:

- listas de tres niveles, con y sin aire; descripciones; aparición progresiva;
- énfasis, citas, notas al pie, referencias cruzadas;
- los tres bloques y la fila de cifras destacadas;
- tabla `booktabs` de resultados y tabla ancha `tabularx` con filas alternadas
  y encabezado en gris institucional;
- serie de tiempo, barras agrupadas y dispersión en `pgfplots`;
- pseudocódigo en `algorithm2e` y código Python en `listings`;
- ecuaciones en panel (`usachformula`), `align` numerado y `cases`;
- figura con pie y fuente, figura junto a texto, imagen a sangre con velo,
  y diagrama de proceso en TikZ con la paleta institucional;
- referencias, cierre y anexo.

Compilar: `latexmk -pdf -outdir=build galeria.tex`.

---

## 6. Imagotipo

`assets/` trae una versión de trabajo extraída de la plantilla oficial, en
positivo y negativo, para que el proyecto compile de inmediato. **Reemplázala
por los archivos del ZIP oficial** (`Usach P1.png` / `Usach P2.png` para fondo
claro, `Usach PB.png` para fondo oscuro) de
<https://guiaweb.usach.cl/normas-gráficas> antes de presentar: la versión de
trabajo es una extracción a baja resolución.

Si el archivo no existe, el tema **no dibuja un blasón aproximado** —eso sería
alterar la marca—: compone el logotipo tipográfico de respaldo y sigue
adelante.

---

## 7. Limitaciones conocidas

- El MNG fija el tamaño mínimo del imagotipo en 30 mm para impresos; en
  proyección se usa 2,4 cm de ancho (`logolamina`) y ~2,7 cm en portada. Si el
  trabajo se imprime como póster, subir `\usachlogoalto`.
- `mathastext` cambia la familia de la matemática, no los símbolos; si el
  documento usa mucha notación AMS, revisar la salida.
- Sin `babel-spanish` instalado, `main.tex` define `Figura`, `Tabla` y
  `Referencias` a mano.
- Las láminas con `lstlisting` necesitan `\begin{frame}[fragile]`.
- `assets/ejemplo-mapa.png` y `assets/ejemplo-fondo.jpg` son material sintético
  de demostración: bórralos del proyecto real.
