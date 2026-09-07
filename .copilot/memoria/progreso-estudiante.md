# Progreso — Cátedra MIA 2026

## 2026-09-06 — Seteo del repositorio de cátedra

- Creada la estructura de carpetas `catedra/` (espejo del repo de laboratorio).
- `README.md` raíz adaptado a cátedra (trabajos T1–T4, grupo, calendario).
- Creada `.copilot/memoria/` con `inventario-material.md`, `progreso-estudiante.md` y `conceptos-clave.md`.
- Completado `.gitignore` (sección LaTeX) y creado `.venv/` con `openpyxl`, `pypdf` y `pdfplumber`.
- Estructura verificada: `catedra/{informacion-usach, material, proyecto, tareas, utilidades}` + `.gitkeep` en carpetas vacías.

## 2026-09-06 — Reordenamiento del estudiante

- `proyecto/` movido de `catedra/informacion-usach/` a la raíz de `catedra/`.
- Eliminado `Proyecto Laboratorio/` (Enunciado, Grupos…, Orientaciones…) de `informacion-usach/`.
- READMEs y memoria actualizados para reflejar el nuevo orden.

## 2026-09-06 — Procesamiento de los archivos subidos

- Revisado y repartido el material oficial en `catedra/` (detalle en `inventario-material.md`).
- Calendario oficial extraído del `Clase a Clase` (17 semanas; receso 14-9; feriado 31-10; entrega final 7-12) y volcado al `README.md`.
- Detectados 5 grupos de cátedra en la inscripción de la Actividad 2; el grupo propio queda por confirmar.
- `README.md` actualizado con calendario real y organización final de carpetas.

## 2026-09-06 — Nueva estructura de tareas

- `T1-ejemplo-procesamiento/` reemplazado por `T1/` con estructura base: `data/`, `enunciado/`, `script/`, `results/`, `presentation/` y `report/tex/`.
- Convención de entregas actualizada en `catedra/tareas/README.md`, `catedra/README.md` y `README.md` raíz.

## 2026-09-06 — Informe Actividad 1 a LaTeX

- Convertido `data/docs/Informe_Actividad_1_Etica_Investigacion.docx` → `report/tex/main.tex` con `script/docx2tex.py` (solo stdlib).
- Estructura generada: portada + 6 secciones + 4 tablas (tabularx/booktabs) + listas; babel español con `es-noquoting`, `xurl` para URLs.
- Compilado en `report/tex/build/` (15 págs., sin errores).
- **Actualización del docx detectada** (2026-09-06): el `.docx` ahora incluye el escudo USACH en la portada (`report/tex/img/image1.png`) y la tabla de tortured phrases ampliada a 7 filas.
- Convertidor mejorado: extrae imágenes incrustadas, respeta numeración decimal continua (enumitem `series/resume`, ítems 1–29) y anida viñetas por nivel (`ilvl`).
- **Rediseño profesional aplicado** (sin tocar las reglas del curso: 12 pt, interlineado 1,5, márgenes 2,5 cm):
  - Tipografía **TeX Gyre Termes** (equivalente Times New Roman) + microtype.
  - Títulos con `titlesec` (bold + regla bajo `\section`), encabezado/pie con `fancyhdr` ("Página X de Y").
  - Las 4 tablas ahora llevan caption estilo APA ("Tabla N.") sobre la tabla; filas de título convertidas en captions.
  - Bibliografía general con **biblatex + estilo IEEE + biber** (`referencias.bib`, 12 referencias numeradas [1]–[12]); compilar con latexmk o pdflatex → biber → pdflatex ×2.
  - **Fuentes por caso + bibliografía general**: las subsecciones 2.9 y 3.9 muestran sus 5 fuentes cada una en IEEE vía `\fullcite` (desde la misma `referencias.bib`, sin duplicar texto), y la bibliografía general conserva las 12 entradas numeradas `[1]`–`[12]`. Mapeo por caso en `CASE_REFS` de `docx2tex.py`.
  - Enunciado oficial T1: `tareas/T1/enunciado/enunciado-email-t1.md` (email del profe): alcance = autoría, FFP y QRP (seres humanos/vivos quedan para la siguiente actividad, miércoles 30/9).

## 2026-09-06 — Confirmaciones del estudiante

- T1 = **Actividad 1 (Ética, parte 1)** de la plataforma ✔.
- **Grupo propio de cátedra: Grupo 1** ✔ (README y memoria actualizados).
- **Integrantes del Grupo 1** (listado oficial): Gonzalo Ahumada Figueroa, Diego Fernández Carrasco, Iván Fernández Gracia y Pablo Figueroa Zelaya. Coinciden con los autores del informe ✔.
- Listado completo (15 estudiantes, 4 grupos) guardado en `catedra/informacion-usach/Grupos Cátedra 2026 - listado oficial.md`.
- Copiado el enunciado oficial de la plataforma a `tareas/T1/enunciado/` (la tarea queda autocontenida).
  - Verificado en los documentos del curso: el programa usa APA en su bibliografía; los enunciados no imponen formato propio al informe.
  - Índice automático agregado (`\tableofcontents` + `tocloft`, título «Índice», puntos guía, secciones en negrita).
  - Ítems de listas con **etiqueta en negrita** vía comando propio de 3 argumentos `\itemlabel{Etiqueta}{:}{Resto}` (57 ítems generados automáticamente; no aplica a ítems tipo referencia, que llevan punto en la etiqueta).

## 2026-09-06 — Fix LaTeX Workshop (archivos fuera de build/)

- VS Code auto-compiló `main.tex` en la carpeta fuente con LaTeX Workshop, dejando auxiliares sueltos en `report/tex/`. Limpiados.
- Creada `.vscode/settings.json` con `latex-workshop.latex.outDir: %DIR%/build` y receta `latexmk` (`-outdir=build`, biber automático). Verificado: `tex/` queda limpio y todo cae en `build/`.

## 2026-09-06 — Ajuste QRP y decisión de presentación

- Introducción del informe: agregada mención explícita de **QRP** (prácticas de investigación cuestionables) junto a autoría y FFP, vía `TEXT_TWEAKS` en `docx2tex.py` (sin tocar el Word). `main.tex` regenerado y compilado ✔.
- **Presentación NO se hará** (decisión del estudiante): `T1/presentation/` queda vacía por ahora.

## 2026-09-06 — Normas gráficas USACH descargadas y analizadas

- Descargados a `catedra/template/`: MNG 2024-2S (PDF), guía de titulación (PDF), sets de imagotipos (principales/secundarios/AV, ZIP extraídos), plantillas PPT 16:9 A/B y hojas carta/oficio Word.
- Colores oficiales: rojo `#C8102E` (P186C) + gris `#394049` (P432C) principales; PEI 2030: `#EAAA00`, `#8C4799`, `#498BCA`, `#00A499`, `#E77500`.
- Tipografías: Bebas Neue (titulares), Nunito Sans / Atkinson Hyperlegible / Helvetica (cuerpos); contraste WCAG AA 4,5:1.
- Resumen y plan de adecuación LaTeX en `catedra/template/README.md` (pendiente de aprobación del estudiante para aplicarlo a `main.tex`).

## 2026-09-06 — Normas gráficas USACH aplicadas al informe

- **Escudo**: el imagotipo oficial `Usach P1.png` (vertical principal) reemplaza al escudo del docx en la portada (3,5 cm, ≥ 30 mm de margen según norma). Se copia a `report/tex/img/escudo-usach.png` en cada conversión.
- **Colores** (`docx2tex.py`): `usachred #C8102E`, `usachgreen #00A499`, `usachgray #394049`, `usachblue #498BCA`. Títulos de sección en sans + gris; reglas de sección, línea de portada y encabezado en **verde azulado `#00A499`** (a juego con el imagotipo); enlaces azul institucional.
- **Portada**: título principal ahora en _title case_ («Informe de Evaluación: Unidad de Ética en Investigación (Parte 1)») según la guía de titulación; autores ya en orden alfabético por apellido.
- Compilado sin errores (14 págs.).

## 2026-09-06 — Plantilla Beamer USACH (normas gráficas)

- Creada `catedra/template/presentation/usach/` con `main.tex` (plantilla general para todas las tareas) + `README.md` + `img/` (imagotipos oficiales color/blanco/negro).
- Diseño fiel al MNG 2024-2S y a la PPT oficial: banda gris `#394049` con imagotipo blanco en el pie, títulos grises con regla verde `#00A499`, bloques con paleta oficial, portadillas por sección, contraste WCAG AA.
- Compilada y verificada (12 diapositivas de ejemplo, latexmk en `build/`).

## 2026-09-06 — Tema Beamer usach-beamer (del estudiante) + imagotipos oficiales

- El estudiante subió un tema Beamer propio en capas (`beamertheme/color/font/inner/outerthemeusach.sty`) con la "pleca" como único elemento estructural, paleta MNG + derivados WCAG, cadenas de tipografía por motor y componentes (`\usachportada`, `\usachdestacado`, `\usachcierre`, `\usachdato`, etc.).
- Se retiró la plantilla anterior `presentation/usach/`.
- Imagotipos **oficiales** copiados a `usach-beamer/assets/` y cableados: horizontal `Usach S1.png` (positivo) / `Usach SB.png` (negativo) por defecto; verticales `Usach P2.png` / `Usach PB.png` como alternativa.
- `main.tex` y `galeria.tex` compilados y verificados (14 y 32 págs. respectivamente).

## 2026-09-06 — Presentación T1 convertida a Beamer (PPTX → tema usach-beamer)

- Convertida la presentación de la T1 (Ética) a `presentation/main.tex` con el tema `usach-beamer` (19 láminas): portada, 4 secciones, filas de cifras (`\usachdatos`), tablas con `\usachcab`/`\usachfuente`, notas `\note{}` con el guion del PPTX y cierre `\usachcierre`.
- QA visual iterativo (renders con pymupdf): corregidos solapes en filas de cifras (Schön a 22 pt, descriptor corto; ACM a 19 pt con `$500–3.000`), `\raggedright` + `\hyphenpenalty=10000` en minipages.
- **Versión minimalista** `presentation/main-minimalista.tex` (19 láminas, compila con latexmk): menos texto, viñetas con **iconos FontAwesome v4 en colores institucionales** (`fontawesome.sty`, pdflatex), datos destacados con icono (`\usachdatoi`), portadillas de sección con icono y agenda con iconos por sección (template `section in toc` redefinido). QA visual completo de las 19 láminas ✔.
- **Lección clave del tema**: `beamerthemeusach.sty` hace `\AtBeginSection[]{\usachpaginaseccion}` → la portadilla de sección es AUTOMÁTICA. NO agregar portadillas manuales (se duplican). Para personalizarla: `\renewcommand{\usachpaginaseccion}{...}` en el preámbulo.
- Los `.sty` del tema están copiados en `presentation/`; iconos FA v4 disponibles: `\faFlask`, `\faCopy`, `\faDatabase`, `\faTrophy`, `\faIndustry`, `\faBalanceScale`, etc.

## Siguientes pasos

1. Subir el listado oficial de grupos de cátedra (para completar la tabla del grupo).
2. Subir `Ejemplos de Proyectos…` y `Modelos de Documentos Comité de Ética USACH/`.
3. Poblar unidades 03–05 en las semanas 7, 9 y 13.
4. Crear `T2/`–`T4/` al subir los enunciados y copiar los scripts de `utilidades/` desde el repo de laboratorio.
