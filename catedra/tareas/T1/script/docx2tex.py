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


def item_to_latex(raw: str) -> str:
    """Ítem de lista: separa la etiqueta (antes de ": ") y la pasa a
    \\itemlabel{etiqueta}{:}{resto} para que vaya en negrita. Si no hay ": " o
    la etiqueta contiene un punto (parece referencia), se deja en texto plano."""
    text = raw.strip()
    idx = text.find(": ")
    if idx <= 0:
        return esc_txt(text)
    label = text[:idx]
    rest = text[idx + 2:]
    if "." in label:
        return esc_txt(text)
    return r"\itemlabel{" + esc_txt(label) + "}{:}{" + esc_txt(rest) + "}"


def cell_latex(tc) -> str:
    parts = []
    for p in tc.findall(qn("p")):
        txt = fmt_runs(runs_of(p))
        if txt.strip():
            parts.append(txt)
    return r"\newline ".join(parts) if parts else ""


TABLE_CAPTIONS = {
    "SÍNTESIS EJECUTIVA DEL CASO SCHÖN": "Síntesis ejecutiva del caso Schön",
    "SÍNTESIS EJECUTIVA DEL CASO INFORMÁTICA (ACM)": "Síntesis ejecutiva del caso Informática (ACM)",
    "Término Informático Real": "Ejemplos de ``tortured phrases'' detectadas en artículos de la ACM",
    "Criterio Evaluativo": "Análisis comparativo entre el caso Schön y el caso ACM",
}

# Fuentes de cada caso (claves de referencias.bib) para las subsecciones
# "Referencias y Fuentes de Información", renderizadas con \fullcite.
CASE_REFS = {
    1: ["nationalacademies2009", "beasley2002", "service2002", "marcus2022", "reich2009"],
    2: ["cabanac2021", "retractionwatch2022", "else2021", "acm2022", "beall2016"],
}


def unwrap_bold(s):
    s = s.strip()
    if s.startswith(r"\textbf{") and s.endswith("}"):
        return s[len(r"\textbf{"):-1]
    return s


def table_latex(tbl) -> str:
    rows = [[cell_latex(tc) for tc in row.findall(qn("tc"))] for row in tbl.findall(qn("tr"))]
    ncols = max(len(r) for r in rows)

    caption = None
    first = rows[0] if rows else []
    header_bold = True
    if len(first) == 1 and len(rows) > 1:
        # fila única al inicio = título de la tabla → pasa a caption y se descarta
        title_raw = unwrap_bold(first[0])
        caption = TABLE_CAPTIONS.get(title_raw, title_raw)
        rows = rows[1:]
        ncols = max(len(r) for r in rows)
        header_bold = False
    else:
        key = unwrap_bold(first[0]) if first else ""
        caption = TABLE_CAPTIONS.get(key)

    lines = [r"\begin{table}[htbp]", r"\centering"]
    if caption:
        lines.append(r"\caption{" + caption + "}")
    lines.append(r"\begin{tabularx}{\linewidth}{" + "X" * ncols + "}")
    lines.append(r"\toprule")
    for ri, cells in enumerate(rows):
        cells = list(cells)
        while len(cells) < ncols:
            cells.append("")
        if ri == 0 and header_bold:
            cells = [r"\textbf{" + c + "}" for c in cells]
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
    out.append(r"\usepackage{csquotes}")
    out.append(r"\usepackage[margin=2.5cm]{geometry}")
    out.append(r"\usepackage{setspace}")
    out.append(r"\onehalfspacing")  # regla del curso: interlineado 1,5
    out.append(r"\usepackage{microtype}")
    out.append(r"\usepackage{tgtermes}")  # TeX Gyre Termes ~ Times New Roman (regla del curso)
    out.append(r"\usepackage{booktabs}")
    out.append(r"\usepackage{tabularx}")
    out.append(r"\usepackage{graphicx}")
    out.append(r"\graphicspath{{img/}}")
    out.append(r"\usepackage[tableposition=top]{caption}")
    out.append(r"\captionsetup[table]{name=Tabla,labelsep=period,font=small,labelfont=bf,justification=raggedright,singlelinecheck=false,skip=4pt}")
    out.append(r"\usepackage{enumitem}")
    out.append(r"\setlist{itemsep=2pt,topsep=4pt,parsep=0pt}")
    out.append(r"\usepackage{titlesec}")
    out.append(r"\titleformat{\section}{\Large\bfseries}{\thesection.}{0.6em}{}[\vspace{3pt}\titlerule]")
    out.append(r"\titleformat{\subsection}{\large\bfseries}{\thesubsection.}{0.6em}{}")
    out.append(r"\titleformat{\subsubsection}{\normalsize\bfseries}{\thesubsubsection.}{0.6em}{}")
    out.append(r"\titlespacing*{\section}{0pt}{16pt}{8pt}")
    out.append(r"\titlespacing*{\subsection}{0pt}{12pt}{6pt}")
    out.append(r"\usepackage{tocloft}")
    out.append(r"\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}")
    out.append(r"\renewcommand{\cftsecfont}{\bfseries}")
    out.append(r"\renewcommand{\contentsname}{Índice}")
    out.append(r"\usepackage{fancyhdr}")
    out.append(r"\usepackage{lastpage}")
    out.append(r"\pagestyle{fancy}")
    out.append(r"\fancyhf{}")
    out.append(r"\fancyhead[L]{\small\itshape Informe de Evaluación — Unidad de Ética en Investigación (Parte 1)}")
    out.append(r"\fancyhead[R]{\small\itshape Metodologías de Investigación Aplicada}")
    out.append(r"\fancyfoot[C]{\small Página \thepage\ de \pageref{LastPage}}")
    out.append(r"\renewcommand{\headrulewidth}{0.4pt}")
    out.append(r"\setlength{\headheight}{14pt}")
    out.append(r"\usepackage[style=ieee,sorting=none,backend=biber]{biblatex}")
    out.append(r"\addbibresource{referencias.bib}")
    out.append(r"\usepackage{hyperref}")
    out.append(r"\usepackage{xurl}")
    out.append(r"\hypersetup{hidelinks,urlcolor=blue}")
    out.append(r"\setlength{\parindent}{0pt}")
    out.append(r"\setlength{\parskip}{5pt}")
    out.append(r"\renewcommand{\arraystretch}{1.25}")
    # Etiqueta en negrita en ítems de lista (3 argumentos):
    #   \itemlabel{Fabricación}{:}{Invención deliberada de datos...}
    out.append(r"\newcommand{\itemlabel}[3]{\textbf{#1#2}~#3}")
    out.append("")
    out.append(r"\begin{document}")
    out.append(r"\thispagestyle{empty}")

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
    out.append(r"\vspace{16pt}")
    out.append(r"\rule{\textwidth}{0.4pt}")
    out.append(r"\end{center}")
    out.append(r"\newpage")
    out.append(r"\tableofcontents")
    out.append(r"\newpage")

    # ---- Cuerpo ----
    body_blocks = blocks[first_sec:]
    dec_state = {"first": True}
    current_case = 0
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
            if depth == 1:
                up = title.upper()
                if "CASO 1" in up:
                    current_case = 1
                elif "CASO 2" in up:
                    current_case = 2
            if depth == 2 and "REFERENCIAS" in title.upper():
                # fuentes del caso en IEEE vía \fullcite (misma referencias.bib);
                # la lista completa consolidada queda en la bibliografía general
                out.append(r"\subsection{%s}" % title)
                out.append(r"\begin{itemize}")
                for key in CASE_REFS.get(current_case, []):
                    out.append(r"\item \fullcite{%s}" % key)
                out.append(r"\end{itemize}")
                i += 1
                while i < len(body_blocks):
                    b2 = body_blocks[i]
                    if b2[0] == "p" and SEC_RE.match(b2[1]["raw"].strip()):
                        break
                    i += 1
                continue
            cmd = {1: "section", 2: "subsection", 3: "subsubsection"}[min(depth, 3)]
            out.append(r"\%s{%s}" % (cmd, title))
            if depth == 1 and "BIBLIOGRAFÍA" in title.upper():
                # la bibliografía general se gestiona con biblatex (IEEE) + referencias.bib
                out.append(r"\nocite{*}")
                out.append(r"\printbibliography[heading=none]")
                i = len(body_blocks)
                continue
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
                # ítem con etiqueta en negrita vía \itemlabel{label}{:}{resto}
                group.append((gm["numid"], gm["ilvl"], item_to_latex(gm["raw"])))
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
