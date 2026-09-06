# tareas — Entregas de cátedra

Una subcarpeta `T<n>/` por trabajo evaluado.

## Trabajos planificados

| Carpeta | Trabajo                              | Peso |
| ------- | ------------------------------------ | ---- |
| `T1/`   | Ética: seres humanos + fraude/plagio | 15 % |
| `T2/`   | Mini Review                          | 25 % |
| `T3/`   | Métodos cuantitativos                | 30 % |
| `T4/`   | Métodos cualitativos                 | 30 % |

> `T1/` ya está creada con la estructura base; `T2/`–`T4/` se crean al subir
> los enunciados correspondientes.

## Estructura de cada entrega

```
T<n>/
├── data/           — datos crudos (solo lectura)
├── enunciado/      — enunciado de la tarea (solo lectura)
├── script/         — scripts autocontenidos
├── results/        — todo lo generado/procesado
├── presentation/   — diapositivas de la presentación
└── report/
    └── tex/        — informe LaTeX (compilar en `report/tex/build/`)
```

## Convención

- `data/` y `enunciado/` solo lectura; lo procesado va a `results/`.
- Scripts autocontenidos, sin rutas absolutas: `python script/x.py` desde la carpeta.
- LaTeX compilado **siempre** en `report/tex/build/` (ignorado en Git).
