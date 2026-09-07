"""Inspecciona un .pptx: diapositivas, textos, tablas, notas y medios."""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P_NS = "{http://schemas.openxmlformats.org/presentationml/2006/main}"


def slide_text(xml: str) -> list:
    root = ET.fromstring(xml)
    out = []
    for sp in root.iter(f"{P_NS}sp"):
        runs = [t.text or "" for t in sp.iter(f"{A_NS}t")]
        txt = "".join(runs).strip()
        if txt:
            out.append(txt)
    return out


def slide_tables(xml: str) -> list:
    root = ET.fromstring(xml)
    out = []
    for tbl in root.iter(f"{A_NS}tbl"):
        for tr in tbl.iter(f"{A_NS}tr"):
            row = []
            for tc in tr.iter(f"{A_NS}tc"):
                cell = " ".join(
                    (t.text or "").strip() for t in tc.iter(f"{A_NS}t")
                )
                row.append(cell.strip())
            if any(row):
                out.append(row)
    return out


def main(path, outfile):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        slides = sorted(
            (n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        notes = sorted(
            (n for n in names if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        media = [n for n in names if n.startswith("ppt/media/")]
        out = [f"SLIDES: {len(slides)} | MEDIOS: {media}"]
        for n in slides:
            xml = z.read(n).decode("utf-8")
            texts = slide_text(xml)
            tables = slide_tables(xml)
            out.append(f"\n=== {n} ===")
            for t in texts:
                out.append("  • " + t)
            for i, row in enumerate(tables):
                out.append("  [tabla] " + " | ".join(row))
        for n in notes:
            xml = z.read(n).decode("utf-8")
            txt = " ".join(
                (t.text or "").strip() for t in ET.fromstring(xml).iter(f"{A_NS}t")
            )
            out.append(f"\n--- notas {n}: {txt}")
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print("OK ->", sys.argv[2])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
