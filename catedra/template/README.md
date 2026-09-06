# Plantillas y normas gráficas USACH

Recursos oficiales de imagen institucional descargados desde la
[Guía Web USACH](https://guiaweb.usach.cl/normas-gr%C3%A1ficas) (2026-09-06).

## Estructura

| Carpeta / archivo | Contenido |
| ----------------- | --------- |
| `standards/MNG 2024 2S[M1].pdf` | Manual de Normas Gráficas oficial (16 págs.) |
| `standards/Guía para el formato de trabajo de titulación.pdf` | Guía de formato de trabajos de titulación (Bibliotecas USACH) |
| `standards/imagotipos-principales/` | Set principal extraído: `Usach P1.png`, `Usach P2.png`, `Usach PB.png` (blanco), `Usach PN.png` (negro) |
| `standards/imagotipos-secundarios/` | Set secundario (versiones horizontales y variantes) |
| `standards/imagotipos-av/` | Set para audiovisual |
| `presentation/` | Plantillas PPT oficiales 16:9 (`Plantilla PPT 16-9 A/B.pptx`) |
| `report/` | Plantillas Word oficiales (`Hoja-Carta-2023.docx`, `Hoja-Oficio-2023.docx`) |
| `links` | Lista de URLs de todos los recursos |
| `analizar_plantillas.py` | Script de análisis de los recursos |

> Las "SVG" (`PALETA DE COLORES 2023F.svg`, `Imagotipos USACH 2023.svg`)
> descargadas son visores HTML del sitio; los colores oficiales están en el MNG
> y los logos en los ZIP.

## Normas clave (resumen del MNG 2024-2S)

### Colores institucionales

| Color | HEX | Pantone | Uso sugerido |
| ----- | --- | ------- | ------------ |
| Rojo | `#C8102E` | 186 C | Principal: acentos, reglas, plecas |
| Gris oscuro | `#394049` | 432 C | Títulos y textos sobre blanco |
| Amarillo | `#EAAA00` | 124 C | PEI 2030 (acentos secundarios) |
| Púrpura | `#8C4799` | 258 C | PEI 2030 |
| Azul | `#498BCA` | 279 C | PEI 2030 / enlaces |
| Verde azulado | `#00A499` | 3272 C | PEI 2030 |
| Naranjo | `#E77500` | 716 C | PEI 2030 |

Contraste mínimo (WCAG AA): **4,5:1** texto normal, **3:1** texto grande.

### Tipografía

- **Titulares / imagotipo**: Bebas Neue Pro (Expanded ExtraBold).
- **Cuerpos de texto**: Nunito Sans, Atkinson Hyperlegible o Helvetica Neue LT.
- Portada de tesis (exento 02968/2008): Arial negrita 14 (universidad) / 12 (facultad).

### Imagotipo (uso correcto)

- Versión **vertical = prioridad**; horizontal = secundaria.
- Solo relleno/vacío + contratipos; **no** sombras, degradados, inclinación,
  estiramiento ni bajo contraste.
- Márgenes de seguridad: 1 carácter de la sigla (mín. 30 mm en impresos).
- Elementos indivisibles (blasón + USACH + pleca).

## Plan de adecuación del informe LaTeX (T1)

1. **Escudo**: reemplazar la imagen extraída del docx por `Usach P1.png`
   (imagotipo vertical principal) a ≥ 3 cm de ancho, centrado, sin efectos.
2. **Colores LaTeX**: definir `usachred (#C8102E)` y `usachgray (#394049)`:
   - Regla bajo `\section` y línea de la portada en rojo institucional.
   - Títulos de sección en gris oscuro (contraste 4,5:1 sobre blanco ✔).
   - Enlaces/hipervínculos en azul institucional `#498BCA` en vez del azul
     por defecto.
3. **Portada**: alinearla a la guía de titulación:
   - Título **sin** MAYÚSCULAS COMPLETAS (solo iniciales, nombres propios y
     siglas) y sin comillas.
   - Autores con nombres y apellidos completos, **orden alfabético por primer
     apellido** (ya se cumple: Ahumada, Fernández, Fernández, Figueroa).
4. **Tipografía**: el curso exige "Times New Roman o equivalente" (12 pt,
   interlineado 1,5) → mantener **TeX Gyre Termes** en el cuerpo; opcional:
   títulos en **Helvetica/Arial** (sans institucional) para acercarse a la
   imagen corporativa.
5. **Presentación** (cuando se haga): partir desde `Plantilla PPT 16-9 A.pptx`
   oficial o replicar sus elementos en Beamer con la paleta oficial.
6. **Documentos Word** (cartas/oficios): usar `Hoja-Carta/Oficio-2023.docx`.
