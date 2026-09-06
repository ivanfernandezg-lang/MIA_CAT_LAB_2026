"""Inspecciona la estructura de un .docx: párrafos, estilos, listas y tablas.

Uso: python script/inspeccionar_docx.py <ruta.docx>
"""
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
}


def qn(tag: str) -> str:
    return f"{{{NS['w']}}}{tag}"


def get_text(el):
    return "".join(t.text or "" for t in el.iter(qn("t")))


def main(path):
    with zipfile.ZipFile(path) as z:
        doc = z.read("word/document.xml")
    root = ET.fromstring(doc)
    body = root.find(qn("body"))
    for child in body:
        tag = child.tag.split("}")[-1]
        if tag == "p":
            style = ""
            ppr = child.find(qn("pPr"))
            if ppr is not None:
                ps = ppr.find(qn("pStyle"))
                if ps is not None:
                    style = ps.get(qn("val"))
                numpr = ppr.find(qn("numPr"))
                numid = ""
                ilvl = ""
                if numpr is not None:
                    ni = numpr.find(qn("numId"))
                    il = numpr.find(qn("ilvl"))
                    numid = ni.get(qn("val")) if ni is not None else ""
                    ilvl = il.get(qn("val")) if il is not None else ""
                style += f" numId={numid} ilvl={ilvl}"
            # negrita/cursiva de los runs
            decor = []
            for r in child.iter(qn("r")):
                rpr = r.find(qn("rPr"))
                if rpr is not None:
                    if rpr.find(qn("b")) is not None:
                        decor.append("B")
                    if rpr.find(qn("i")) is not None:
                        decor.append("I")
            print(f"[p:{style}] {'/'.join(sorted(set(decor)))} | {get_text(child)[:120]}")
        elif tag == "tbl":
            rows = child.findall(qn("tr"))
            print(f"[TABLA {len(rows)} filas]")
            for ri, row in enumerate(rows[:5]):
                cells = []
                for tc in row.findall(qn("tc")):
                    cells.append(get_text(tc).replace("\n", " ")[:60])
                print(f"  fila{ri}: {cells}")
        else:
            print(f"[{tag}] {get_text(child)[:80]}")


if __name__ == "__main__":
    main(sys.argv[1])
