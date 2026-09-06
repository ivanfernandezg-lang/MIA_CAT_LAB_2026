# T1 — Ejemplo: procesamiento de una encuesta

Plantilla de referencia del flujo completo de una tarea. Úsala como base:
copiar esta carpeta con el nombre de la tarea real y reemplazar los archivos
de ejemplo.

## Estructura

- `datos/encuesta.csv` — datos crudos (**solo lectura**)
- `scripts/procesar_encuesta.py` — lee los datos y calcula estadísticas
- `resultados/` — tablas generadas por el script (`resumen.csv`, `frecuencia_por_genero.csv`)
- `tex/main.tex` — informe LaTeX

## Reproducir

```powershell
# 1) Procesar los datos (desde esta carpeta)
python scripts/procesar_encuesta.py

# 2) Compilar el informe (desde tex/)
cd tex
pdflatex -output-directory=build main.tex
```

## Para la tarea real

1. Copiar esta carpeta como `tareas/T<numero>-<tema>/`.
2. Reemplazar `datos/` con los archivos reales.
3. Adaptar `scripts/procesar_encuesta.py` (o crear un script nuevo).
4. Editar `tex/main.tex` con título, nombre y contenido real.
5. Anotar el avance en `.copilot/memoria/progreso-estudiante.md`.
