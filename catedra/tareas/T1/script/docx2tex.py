"""Convierte el informe .docx de la Actividad 1 (ética) a LaTeX.

Uso (desde catedra/tareas/T1):
  python script/docx2tex.py data/docs/<archivo>.docx report/tex/main.tex

Solo stdlib (zipfile + ElementTree).
"""
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def qn(tag: str) -> str:
    return f"{{{NS['w']}}}{tag}"


def esc(s: str) -> str:
    s = s.replace("\\", r"\textbackslash{}")
    for ch in "&%$#_{}":
        s = s.replace(ch, "\\" + ch)
    s = s.replace("~", r"\textasciitilde{}")
    s = s.replace("^", r"\textasciicircum{}")
    s = s.replace('"', r"\textquotedbl{}")
    return s


def runs_of(p):
    """Lista de (texto, bold, italic) por run del párrafo."""
    out = []
    for r in p.iter(qn("r")):
        txt = "".join(t.text or "" for t in r.iter(qn("t")))
        if not txt:
            continue
        rpr = r.find(qn("rPr"))
        b = rpr is not None and rpr.find(qn("b")) is not None
        i = rpr is not None and rpr.find(qn("i")) is not None
        out.append((txt, b, i))
    return out


def fmt_runs(runs):
    parts = []
    for txt, b, i in runs:
        t = esc_txt(txt)
        if b and i:
            t = r"\textit{\textbf{" + t + "}}"
        elif b:
            t = r"\textbf{" + t + "}"
        elif i:
            t = r"\textit{" + t + "}"
        parts.append(t)
    return "".join(parts)


def raw_text(p) -> str:
    return "".join(t.text or "" for t in p.iter(qn("t")))


def para_meta(p):
    ppr = p.find(qn("pPr"))
    numid = ""
    ilvl = 0
    if ppr is not None:
        numpr = ppr.find(qn("numPr"))
        if numpr is not None:
            ni = numpr.find(qn("numId"))
            if ni is not None:
                numid = ni.get(qn("val"))
            il = numpr.find(qn("ilvl"))
            if il is not None:
                ilvl = int(il.get(qn("val")))
    bold = any(b for _, b, _ in runs_of(p))
    return numid, ilvl, bold


A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def load_rels(z):
    rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    return {r.get("Id"): r.get("Target") for r in rels}


def numid_formats(z):
    """numId -> formato del nivel 0 (bullet/decimal/...)."""
    n = ET.fromstring(z.read("word/numbering.xml"))
    abs_by_id = {a.get(qn("abstractNumId")): a for a in n.findall(qn("abstractNum"))}
    fmt = {}
    for ni in n.findall(qn("num")):
        num_id = ni.get(qn("numId"))
        ai = ni.find(qn("abstractNumId"))
        if ai is None:
            continue
        abs_el = abs_by_id.get(ai.get(qn("val")))
        if abs_el is None:
            continue
        for lvl in abs_el.findall(qn("lvl")):
            if lvl.get(qn("ilvl")) == "0":
                nf = lvl.find(qn("numFmt"))
                fmt[num_id] = nf.get(qn("val")) if nf is not None else "bullet"
                break
        fmt.setdefault(num_id, "bullet")
    return fmt


def drawing_targets(p, rels):
    """Ids de relación de las imágenes incrustadas en el párrafo."""
    ids = []
    for blip in p.iter(f"{{{A_NS}}}blip"):
        rid = blip.get(f"{{{R_NS}}}embed")
        if rid and rid in rels and rid not in ids:
            ids.append(rid)
    return ids


def extract_images(z, rels, img_dir, used_ids):
    """Copia las imágenes usadas a img_dir; retorna rid -> nombre de archivo."""
    os.makedirs(img_dir, exist_ok=True)
    mapping = {}
    for rid in used_ids:
        target = rels[rid]
        name = os.path.basename(target.replace("\\", "/"))
        data = z.read("word/" + target.lstrip("/"))
        with open(os.path.join(img_dir, name), "wb") as f:
            f.write(data)
        mapping[rid] = name
    return mapping


SEC_RE = re.compile(r"^(\d+(?:\.\d+)*)\.\s+(.*)$")
LET_RE = re.compile(r"^([A-Z])\.\s+(.*)$")
URL_RE = re.compile(r"(https?://[^\s\)\],;\"']+)")


def esc_txt(s: str) -> str:
    """Escapa texto y envuelve URLs en el macro de url (xurl permite quiebres de linea)."""
    out = []
    last = 0
    for m in URL_RE.finditer(s):
        out.append(esc(s[last:m.start()]))
        out.append(r"\url{" + m.group(0) + "}")
        last = m.end()
    out.append(esc(s[last:]))
    return "".join(out)


def cell_latex(tc) -> str:
    parts = []
    for p in tc.findall(qn("p")):
        txt = fmt_runs(runs_of(p))
        if txt.strip():
            parts.append(txt)
    return r"\newline ".join(parts) if parts else ""


def table_latex(tbl) -> str:
    rows = tbl.findall(qn("tr"))
    ncols = max(len(row.findall(qn("tc"))) for row in rows)
    spec = "X" * ncols
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\begin{tabularx}{\linewidth}{" + spec + "}",
        r"\toprule",
    ]
    for ri, row in enumerate(rows):
        cells = []
        for tc in row.findall(qn("tc")):
            c = cell_latex(tc)
            if ri == 0:
                c = r"\textbf{" + c + "}"
            cells.append(c)
        while len(cells) < ncols:
            cells.append("")
        lines.append(" & ".join(cells) + r" \\")
        if ri == 0:
            lines.append(r"\midrule")
    lines += [r"\bottomrule", r"\end{tabularx}", r"\end{table}"]
    return "\n".join(lines)


def render_list(group, formats, dec_state):
    """group: lista de (numid, ilvl, latex). Genera itemize/enumerate anidados."""
    out = []
    stack = []  # tipos de entorno abiertos

    def item_type(numid, ilvl, stack_len):
        if stack_len == 0 and formats.get(numid) == "decimal" and ilvl == 0:
            return "enumerate"
        return "itemize"

    for numid, ilvl, txt in group:
        need = int(ilvl) + 1
        while len(stack) > need:
            out.append(r"\end{" + stack.pop() + "}")
        while len(stack) < need:
            typ = item_type(numid, ilvl, len(stack))
            opts = ""
            if typ == "enumerate":
                if dec_state["first"]:
                    opts = "[series=lista]"
                    dec_state["first"] = False
                else:
                    opts = "[resume*=lista]"
            out.append(r"\begin{" + typ + "}" + opts)
            stack.append(typ)
        if txt.strip():
            out.append(r"\item " + txt)
    while stack:
        out.append(r"\end{" + stack.pop() + "}")
    return out


def convert(docx_path: str, out_path: str):
    with zipfile.ZipFile(docx_path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
        rels = load_rels(z)
        formats = numid_formats(z)
        body = root.find(qn("body"))

        blocks = []
        used_imgs = set()
        for child in body:
            tag = child.tag.split("}")[-1]
            if tag == "p":
                numid, ilvl, bold = para_meta(child)
                imgs = drawing_targets(child, rels)
                used_imgs.update(imgs)
                blocks.append(("p", {
                    "numid": numid, "ilvl": ilvl, "bold": bold,
                    "raw": raw_text(child), "el": child, "imgs": imgs,
                }))
            elif tag == "tbl":
                blocks.append(("tbl", child))

        tex_dir = os.path.dirname(os.path.abspath(out_path))
        img_map = extract_images(z, rels, os.path.join(tex_dir, "img"), used_imgs)

    # Primer párrafo que es un encabezado de sección → fin de la portada
    first_sec = None
    for i, b in enumerate(blocks):
        if b[0] == "p" and SEC_RE.match(b[1]["raw"].strip()):
            first_sec = i
            break
    if first_sec is None:
        first_sec = len(blocks)

    out = []
    out.append(r"\documentclass[12pt,a4paper]{article}")
    out.append(r"\usepackage[utf8]{inputenc}")
    out.append(r"\usepackage[T1]{fontenc}")
    out.append(r"\usepackage[spanish,es-noquoting]{babel}")
    out.append(r"\usepackage[margin=2.5cm]{geometry}")
    out.append(r"\usepackage{setspace}")
    out.append(r"\onehalfspacing")
    out.append(r"\usepackage{booktabs}")
    out.append(r"\usepackage{tabularx}")
    out.append(r"\usepackage{graphicx}")
    out.append(r"\graphicspath{{img/}}")
    out.append(r"\usepackage{enumitem}")
    out.append(r"\usepackage{hyperref}")
    out.append(r"\usepackage{xurl}")
    out.append(r"\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}")
    out.append(r"\setlength{\parindent}{0pt}")
    out.append(r"\setlength{\parskip}{4pt}")
    out.append("")
    out.append(r"\begin{document}")

    # ---- Portada ----
    title_ps = [b[1] for b in blocks[:first_sec] if b[0] == "p"]
    out.append(r"\begin{center}")
    tidx = 0
    for meta in title_ps:
        if meta["imgs"]:
            out.append(r"\includegraphics[width=3cm]{%s}\par" % img_map[meta["imgs"][0]])
            out.append(r"\vspace{12pt}")
            continue
        txt = fmt_runs(runs_of(meta["el"]))
        if not txt.strip():
            continue
        if tidx == 0:
            out.append(r"{\Large\bfseries " + txt + r"}\par")
        elif tidx < 3:
            out.append(r"\vspace{6pt}")
            out.append(r"{\large " + txt + r"}\par")
        elif tidx == 3:
            out.append(r"\vspace{18pt}")
            out.append(r"{\LARGE\bfseries " + txt + r"}\par")
        elif tidx == 4:
            out.append(r"\vspace{8pt}")
            out.append(r"{\large " + txt + r"}\par")
        else:
            out.append(r"\vspace{10pt}")
            out.append(txt + r"\par")
        tidx += 1
    out.append(r"\vspace{14pt}")
    out.append(r"\end{center}")
    out.append(r"\newpage")

    # ---- Cuerpo ----
    body_blocks = blocks[first_sec:]
    dec_state = {"first": True}
    i = 0
    while i < len(body_blocks):
        b = body_blocks[i]
        if b[0] == "tbl":
            out.append(table_latex(b[1]))
            i += 1
            continue
        meta = b[1]
        raw = meta["raw"].strip()
        if meta["imgs"]:
            for rid in meta["imgs"]:
                out.append(r"\begin{center}")
                out.append(r"\includegraphics[width=0.4\linewidth]{%s}" % img_map[rid])
                out.append(r"\end{center}")
            i += 1
            continue
        if not raw:
            i += 1
            continue
        m = SEC_RE.match(raw)
        if m:
            depth = m.group(1).count(".") + 1
            title = esc_txt(m.group(2))
            cmd = {1: "section", 2: "subsection", 3: "subsubsection"}[min(depth, 3)]
            out.append(r"\%s{%s}" % (cmd, title))
            i += 1
            continue
        if meta["bold"] and LET_RE.match(raw) and not meta["numid"]:
            out.append(r"\bigskip")
            out.append(r"\noindent\textbf{" + esc_txt(raw) + "}")
            i += 1
            continue
        if meta["numid"]:
            group = []
            while i < len(body_blocks) and body_blocks[i][0] == "p" \
                    and body_blocks[i][1]["numid"]:
                gm = body_blocks[i][1]
                group.append((gm["numid"], gm["ilvl"], fmt_runs(runs_of(gm["el"]))))
                i += 1
            out.extend(render_list(group, formats, dec_state))
            continue
        out.append(fmt_runs(runs_of(meta["el"])))
        i += 1

    out.append(r"\end{document}")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"OK -> {out_path}")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
