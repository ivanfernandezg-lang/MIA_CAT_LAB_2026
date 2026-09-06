"""T1 — Ejemplo: procesamiento de una encuesta (CSV → resultados).

Flujo demostrado:
    1. Leer datos crudos desde ../datos (SOLO LECTURA).
    2. Calcular estadísticas descriptivas con la biblioteca estándar.
    3. Escribir tablas limpias en ../resultados.

Ejecutar desde la carpeta de la tarea:
    python scripts/procesar_encuesta.py
"""
import csv
import statistics
import sys
from collections import Counter
from pathlib import Path

# Carpeta de la tarea (padre de scripts/)
CARPETA_TAREA = Path(__file__).resolve().parent.parent

# Permite importar los helpers desde utilidades/ (raíz del repo)
sys.path.insert(0, str(CARPETA_TAREA.parent.parent / "utilidades"))
from leer_excel import leer_tabla  # noqa: E402


def main() -> None:
    datos = CARPETA_TAREA / "datos"
    resultados = CARPETA_TAREA / "resultados"
    resultados.mkdir(exist_ok=True)

    # 1) Leer los datos crudos (nunca se modifican)
    filas = leer_tabla(datos / "encuesta.csv")

    # 2) Convertir columnas numéricas (csv.DictReader devuelve texto)
    edades = [int(fila["edad"]) for fila in filas]
    puntajes = [int(fila["puntaje"]) for fila in filas]

    # 3) Estadísticas descriptivas
    resumen = [
        {"metrica": "n_encuestados", "valor": len(filas)},
        {"metrica": "edad_promedio", "valor": round(statistics.mean(edades), 2)},
        {"metrica": "edad_desviacion", "valor": round(statistics.stdev(edades), 2)},
        {"metrica": "puntaje_promedio", "valor": round(statistics.mean(puntajes), 2)},
        {"metrica": "puntaje_desviacion", "valor": round(statistics.stdev(puntajes), 2)},
    ]

    # 4) Frecuencia por género
    conteo_genero = Counter(fila["genero"] for fila in filas)
    tabla_genero = [
        {
            "genero": genero,
            "n": cantidad,
            "porcentaje": round(100 * cantidad / len(filas), 1),
        }
        for genero, cantidad in sorted(conteo_genero.items())
    ]

    # 5) Escribir resultados (tablas limpias para el informe)
    _escribir_csv(resultados / "resumen.csv", resumen)
    _escribir_csv(resultados / "frecuencia_por_genero.csv", tabla_genero)

    print("Resultados generados:")
    for archivo in ("resumen.csv", "frecuencia_por_genero.csv"):
        print(f"  {resultados / archivo}")


def _escribir_csv(ruta: Path, filas: list[dict]) -> None:
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


if __name__ == "__main__":
    main()
