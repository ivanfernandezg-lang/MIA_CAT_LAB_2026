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

## Siguientes pasos

1. Subir el listado oficial de grupos de cátedra (para completar la tabla del grupo).
2. Subir `Ejemplos de Proyectos…` y `Modelos de Documentos Comité de Ética USACH/`.
3. Poblar unidades 03–05 en las semanas 7, 9 y 13.
4. Crear `T2/`–`T4/` al subir los enunciados y copiar los scripts de `utilidades/` desde el repo de laboratorio.
