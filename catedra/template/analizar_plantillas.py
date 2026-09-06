"""Analiza los recursos descargados de las normas gráficas USACH.

Imprime: colores/tipografías del tema PPT oficial, inventario de imagotipos,
y reglas de formato de la guía de titulación.
"""
import re
import zipfile

from pypdf import PdfReader

PPTX = "catedra/template/presentation/Plantilla PPT 16-9 A.pptx"
with zipfile.ZipFile(PPTX) as z:
    xml = z.read("ppt/theme/theme1.xml").decode("utf-8")
cols = re.findall(r'<a:srgbClr val="([0-9A-Fa-f]{6})"/>', xml)
fonts = re.findall(r'typeface="([^"]+)"', xml)
print("Colores tema PPT oficial:", [c.upper() for c in cols])
print("Tipografías PPT:", sorted(set(fonts))[:15])

print("\n--- Guía de titulación (primeras páginas) ---")
r = PdfReader("catedra/template/standards/Guía para el formato de trabajo de titulación.pdf")
for i in range(min(4, len(r.pages))):
    t = (r.pages[i].extract_text() or "")[:900]
    if t.strip():
        print(f"=== PAG {i+1} ===")
        print(t)
