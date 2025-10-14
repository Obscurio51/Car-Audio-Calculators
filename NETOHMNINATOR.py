"""
calcolatore_reti_keygen_v3.py
Versione V3 — Keygen-style GUI con:
 - spinbox stile keygen (frecce verdi)
 - progress bar reale (percentuale + conteggio) SOPRA il pulsante CALCOLA
 - Treeview/stile identico al codice originale: scrollbar verde, heading non diventa bianco
 - disegno rete: S (serie) rami verdi, P (parallelo) rami bianchi
 - mantiene audio opzionale, versione completa, annulla, esport CSV
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
import threading
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import base64, tempfile, os, time, subprocess, shutil, random, sys

def resource_path(relative_path):
    """Restituisce il percorso corretto per il file, anche se è dentro un exe PyInstaller"""
    try:
        # PyInstaller crea questa variabile temporanea
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# optional audio
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

# ---------------- Theme constants (Keygen) ----------------
NEON_BG = "#000000"
NEON_GREEN = "#23ff00"
NEON_GREEN_DIM = "#0fa000"
PANEL_BG = "#070707"
ENTRY_BG = "#001100"
BORDER_COLOR = "#003300"
HEADING_BG = "#002200"
FONT_MONO = ("Consolas", 10)

# ---------------- Base64 music placeholder ----------------
BASE64_KEYGEN_MUSIC = """dGhlIGFybW9yIG9mIGdvZC4AAABieSBtYWt0b25lIG9mOiAgY2xhc3MmAi4AQAAAAAB4LXByZXNzaW9uJnN1cGVyc3RhcnMAAUIAQAAAAAAtAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOwAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4AQAAGADgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABQAQAAGAA4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAASAA4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAASAA4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAASAA5ncmVldHMgdG86IC0AAAAAAAAAAAAAAAAAAAAAAABveHlnZW5lci5uYXRhbjEuc3Bhcmt5AAAAAAAAAABvbWVnYXR3by5zZWZmcmVuLmF0bS4AAAAAAAAAAABnb2xkcHVzaC5sZWsuYW50aWJvZHkuAAAAAAAAAABzY29ycGlvLnplYy5zaG9vcG9vLgAAAAAAAAAAAABrb29sYWcud2hpenp0ZXIuZGFydS4AAAAAAAAAAAByZXB0aWxlLm1lbXBoZXJpYS4AAAAAAAAAAAAAAAB3YXJoYXdrLmtsZWZ6Lnp1bGxlLgAAAAAAAAAAAABsb29uaWUubWl0aHJpcy5mdW5uZWwuAAAAAAAAAAAtIDoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAABAgMEBQYHCAkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATS5LLgGsTwUBrIAAAR2EgQFohIEAAAAAAAAAAAAABAAAAAQAAAAAAAEdgAAAAAQAAAAEAAAAAAABrIweAAAEAAAABAAAAAAAAWiAAAAABAAAAAQAAAAAAAEdjB4AAAQAAAAEAAAAAAABrIAAAAAEAAAABAAAAAAAAWiMHgAABAAAAAQAAAAAAAFogAAAAAQAAAAEAAAAAAABrIweAAAEAAAABAAAAAAAAR2AAAAABAAAAAQAAAAAAAFojB4AAAQAAAAEAAAACgIBaIAAAAAEAAAABAAAAAoCAR2MHgAABAAAAAQAAAAKAgGsgAABDYQAAAAEAAAACgIBaIweAAAEAAAABAAB4EAAAeCAAAFAhAABfYQAAAAAAAAAAAAAAAQAAAAEAAAAAAABQIAAAAAEAAAABAAAAAAAAeCMHgAABAAAAAQAAAAAAAF9gAAAAAQAAAAEAAAAAAABQIweAAAEAAAABAAAAAAAAeCAAAAABAAAAAQAAAAAAAF9jB4AAAQAAAAEAAAAAAABfYAAAAAEAAAABAAAAAAAAeCMHgAABAAAAAQAAAAAAAFAgAAAAAQAAAAEAAAAAAABfYweAAAEAAAABAAAAAoCAX2AAAAABAAAAAQAAAAKAgFAjB4AAAQAAAAEAAAACgIB4IAAAAAEAAFohAAAAAoCAX2MHgAABAAAAAQAAjpAAAI6gAABfYQAAeCEAAAAAAAAAAAAAAAEAAAABAAAAAAAAX2AAAAABAAAAAQAAAAAAAI6jB4AAAQAAAAEAAAAAAAB4IAAAAAEAAAABAAAAAAAAX2MHgAABAAAAAQAAAAAAAI6gAAAAAQAAAAEAAAAAAAB4IweAAAEAAAABAAAAAAAAeCAAAAABAAAAAQAAAAAAAI6jB4AAAQAAAAEAAAAAAABfYAAAAAEAAAABAAAAAAAAX2MHgAABAAAAAQAAAAKAgHggAAAAAQAAAAEAAAACgICOoweAAAEAAAABAAAAAoCAjqAAAFohAAAAAQAAAAKAgHgjB4AAAQAAAAEAAKAQAACgIAAAayEAAH8hAAAAAAAAAAAAAAABAAAAAQAAAAAAAGsgAAAAAQAAAAEAAAAAAACgIweAAAEAAAABAAAAAAAAfyAAAAABAAAAAQAAAAAAAGsjB4AAAQAAAAEAAAAAAACgIAAAAAEAAAABAAAAAAAAfyMHgAABAAAAAQAAAAAAAH8gAAAAAQAAAAEAAAAAAACgIweAAAEAAAABAAAAAAAAayAAAAABAAAAAQAAAAAAAH8jB4AAAQAAAAEAAAACgIB/IAAAAAEAAAABAAAAAoCAoCMHgAABAAAAAQAAAAKAgKAgAAAAAQAAeCEAAAACgIBrIweAAAEAAAABAABrEAAAayAAAEdhIEBaISBAAAAAAAAAAAAAAQAAAAEAAAAAAABHYAAAAAEAAAABAAAAAAAAayMHgAABAAAAAQAAAAAAAFogAAAAAQAAAAEAAAAAAABHYweAAAEAAAABAAAAAAAAayAAAAABAAAAAQAAAAAAAFojB4AAAQAAAAEAAAAAAABaIAAAAAEAAAABAAAAAAAAayMHgAABAAAAAQAAAAAAAEdgAAAAAQAAAAEAAAAAAABaIweAAAEAAAABAAAAAoCAWiAAAAABAAAAAQAAAAKAgEdjB4AAAQAAAAEAAAACgIBrIAAAQ2EAAAABAAAAAoCAWiMHgAABAAAAAQAAeBAAAHggAABQIQAAX2EAAAAAAAAAAAAAAAEAAAABAAAAAAAAUCAAAAABAAAAAQAAAAAAAHgjB4AAAQAAAAEAAAAAAABfYAAAAAEAAAABAAAAAAAAUCMHgAABAAAAAQAAAAAAAHggAAAAAQAAAAEAAAAAAABfYweAAAEAAAABAAAAAAAAX2AAAAABAAAAAQAAAAAAAHgjB4AAAQAAAAEAAAAAAABQIAAAAAEAAAABAAAAAAAAX2MHgAABAAAAAQAAAAKAgF9gAAAAAQAAAAEAAAACgIBQIweAAAEAAAABAAAAAoCAeCAAAAABAABaIQAAAAKAgF9jB4AAAQAAAAEAAI6QAACOoAAAX2EAAHghAAAAAAAAAAAAAAABAAAAAQAAAAAAAF9gAAAAAQAAAAEAAAAAAACOoweAAAEAAAABAAAAAAAAeCAAAAABAAAAAQA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
"""  # se vuoi musica, incolla la base64 qui

# ---------------- Math helpers ----------------
def safe_fraction(x):
    if isinstance(x, Fraction):
        return x
    try:
        return Fraction(str(float(x))).limit_denominator()
    except Exception:
        try:
            return Fraction(x)
        except Exception:
            raise ValueError(f"Valore non valido: {x}")

def series(a, b):
    a = safe_fraction(a); b = safe_fraction(b)
    return a + b

def parallel(a, b):
    a = safe_fraction(a); b = safe_fraction(b)
    if a + b == 0:
        return Fraction(0,1)
    return (a * b) / (a + b)

def canonical_key(frac_list):
    lst = sorted([safe_fraction(x) for x in frac_list], key=lambda x: float(x))
    return tuple((int(v.numerator), int(v.denominator)) for v in lst)

# ---------------- Caching recursive reachable ----------------
@lru_cache(maxsize=None)
def reachable_values_for_key(key):
    # key is tuple of (num,den) pairs or Fractions
    state = []
    for item in key:
        if isinstance(item, Fraction):
            state.append(item)
        else:
            try:
                n,d = item
                state.append(Fraction(n,d))
            except Exception:
                state.append(Fraction(item))
    if len(state) == 1:
        return {state[0]}
    results = set()
    n = len(state)
    for i in range(n):
        for j in range(i+1, n):
            a = state[i]; b = state[j]
            rest = [state[k] for k in range(n) if k!=i and k!=j]
            # series
            s = series(a,b)
            key_s = canonical_key(rest + [s])
            results |= reachable_values_for_key(key_s)
            # parallel
            p = parallel(a,b)
            key_p = canonical_key(rest + [p])
            results |= reachable_values_for_key(key_p)
    return results

# build expression tree / find expression
def replace_one_leaf(node, leaf_value, replacement_node):
    t = node[0]
    if t == 'leaf':
        if node[1] == leaf_value:
            return replacement_node
        return None
    left = node[1]; right = node[2]
    new_left = replace_one_leaf(left, leaf_value, replacement_node)
    if new_left is not None:
        return (t, new_left, right)
    new_right = replace_one_leaf(right, leaf_value, replacement_node)
    if new_right is not None:
        return (t, left, new_right)
    return None

@lru_cache(maxsize=None)
def find_expr_for_exact_value(key, target_num, target_den):
    target = Fraction(target_num, target_den)
    state = []
    for item in key:
        if isinstance(item, Fraction):
            state.append(item)
        else:
            try:
                n,d = item
                state.append(Fraction(n,d))
            except Exception:
                state.append(Fraction(item))
    if len(state) == 1:
        if state[0] == target:
            return ('leaf', state[0])
        return None
    n = len(state)
    for i in range(n):
        for j in range(i+1, n):
            a = state[i]; b = state[j]
            rest = [state[k] for k in range(n) if k!=i and k!=j]
            s = series(a,b)
            key_s = canonical_key(rest + [s])
            try:
                if target in reachable_values_for_key(key_s):
                    sub = find_expr_for_exact_value(key_s, target_num, target_den)
                    if sub is not None:
                        replaced = replace_one_leaf(sub, s, ('S', ('leaf', a), ('leaf', b)))
                        if replaced is not None:
                            return replaced
            except RecursionError:
                pass
            p = parallel(a,b)
            key_p = canonical_key(rest + [p])
            try:
                if target in reachable_values_for_key(key_p):
                    sub = find_expr_for_exact_value(key_p, target_num, target_den)
                    if sub is not None:
                        replaced = replace_one_leaf(sub, p, ('P', ('leaf', a), ('leaf', b)))
                        if replaced is not None:
                            return replaced
            except RecursionError:
                pass
    return None

def expr_value_and_str(node):
    t = node[0]
    if t == 'leaf':
        v = node[1]
        return v, f"{float(v):g}"
    if t == 'S':
        a_val, a_str = expr_value_and_str(node[1])
        b_val, b_str = expr_value_and_str(node[2])
        val = series(a_val, b_val)
        return val, f"({a_str} S {b_str})"
    if t == 'P':
        a_val, a_str = expr_value_and_str(node[1])
        b_val, b_str = expr_value_and_str(node[2])
        val = parallel(a_val, b_val)
        return val, f"({a_str} P {b_str})"
    raise ValueError("Unknown node type")

# ---------------- UI setup (keygen theme) ----------------
root = tk.Tk()
root.title("Calcolatore abbinamenti OHM")
root.geometry("1200x780")
root.configure(bg=NEON_BG)
root.iconbitmap(resource_path("icongg.ico"))

ASCII_TITLE = r"""
      ::::    ::: :::::::::: :::::::::::          ::::::::  :::    :::   :::   :::   ::::    ::: ::::::::::: ::::    :::     ::: ::::::::::: ::::::::  ::::::::: 
     :+:+:   :+: :+:            :+:             :+:    :+: :+:    :+:  :+:+: :+:+:  :+:+:   :+:     :+:     :+:+:   :+:   :+: :+:   :+:    :+:    :+: :+:    :+: 
    :+:+:+  +:+ +:+            +:+             +:+    +:+ +:+    +:+ +:+ +:+:+ +:+ :+:+:+  +:+     +:+     :+:+:+  +:+  +:+   +:+  +:+    +:+    +:+ +:+    +:+  
   +#+ +:+ +#+ +#++:++#       +#+             +#+    +:+ +#++:++#++ +#+  +:+  +#+ +#+ +:+ +#+     +#+     +#+ +:+ +#+ +#++:++#++: +#+    +#+    +:+ +#++:++#:    
  +#+  +#+#+# +#+            +#+             +#+    +#+ +#+    +#+ +#+       +#+ +#+  +#+#+#     +#+     +#+  +#+#+# +#+     +#+ +#+    +#+    +#+ +#+    +#+    
 #+#   #+#+# #+#            #+#             #+#    #+# #+#    #+# #+#       #+# #+#   #+#+#     #+#     #+#   #+#+# #+#     #+# #+#    #+#    #+# #+#    #+#     
###    #### ##########     ###              ########  ###    ### ###       ### ###    #### ########### ###    #### ###     ### ###     ########  ###    ###      
"""
header_canvas = tk.Canvas(root, bg=NEON_BG, highlightthickness=0, height=120)
header_canvas.pack(fill="x", padx=0, pady=(0,4))

def draw_logo():
    header_canvas.delete("all")
    lines = ASCII_TITLE.strip("\n").split("\n")
    font_family="Consolas"; font_size=10
    x0,y0=8,6
    for i,line in enumerate(lines):
        y = y0 + i*12
        header_canvas.create_text(x0+2,y+2,text=line,fill="#022200",font=(font_family,font_size),anchor="nw")
        header_canvas.create_text(x0+1,y+1,text=line,fill=NEON_GREEN_DIM,font=(font_family,font_size),anchor="nw",tags="logo_glow")
        header_canvas.create_text(x0,y,text=line,fill=NEON_GREEN,font=(font_family,font_size),anchor="nw",tags="logo_main")
draw_logo()
def logo_pulse():
    header_canvas.itemconfigure("logo_main", fill=(NEON_GREEN_DIM if random.random()<0.45 else NEON_GREEN))
    root.after(400+random.randint(-120,120), logo_pulse)
logo_pulse()

# frames
left = tk.Frame(root, bg=PANEL_BG, padx=10, pady=10)
left.pack(side="left", fill="y")
right = tk.Frame(root, bg=PANEL_BG, padx=10, pady=10)
right.pack(side="right", fill="both", expand=True)

def make_entry(parent, label, default=""):
    lbl = tk.Label(parent, text=label, bg=PANEL_BG, fg=NEON_GREEN, font=FONT_MONO)
    lbl.pack(anchor="w", pady=(6,2))
    e = tk.Entry(parent, bg=ENTRY_BG, fg=NEON_GREEN, insertbackground=NEON_GREEN,
                 font=("Consolas",11), bd=0, relief="flat")
    e.configure(highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=NEON_GREEN)
    e.pack(fill="x", pady=(0,4))
    if default:
        e.insert(0, default)
    return e

# inputs
std_values = [0.5,1,2,3,4,6,8,16]
std_vars = {}
vals_label = tk.Label(left, text="Valori standard:", bg=PANEL_BG, fg=NEON_GREEN, font=FONT_MONO)
vals_label.pack(anchor="w")
vals_frame = tk.Frame(left, bg=PANEL_BG); vals_frame.pack()
for i,v in enumerate(std_values):
    var = tk.IntVar(value=1 if v==4 else 0)
    cb = tk.Checkbutton(vals_frame, text=f"{v} Ω", variable=var, bg=PANEL_BG, fg=NEON_GREEN, selectcolor="#002200", font=FONT_MONO)
    cb.grid(row=i//4,column=i%4, sticky="w", padx=4)
    std_vars[v]=var

custom_entry = make_entry(left, "Valori personalizzati (es: 2.2,5.6):", "")
mandatory_entry = make_entry(left, "Resistenze obbligatorie (es: 4,4):", "4,4")

# Spinbox stile keygen (tentativo di freccette verdi cross-platform)
def make_spinbox(parent, from_, to, initial):
    sb = tk.Spinbox(parent, from_=from_, to=to, width=4,
                    bg=ENTRY_BG, fg=NEON_GREEN, font=FONT_MONO,
                    buttonbackground="#002200",
                    highlightbackground=BORDER_COLOR, highlightcolor=NEON_GREEN,
                    relief="flat", bd=1, insertbackground=NEON_GREEN)
    sb.delete(0,'end'); sb.insert(0,str(initial))
    return sb

minmax_frame = tk.Frame(left, bg=PANEL_BG); minmax_frame.pack(anchor="w", pady=(6,2))
tk.Label(minmax_frame, text="Min:", bg=PANEL_BG, fg=NEON_GREEN, font=FONT_MONO).grid(row=0,column=0)
min_res_spin = make_spinbox(minmax_frame, 2, 12, 2); min_res_spin.grid(row=0,column=1,padx=4)
tk.Label(minmax_frame, text="Max:", bg=PANEL_BG, fg=NEON_GREEN, font=FONT_MONO).grid(row=0,column=2)
max_res_spin = make_spinbox(minmax_frame, 2, 12, 8); max_res_spin.grid(row=0,column=3,padx=4)

target_entry = make_entry(left, "Target (Ω):", "2.0")
tol_entry = make_entry(left, "Tolleranza (Ω):", "0.05")

draw_schema_var = tk.IntVar(value=1)
versione_completa_var = tk.IntVar(value=0)
music_var = tk.IntVar(value=1)

tk.Checkbutton(left, text="Versione completa (off = max 40 results)", variable=versione_completa_var, bg=PANEL_BG, fg=NEON_GREEN, selectcolor="#002200", font=FONT_MONO).pack(anchor="w")
tk.Checkbutton(left, text="Musica", variable=music_var, bg=PANEL_BG, fg=NEON_GREEN, selectcolor="#002200", font=FONT_MONO).pack(anchor="w", pady=(6,2))

status_label = tk.Label(left, text="Pronto.", bg=PANEL_BG, fg=NEON_GREEN, font=("Consolas",9,"italic"))
status_label.pack(anchor="w", pady=(8,4))

# pulsating entry effect
def pulse_entries():
    for ch in left.winfo_children():
        if isinstance(ch, tk.Entry):
            ch.configure(highlightbackground=(random.choice([NEON_GREEN, NEON_GREEN_DIM]) if random.random()<0.25 else BORDER_COLOR))
    root.after(600, pulse_entries)
pulse_entries()

# Treeview & styling restore to original Keygen behavior
style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass

# Treeview colors
style.configure("Treeview",
                background=ENTRY_BG,
                foreground=NEON_GREEN,
                fieldbackground=ENTRY_BG,
                font=("Consolas",9),
                rowheight=20,
                bordercolor=BORDER_COLOR,
                borderwidth=1)
# selection keeps neon green
style.map("Treeview",
          background=[("selected", HEADING_BG)],
          foreground=[("selected", NEON_GREEN)])
# Heading: fix background to HEADING_BG for all states to avoid white flashing
style.configure("Treeview.Heading",
                background=HEADING_BG,
                foreground=NEON_GREEN,
                font=("Consolas",9,"bold"),
                bordercolor=BORDER_COLOR)

style.map("Treeview.Heading",
          background=[("active", HEADING_BG), ("!active", HEADING_BG)],
          foreground=[("active", NEON_GREEN), ("!active", NEON_GREEN)])

# Scrollbar neon (restore original keygen style)
style.configure("Neon.Vertical.TScrollbar",
                troughcolor=ENTRY_BG,
                background=NEON_GREEN,
                darkcolor=NEON_GREEN_DIM,
                lightcolor=NEON_GREEN,
                bordercolor=BORDER_COLOR,
                arrowcolor=NEON_GREEN,
                troughrelief="flat",
                relief="flat",
                gripcount=0)
style.map("Neon.Vertical.TScrollbar",
          background=[("active", NEON_GREEN), ("!active", NEON_GREEN_DIM)],
          arrowcolor=[("active", NEON_GREEN), ("!active", NEON_GREEN)])

# Progressbar style (green neon)
style.configure("Neon.Horizontal.TProgressbar",
                troughcolor=ENTRY_BG,
                background=NEON_GREEN,
                thickness=12)
style.map("Neon.Horizontal.TProgressbar",
          background=[("!disabled", NEON_GREEN)])

# Place progress bar ABOVE CALCOLA (per richiesta)
progress_frame = tk.Frame(left, bg=PANEL_BG)
progress_frame.pack(fill="x", pady=(6,4))
progress_bar = ttk.Progressbar(progress_frame, style="Neon.Horizontal.TProgressbar", orient="horizontal", mode="determinate", length=260)
progress_bar.pack(side="left", padx=(0,6))
progress_text = tk.Label(progress_frame, text="", bg=PANEL_BG, fg=NEON_GREEN, font=("Consolas",9))
progress_text.pack(side="left")

border_wrap = tk.Frame(right, bg=NEON_GREEN); border_wrap.pack(fill="both", expand=True, padx=6, pady=6)
table_frame = tk.Frame(border_wrap, bg=PANEL_BG); table_frame.pack(fill="both", expand=True, padx=2, pady=2)

cols = ("speakers","expr","value")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Treeview")
for c in cols:
    tree.heading(c, text=c.capitalize())
    tree.column(c, anchor="w", width=200, stretch=True)
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview, style="Neon.Vertical.TScrollbar")
tree.configure(yscrollcommand=vsb.set)
tree.grid(row=0,column=0, sticky="nsew", padx=(4,0), pady=4)
vsb.grid(row=0,column=1, sticky="ns", padx=(6,4), pady=4)
table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

# matplotlib canvas for drawing networks
canvas_frame = tk.Frame(right, bg=PANEL_BG); canvas_frame.pack(fill="both", expand=True)
_fig = plt.Figure(figsize=(6,3), facecolor='black', dpi=100)
_ax = _fig.add_subplot(111); _ax.set_facecolor('black')
canvas = FigureCanvasTkAgg(_fig, master=canvas_frame)
canvas_widget = canvas.get_tk_widget(); canvas_widget.pack(fill="both", expand=True)

results_list = []

# drawing functions (tree layout) — SERIES GREEN, PARALLEL WHITE; labels S/P
def plot_tree_matplotlib(node, title=None):
    if node is None:
        return None
    root.update_idletasks()
    w_px = max(canvas_widget.winfo_width(), 200); h_px = max(canvas_widget.winfo_height(), 120)
    dpi = 100; fig_w = w_px / dpi; fig_h = h_px / dpi
    positions = {}; labels = {}; counter = {'x':0}
    def assign(n, depth=0):
        t = n[0]
        if t == 'leaf':
            x = counter['x']; positions[id(n)] = (x, -depth); labels[id(n)] = f"{float(n[1]):g}"; counter['x']+=1; return positions[id(n)]
        left = n[1]; right = n[2]; lpos = assign(left, depth+1); rpos = assign(right, depth+1)
        x = (lpos[0]+rpos[0])/2.0; positions[id(n)] = (x, -depth); labels[id(n)] = expr_value_and_str(n)[1]; return positions[id(n)]
    assign(node, depth=0)
    fig = plt.Figure(figsize=(fig_w, fig_h), facecolor='black', dpi=dpi)
    ax_local = fig.add_subplot(111); ax_local.set_facecolor('black')
    def draw(n):
        nid = id(n); x,y = positions[nid]; t = n[0]
        if t != 'leaf':
            left = n[1]; right = n[2]
            branch_color = NEON_GREEN if t == 'S' else "white"
            for child in (left, right):
                cx,cy = positions[id(child)]
                ax_local.plot([x,cx],[y,cy], color=branch_color, linewidth=1.5)
                draw(child)
        ax_local.scatter([x],[y], s=100, color=NEON_GREEN)
        ax_local.text(x,y, labels[nid], color='black', fontsize=8, ha='center', va='center', backgroundcolor=NEON_GREEN)
    draw(node)
    ax_local.axis('off')
    if title:
        ax_local.set_title(title, color=NEON_GREEN)
    fig.tight_layout()
    return fig

def update_canvas_figure(fig_local):
    if fig_local is None:
        return
    root.update_idletasks()
    if not canvas_widget.winfo_ismapped():
        canvas.figure = fig_local; canvas.draw_idle(); return
    w = max(canvas_widget.winfo_width(), 200); h = max(canvas_widget.winfo_height(), 120)
    try: dpi = getattr(fig_local, "dpi", 100) or 100
    except Exception: dpi = 100
    try: fig_local.set_size_inches(w/dpi, h/dpi)
    except Exception: pass
    canvas.figure = fig_local; canvas.draw_idle(); canvas_widget.update_idletasks()

# ---------------- Audio thread (kept) ----------------
_audio_thread = None; _audio_stop_event = threading.Event(); _audio_tempfile = None; _music_flag = False

def _audio_play_loop():
    global _audio_tempfile, _music_flag
    if not BASE64_KEYGEN_MUSIC or not BASE64_KEYGEN_MUSIC.strip():
        return
    if not PYGAME_AVAILABLE:
        root.after(0, lambda: messagebox.showwarning("Musica disabilitata","Installa pygame per abilitare la musica"))
        return
    try:
        decoded = base64.b64decode(BASE64_KEYGEN_MUSIC)
        fd, tmp = tempfile.mkstemp(prefix="keygen_music_", suffix=".mp3"); os.close(fd)
        with open(tmp,"wb") as f: f.write(decoded)
        _audio_tempfile = tmp
        wav = tmp
        if shutil.which("ffmpeg"):
            fd2, wav = tempfile.mkstemp(prefix="keygen_music_", suffix=".wav"); os.close(fd2)
            try:
                subprocess.run(["ffmpeg","-y","-loglevel","error","-i", tmp, wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
                try: os.unlink(tmp)
                except Exception: pass
            except Exception:
                wav = tmp
        import pygame
        pygame.mixer.quit(); pygame.mixer.init(); pygame.mixer.music.load(wav); pygame.mixer.music.set_volume(0.5); pygame.mixer.music.play(-1)
        while _music_flag and not _audio_stop_event.is_set():
            time.sleep(0.5)
        pygame.mixer.music.stop(); pygame.mixer.quit()
    except Exception as e:
        print("[audio error]", e)
    finally:
        try:
            if _audio_tempfile and os.path.exists(_audio_tempfile): os.unlink(_audio_tempfile)
        except Exception:
            pass

def start_audio():
    global _audio_thread, _music_flag
    _music_flag = bool(music_var.get())
    _audio_stop_event.set()
    if _audio_thread and _audio_thread.is_alive():
        _audio_thread.join(timeout=0.5)
    _audio_stop_event.clear()
    if _music_flag:
        _audio_thread = threading.Thread(target=_audio_play_loop, daemon=True); _audio_thread.start()

def on_music_change(*args):
    if music_var.get():
        status_label.config(text="Musica ON")
        start_audio()
    else:
        status_label.config(text="Musica OFF"); _audio_stop_event.set()

music_var.trace_add('write', on_music_change)

# ---------------- Parsing helpers & pruning ----------------
def parse_vals(txt):
    out=[]
    if not txt: return out
    for p in [x.strip() for x in txt.split(",") if x.strip()]:
        try:
            out.append(Fraction(str(float(p))).limit_denominator())
        except Exception:
            try: out.append(Fraction(p))
            except Exception: pass
    return out

def multisets_with_mandatory(values, min_n, max_n, mandatory):
    out=set(); mand_len=len(mandatory)
    for n in range(max(min_n, mand_len), max_n+1):
        r = n - mand_len
        if r < 0: continue
        for comb in combinations_with_replacement(values, r):
            full = tuple(sorted(list(mandatory) + list(comb), key=lambda x: float(x)))
            out.add(full)
    return sorted(out, key=lambda x:(len(x), x))

def harmonic_parallel_min(vals):
    s = 0.0
    for v in vals:
        try:
            s += 1.0/float(v)
        except Exception:
            s += 0.0
    if s <= 0: return 0.0
    return 1.0/s

# ---------------- Progress controls and cancel ----------------
progress_cancel_event = threading.Event()

def cancel_calculation():
    progress_cancel_event.set()
    status_label.config(text="Cancellazione richiesta...")

cancel_btn = tk.Button(left, text="Annulla", command=cancel_calculation, bg=ENTRY_BG, fg=NEON_GREEN, bd=0, relief="flat")
cancel_btn.pack(fill="x", pady=(6,2))

# ---------------- Worker logic (threaded) ----------------
def show_results(results):
    global results_list
    results_list = results
    for i in tree.get_children(): tree.delete(i)
    for idx, r in enumerate(results):
        speakers_str=[]
        for x in r['speakers']:
            fx=float(x)
            speakers_str.append(str(int(round(fx))) if abs(fx-round(fx))<1e-9 else f"{fx:g}")
        tree.insert('', 'end', iid=str(idx), values=(",".join(speakers_str), r['expr'], f"{r['value']:.6f}"))
    status_label.config(text=f"Trovate {len(results)} soluzioni.")
    if results and draw_schema_var.get():
        node = results[0]['tree']
        fig_local = plot_tree_matplotlib(node, title=results[0]['expr'])
        update_canvas_figure(fig_local)

def worker_calculation(all_values, mandatory, min_res, max_res, target_frac, tol, versione_completa):
    try:
        progress_cancel_event.clear()
        multisets = multisets_with_mandatory(all_values, min_res, max_res, mandatory)
        total = len(multisets)
        if total == 0:
            root.after(0, lambda: messagebox.showinfo("Nessun multiset", "Nessun multiset generato con i parametri inseriti."))
            return
        root.after(0, lambda: (progress_bar.config(maximum=max(1,total)), progress_bar.config(value=0), progress_text.config(text=f"0/0 (0%)")))
        results=[]; seen=set(); processed=0
        max_checks = 10**12 if versione_completa else 100000  # safety
        for ms in multisets:
            if progress_cancel_event.is_set():
                break
            processed += 1
            # update progress UI every few iterations
            if processed % 5 == 0 or processed == 1 or processed == total:
                pct = int(processed/total*100)
                root.after(0, lambda p=processed, t=total, pc=pct: (progress_bar.config(value=p), progress_text.config(text=f"{pc}% - {p}/{t}"), status_label.config(text=f"Verifica {p}/{t}...")))
            # quick prune numeric bounds
            numeric_list = [float(x) for x in ms]
            max_possible = sum(numeric_list)
            min_possible = harmonic_parallel_min(numeric_list)
            if float(target_frac) + tol < min_possible - 1e-9 or float(target_frac) - tol > max_possible + 1e-9:
                continue
            key = canonical_key(ms)
            try:
                reach = reachable_values_for_key(key)
            except RecursionError:
                continue
            match = [v for v in reach if abs(float(v)-float(target_frac))<=tol]
            if not match:
                continue
            chosen = min(match, key=lambda x: abs(float(x)-float(target_frac)))
            try:
                node = find_expr_for_exact_value(key, chosen.numerator, chosen.denominator)
            except RecursionError:
                node = None
            if node is None:
                continue
            val, expr = expr_value_and_str(node)
            expr_norm = expr.replace(' ','')
            seen.add(expr_norm)
            results.append({'speakers': ms, 'expr': expr, 'value': float(val), 'tree': node})
            # safety
            if not versione_completa and len(results) >= 40:
                break
            if processed >= max_checks:
                break
        root.after(0, lambda: show_results(results))
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Errore worker", str(e)))
    finally:
        root.after(0, lambda: progress_text.config(text=""))
        root.after(0, lambda: progress_bar.config(value=0))
        progress_cancel_event.clear()

# ---------------- Start calculation UI ----------------
def on_calculate():
    try:
        selected=[Fraction(str(v)) for v,var in std_vars.items() if var.get()==1]
    except Exception:
        selected=[]
    custom = parse_vals(custom_entry.get())
    all_values = sorted(set(selected+custom), key=lambda x: float(x)) if (selected or custom) else []
    if not all_values:
        messagebox.showerror("Errore", "Seleziona almeno un valore o inserisci valori personalizzati.")
        return
    mandatory = parse_vals(mandatory_entry.get())
    try:
        min_res = int(min_res_spin.get()); max_res = int(max_res_spin.get())
    except Exception:
        messagebox.showerror("Errore", "Min/Max non validi"); return
    try:
        target_frac = Fraction(str(float(target_entry.get()))).limit_denominator()
    except Exception:
        messagebox.showerror("Errore","Target non valido"); return
    try:
        tol = float(tol_entry.get())
    except Exception:
        tol = 0.05
    versione_completa = bool(versione_completa_var.get())
    if versione_completa and max_res >= 9:
        if not messagebox.askokcancel("Attenzione", "La versione completa con molte resistenze può richiedere molto tempo. Continuare?"):
            return
    status_label.config(text="Preparazione calcolo...")
    progress_cancel_event.clear()
    progress_bar.config(value=0)
    progress_text.config(text="0/0 (0%)")
    th = threading.Thread(target=worker_calculation, args=(all_values, mandatory, min_res, max_res, target_frac, tol, versione_completa), daemon=True)
    th.start()

# place CALCOLA button (progress is above)
calc_btn = tk.Button(left, text=">>> CALCOLA <<<", command=on_calculate, bg=ENTRY_BG, fg=NEON_GREEN, font=("Consolas",11,"bold"), bd=0, relief="flat")
calc_btn.pack(fill="x", pady=(10,6))

# export / clear / exit
def clear_all():
    for i in tree.get_children(): tree.delete(i)
    status_label.config(text="Pulito.")

def export_csv():
    items=[tree.item(iid)['values'] for iid in tree.get_children()]
    if not items:
        messagebox.showinfo("Export","Nessun dato da esportare")
        return
    fn = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if not fn:
        return
    try:
        with open(fn,"w",encoding="utf-8") as f:
            f.write("Speakers,Expr,Value\n")
            for row in items:
                expr = str(row[1]).replace(",",";")
                f.write(f"{row[0]},{expr},{row[2]}\n")
        messagebox.showinfo("Export", f"Esportato: {fn}")
    except Exception as e:
        messagebox.showerror("Export failed", str(e))

btns_frame = tk.Frame(left, bg=PANEL_BG); btns_frame.pack(fill="x", pady=(6,2))
tk.Button(btns_frame, text="Azzera", command=clear_all, bg=ENTRY_BG, fg=NEON_GREEN, bd=0, relief="flat").pack(fill="x", pady=2)
tk.Button(btns_frame, text="Esporta CSV", command=export_csv, bg=ENTRY_BG, fg=NEON_GREEN, bd=0, relief="flat").pack(fill="x", pady=2)

# tree selection -> draw
def on_select(event=None):
    sel = tree.selection()
    if not sel:
        return
    try:
        idx = int(sel[0])
    except Exception:
        return
    entry = results_list[idx]
    node = entry.get('tree')
    fig_local = plot_tree_matplotlib(node, title=entry['expr'])
    update_canvas_figure(fig_local)

tree.bind("<<TreeviewSelect>>", on_select)

# graceful close
def on_close():
    try:
        progress_cancel_event.set()
        _audio_stop_event.set()
        time.sleep(0.1)
    except Exception:
        pass
    try:
        root.destroy()
    except Exception:
        os._exit(0)

root.protocol("WM_DELETE_WINDOW", on_close)

# start audio if requested
if music_var.get():
    start_audio()

root.mainloop()
