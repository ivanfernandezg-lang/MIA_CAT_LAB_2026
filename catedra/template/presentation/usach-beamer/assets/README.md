# Imagotipo

Archivos **oficiales** copiados desde el ZIP de imagotipos de
https://guiaweb.usach.cl/normas-gr%C3%A1ficas (MNG 2024-2S):

| Archivo        | Uso                                                                  |
| -------------- | -------------------------------------------------------------------- |
| `Usach S1.png` | Horizontal **positivo** (fondo claro) — por defecto del tema         |
| `Usach SB.png` | Horizontal **negativo/blanco** (fondo oscuro) — por defecto del tema |
| `Usach P2.png` | Vertical positivo (alternativa, prioritaria según MNG)               |
| `Usach PB.png` | Vertical negativo/blanco (alternativa)                               |

`usach-horizontal.png` y `usach-horizontal-blanco.png` son las extracciones
bajas originales; quedan solo como respaldo histórico.

Para cambiar la versión, apuntar en `main.tex`:

    \usachimagotipo{assets/Usach P2.png}          % fondo claro
    \usachimagotipoblanco{assets/Usach PB.png}    % fondo oscuro

No editar, recolorear ni recomponer el imagotipo: el MNG lo declara indivisible.
