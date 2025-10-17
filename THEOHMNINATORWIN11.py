# calcolatore_reti_pyqt_v3.py
# Conversione 1:1 da tkinter -> PyQt6
# Versione V3 — Keygen-style GUI portata su PyQt6
# Mantiene tutte le funzioni, layout, bottoni, logica, audio opzionale, export PNG, annulla, ecc.

import sys
import os
import tempfile
import base64
import shutil
import subprocess
import time
import random
import threading
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QIcon

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

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
FONT_MONO_FAMILY = "Consolas"
FONT_MONO = (FONT_MONO_FAMILY, 10)

# ---------------- Base64 music placeholder ----------------
BASE64_KEYGEN_MUSIC = """dGhlIGFybW9yIG9mIGdvZC4AAABieSBtYWt0b25lIG9mOiAgY2xhc3MmAi4AQAAAAAB4LXByZXNzaW9uJnN1cGVyc3RhcnMAAUIAQAAAAAAtAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOwAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4AQAAGADgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABQAQAAGAA4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAASAA4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAASAA4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAASAA5ncmVldHMgdG86IC0AAAAAAAAAAAAAAAAAAAAAAABveHlnZW5lci5uYXRhbjEuc3Bhcmt5AAAAAAAAAABvbWVnYXR3by5zZWZmcmVuLmF0bS4AAAAAAAAAAABnb2xkcHVzaC5sZWsuYW50aWJvZHkuAAAAAAAAAABzY29ycGlvLnplYy5zaG9vcG9vLgAAAAAAAAAAAABrb29sYWcud2hpenp0ZXIuZGFydS4AAAAAAAAAAAByZXB0aWxlLm1lbXBoZXJpYS4AAAAAAAAAAAAAAAB3YXJoYXdrLmtsZWZ6Lnp1bGxlLgAAAAAAAAAAAABsb29uaWUubWl0aHJpcy5mdW5uZWwuAAAAAAAAAAAtIDoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAABAgMEBQYHCAkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATS5LLgGsTwUBrIAAAR2EgQFohIEAAAAAAAAAAAAABAAAAAQAAAAAAAEdgAAAAAQAAAAEAAAAAAABrIweAAAEAAAABAAAAAAAAWiAAAAABAAAAAQAAAAAAAEdjB4AAAQAAAAEAAAAAAABrIAAAAAEAAAABAAAAAAAAWiMHgAABAAAAAQAAAAAAAFogAAAAAQAAAAEAAAAAAABrIweAAAEAAAABAAAAAAAAR2AAAAABAAAAAQAAAAAAAFojB4AAAQAAAAEAAAACgIBaIAAAAAEAAAABAAAAAoCAR2MHgAABAAAAAQAAAAKAgGsgAABDYQAAAAEAAAACgIBaIweAAAEAAAABAAB4EAAAeCAAAFAhAABfYQAAAAAAAAAAAAAAAQAAAAEAAAAAAABQIAAAAAEAAAABAAAAAAAAeCMHgAABAAAAAQAAAAAAAF9gAAAAAQAAAAEAAAAAAABQIweAAAEAAAABAAAAAAAAeCAAAAABAAAAAQAAAAAAAF9jB4AAAQAAAAEAAAAAAABfYAAAAAEAAAABAAAAAAAAeCMHgAABAAAAAQAAAAAAAFAgAAAAAQAAAAEAAAAAAABfYweAAAEAAAABAAAAAoCAX2AAAAABAAAAAQAAAAKAgFAjB4AAAQAAAAEAAAACgIB4IAAAAAEAAFohAAAAAoCAX2MHgAABAAAAAQAAjpAAAI6gAABfYQAAeCEAAAAAAAAAAAAAAAEAAAABAAAAAAAAX2AAAAABAAAAAQAAAAAAAI6jB4AAAQAAAAEAAAAAAAB4IAAAAAEAAAABAAAAAAAAX2MHgAABAAAAAQAAAAAAAI6gAAAAAQAAAAEAAAAAAAB4IweAAAEAAAABAAAAAAAAeCAAAAABAAAAAQAAAAAAAI6jB4AAAQAAAAEAAAAAAABfYAAAAAEAAAABAAAAAAAAX2MHgAABAAAAAQAAAAKAgHggAAAAAQAAAAEAAAACgICOoweAAAEAAAABAAAAAoCAjqAAAFohAAAAAQAAAAKAgHgjB4AAAQAAAAEAAKAQAACgIAAAayEAAH8hAAAAAAAAAAAAAAABAAAAAQAAAAAAAGsgAAAAAQAAAAEAAAAAAACgIweAAAEAAAABAAAAAAAAfyAAAAABAAAAAQAAAAAAAGsjB4AAAQAAAAEAAAAAAACgIAAAAAEAAAABAAAAAAAAfyMHgAABAAAAAQAAAAAAAH8gAAAAAQAAAAEAAAAAAACgIweAAAEAAAABAAAAAAAAayAAAAABAAAAAQAAAAAAAH8jB4AAAQAAAAEAAAACgIB/IAAAAAEAAAABAAAAAoCAoCMHgAABAAAAAQAAAAKAgKAgAAAAAQAAeCEAAAACgIBrIweAAAEAAAABAABrEAAAayAAAEdhIEBaISBAAAAAAAAAAAAAAQAAAAEAAAAAAABHYAAAAAEAAAABAAAAAAAAayMHgAABAAAAAQAAAAAAAFogAAAAAQAAAAEAAAAAAABHYweAAAEAAAABAAAAAAAAayAAAAABAAAAAQAAAAAAAFojB4AAAQAAAAEAAAAAAABaIAAAAAEAAAABAAAAAAAAayMHgAABAAAAAQAAAAAAAEdgAAAAAQAAAAEAAAAAAABaIweAAAEAAAABAAAAAoCAWiAAAAABAAAAAQAAAAKAgEdjB4AAAQAAAAEAAAACgIBrIAAAQ2EAAAABAAAAAoCAWiMHgAABAAAAAQAAeBAAAHggAABQIQAAX2EAAAAAAAAAAAAAAAEAAAABAAAAAAAAUCAAAAABAAAAAQAAAAAAAHgjB4AAAQAAAAEAAAAAAABfYAAAAAEAAAABAAAAAAAAUCMHgAABAAAAAQAAAAAAAHggAAAAAQAAAAEAAAAAAABfYweAAAEAAAABAAAAAAAAX2AAAAABAAAAAQAAAAAAAHgjB4AAAQAAAAEAAAAAAABQIAAAAAEAAAABAAAAAAAAX2MHgAABAAAAAQAAAAKAgF9gAAAAAQAAAAEAAAACgIBQIweAAAEAAAABAAAAAoCAeCAAAAABAABaIQAAAAKAgF9jB4AAAQAAAAEAAI6QAACOoAAAX2EAAHghAAAAAAAAAAAAAAABAAAAAQAAAAAAAF9gAAAAAQAAAAEAAAAAAACOoweAAAEAAAABAAAAAAAAeCAAAAABAAAAAQA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
"""  # se vuoi musica, incolla la base64 qui

def resource_path(relative_path):
    """Restituisce il percorso assoluto anche quando eseguito da EXE PyInstaller"""
    try:
        base_path = sys._MEIPASS  # path temporaneo in cui PyInstaller estrae i file
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ---------------- Math helpers (identici) ----------------
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

# build expression tree / find expression (identici a prima)
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

# ---------------- Parsing helpers & pruning (identici) ----------------
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

# ---------------- Worker thread as QThread with signals ----------------
class WorkerSignals(QObject):
    progress = pyqtSignal(int, int, int)  # processed, total, pct
    status = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

class CalculationWorker(QtCore.QThread):
    def __init__(self, all_values, mandatory, min_res, max_res, target_frac, tol, versione_completa):
        super().__init__()
        self.all_values = all_values
        self.mandatory = mandatory
        self.min_res = min_res
        self.max_res = max_res
        self.target_frac = target_frac
        self.tol = tol
        self.versione_completa = versione_completa
        self.signals = WorkerSignals()
        self._cancel = False

    def run(self):
        try:
            self._cancel = False
            multisets = multisets_with_mandatory(self.all_values, self.min_res, self.max_res, self.mandatory)
            total = len(multisets)
            if total == 0:
                self.signals.error.emit("Nessun multiset generato con i parametri inseriti.")
                self.signals.finished.emit([])
                return
            results=[]; seen=set(); processed=0
            max_checks = 10**12 if self.versione_completa else 100000
            for ms in multisets:
                if self._cancel:
                    break
                processed += 1
                if processed % 5 == 0 or processed == 1 or processed == total:
                    pct = int(processed/total*100)
                    self.signals.progress.emit(processed, total, pct)
                    self.signals.status.emit(f"Verifica {processed}/{total}...")
                numeric_list = [float(x) for x in ms]
                max_possible = sum(numeric_list)
                min_possible = harmonic_parallel_min(numeric_list)
                if float(self.target_frac) + self.tol < min_possible - 1e-9 or float(self.target_frac) - self.tol > max_possible + 1e-9:
                    continue
                key = canonical_key(ms)
                try:
                    reach = reachable_values_for_key(key)
                except RecursionError:
                    continue
                match = [v for v in reach if abs(float(v)-float(self.target_frac))<=self.tol]
                if not match:
                    continue
                chosen = min(match, key=lambda x: abs(float(x)-float(self.target_frac)))
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
                if not self.versione_completa and len(results) >= 40:
                    break
                if processed >= max_checks:
                    break
            self.signals.finished.emit(results)
        except Exception as e:
            self.signals.error.emit(str(e))

    def cancel(self):
        self._cancel = True

# ---------------- Audio thread (kept) ----------------
_audio_thread = None
_audio_stop_event = threading.Event()
_audio_tempfile = None
_music_flag = False

def _audio_play_loop_pyqt():
    global _audio_tempfile, _music_flag
    if not BASE64_KEYGEN_MUSIC or not BASE64_KEYGEN_MUSIC.strip():
        return
    if not PYGAME_AVAILABLE:
        # no QMessageBox here, caller will show
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

def start_audio_pyqt(enabled):
    global _audio_thread, _music_flag
    _music_flag = bool(enabled)
    _audio_stop_event.set()
    if _audio_thread and _audio_thread.is_alive():
        _audio_thread.join(timeout=0.5)
    _audio_stop_event.clear()
    if _music_flag:
        if not PYGAME_AVAILABLE:
            return False
        _audio_thread = threading.Thread(target=_audio_play_loop_pyqt, daemon=True)
        _audio_thread.start()
    return True

# ---------------- GUI principale PyQt6 ----------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(resource_path("icongg.ico")))
        self.setWindowTitle("Calcolatore abbinamenti OHM")
        self.resize(1200, 780)
        # central widget
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(4)

        # =========================
        # ASCII header (stile CableCalc con effetto casuale)
        # =========================
        def shrink_ascii_logo(ascii_logo, scale=0.7):
            lines = ascii_logo.rstrip("\n").splitlines()
            if not lines:
                return ""
            maxw = max(len(l) for l in lines)
            padded = [l.ljust(maxw) for l in lines]
            new_h = max(1, int(len(padded) * scale))
            new_w = max(1, int(maxw * scale))
            out_lines = []
            for y in range(new_h):
                src_y = min(len(padded) - 1, int(y / scale))
                src_line = padded[src_y]
                chars = []
                for x in range(new_w):
                    src_x = min(maxw - 1, int(x / scale))
                    chars.append(src_line[src_x])
                out_lines.append("".join(chars).rstrip())
            return "\n".join(out_lines)

        self.NEON_GREEN = "#23ff00"
        self.NEON_GREEN_DIM = "#0fa000"

        self.ORIGINAL_ASCII = r'''
  ::::::::::: :::    ::: ::::::::::          ::::::::  :::    :::   :::   :::   ::::    ::: ::::::::::: ::::    :::     ::: ::::::::::: ::::::::  ::::::::: 
     :+:     :+:    :+: :+:                :+:    :+: :+:    :+:  :+:+: :+:+:  :+:+:   :+:     :+:     :+:+:   :+:   :+: :+:   :+:    :+:    :+: :+:    :+: 
    +:+     +:+    +:+ +:+                +:+    +:+ +:+    +:+ +:+ +:+:+ +:+ :+:+:+  +:+     +:+     :+:+:+  +:+  +:+   +:+  +:+    +:+    +:+ +:+    +:+  
   +#+     +#++:++#++ +#++:++#           +#+    +:+ +#++:++#++ +#+  +:+  +#+ +#+ +:+ +#+     +#+     +#+ +:+ +#+ +#++:++#++: +#+    +#+    +:+ +#++:++#:    
  +#+     +#+    +#+ +#+                +#+    +#+ +#+    +#+ +#+       +#+ +#+  +#+#+#     +#+     +#+  +#+#+# +#+     +#+ +#+    +#+    +#+ +#+    +#+    
 #+#     #+#    #+# #+#                #+#    #+# #+#    #+# #+#       #+# #+#   #+#+#     #+#     #+#   #+#+# #+#     #+# #+#    #+#    #+# #+#    #+#     
###     ###    ### ##########          ########  ###    ### ###       ### ###    #### ########### ###    #### ###     ### ###     ########  ###    ###      
'''

        SMALL_LOGO = shrink_ascii_logo(self.ORIGINAL_ASCII, scale=1.0)
        self.logo_label = QtWidgets.QLabel(SMALL_LOGO)
        self.logo_label.setFont(QtGui.QFont("Consolas", 9, QtGui.QFont.Weight.Bold))
        self.logo_label.setStyleSheet(
            f"color:{self.NEON_GREEN}; background-color:black; padding-left: 10px;"
        )
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(self.logo_label)

        # --- Effetto "pulse casuale" (stile keygen originale) ---
        import random

        def random_pulse_logo():
            color = random.choice([self.NEON_GREEN, self.NEON_GREEN_DIM])
            # 🔧 manteniamo SEMPRE il padding sinistro anche quando cambia il colore
            self.logo_label.setStyleSheet(
                f"color:{color}; background-color:black; padding-left: 10px;"
            )
            next_delay = random.randint(200, 800)
            QtCore.QTimer.singleShot(next_delay, random_pulse_logo)

        # avvia il primo tick
        QtCore.QTimer.singleShot(400, random_pulse_logo)


        # =========================
        # AREA PRINCIPALE
        # =========================
        area = QtWidgets.QHBoxLayout()
        area.setContentsMargins(6, 0, 6, 6)
        main_layout.addLayout(area)

        # left pane (controls)
        left_widget = QtWidgets.QWidget()
        left_widget.setFixedWidth(380)
        left_widget.setStyleSheet(f"background:{PANEL_BG};")
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(6)
        area.addWidget(left_widget)

        # right pane (table + canvas)
        right_widget = QtWidgets.QWidget()
        right_widget.setStyleSheet(f"background:{PANEL_BG};")
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(6)
        area.addWidget(right_widget, 1)



        # --- left controls construction matching il layout tkinter ---
        def make_label(text):
            lbl = QtWidgets.QLabel(text)
            lbl.setStyleSheet(f"color:{NEON_GREEN}; background:{PANEL_BG}; font-family:{FONT_MONO_FAMILY};")
            return lbl

        def make_entry(default=""):
            e = QtWidgets.QLineEdit()
            e.setText(default)
            e.setStyleSheet(f"background:{ENTRY_BG}; color:{NEON_GREEN}; border:1px solid {BORDER_COLOR}; font-family:{FONT_MONO_FAMILY}; padding:4px;")
            return e

        std_values = [0.5,1,2,3,4,6,8,16]
        self.std_checkboxes = {}

        vals_label = make_label("Valori standard:")
        left_layout.addWidget(vals_label)
        vals_grid = QtWidgets.QGridLayout()
        vals_grid.setHorizontalSpacing(8); vals_grid.setVerticalSpacing(4)
        left_layout.addLayout(vals_grid)
        for i, v in enumerate(std_values):
            cb = QtWidgets.QCheckBox(f"{v} Ω")
            cb.setStyleSheet(f"color:{NEON_GREEN}; background:{PANEL_BG};")
            cb.setChecked(True if v==4 else False)
            vals_grid.addWidget(cb, i//4, i%4)
            self.std_checkboxes[v] = cb

        self.custom_entry = make_entry("")
        left_layout.addWidget(make_label("Valori personalizzati (es: 2.2,5.6):"))
        left_layout.addWidget(self.custom_entry)

        self.mandatory_entry = make_entry("4,4")
        left_layout.addWidget(make_label("Resistenze obbligatorie (es: 4,4):"))
        left_layout.addWidget(self.mandatory_entry)

        # --- Min / Max Impedance controls (clean, single block) ---
        minmax_widget = QtWidgets.QWidget()
        minmax_layout = QtWidgets.QHBoxLayout(minmax_widget)
        minmax_layout.setContentsMargins(0, 0, 0, 0)
        minmax_layout.setSpacing(6)
        left_layout.addWidget(minmax_widget)

        lbl_min = make_label("Min:")
        minmax_layout.addWidget(lbl_min)

        self.min_res_spin = QtWidgets.QSpinBox()
        self.min_res_spin.setRange(2, 12)
        self.min_res_spin.setValue(2)
        self.min_res_spin.setMinimumWidth(90)
        self.min_res_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.min_res_spin.setStyleSheet(f"""
            QSpinBox {{
                background:{ENTRY_BG};
                color:{NEON_GREEN};
                border:1px solid {BORDER_COLOR};
                font-family:{FONT_MONO_FAMILY};
                padding-right: 20px; /* spazio per le frecce */
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 16px;
                background:{HEADING_BG};
                border: 1px solid {BORDER_COLOR};
            }}
        """)
        minmax_layout.addWidget(self.min_res_spin)

        lbl_max = make_label("Max:")
        minmax_layout.addWidget(lbl_max)

        self.max_res_spin = QtWidgets.QSpinBox()
        self.max_res_spin.setRange(2, 12)
        self.max_res_spin.setValue(8)
        self.max_res_spin.setMinimumWidth(90)
        self.max_res_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.max_res_spin.setStyleSheet(f"""
            QSpinBox {{
                background:{ENTRY_BG};
                color:{NEON_GREEN};
                border:1px solid {BORDER_COLOR};
                font-family:{FONT_MONO_FAMILY};
                padding-right: 20px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 16px;
                background:{HEADING_BG};
                border: 1px solid {BORDER_COLOR};
            }}
        """)
        minmax_layout.addWidget(self.max_res_spin)

        minmax_layout.addStretch()

        # --- Target impedance entry ---
        left_layout.addWidget(make_label("Target (Ω):"))
        self.target_entry = make_entry("2.0")
        left_layout.addWidget(self.target_entry)

        self.tol_entry = make_entry("0.05")
        left_layout.addWidget(make_label("Tolleranza (Ω):"))
        left_layout.addWidget(self.tol_entry)
        left_layout.addWidget(make_label("Potenza ingresso (W):"))
        self.power_entry = make_entry("100")  # default 100 W
        left_layout.addWidget(self.power_entry)

        # checkboxes versione_completa e musica
        self.versione_completa_cb = QtWidgets.QCheckBox("Versione completa (off = max 40 results)")
        self.versione_completa_cb.setStyleSheet(f"color:{NEON_GREEN}; background:{PANEL_BG};")
        left_layout.addWidget(self.versione_completa_cb)

        self.music_cb = QtWidgets.QCheckBox("Musica")
        self.music_cb.setStyleSheet(f"color:{NEON_GREEN}; background:{PANEL_BG};")
        self.music_cb.setChecked(True)
        left_layout.addWidget(self.music_cb)
        self.music_cb.stateChanged.connect(self.toggle_music)


        # status label
        self.status_label = QtWidgets.QLabel("Pronto.")
        self.status_label.setStyleSheet(f"color:{NEON_GREEN}; font-family:{FONT_MONO_FAMILY}; font-style:italic;")
        left_layout.addWidget(self.status_label)

        # pulsating entry effect simulation (timer)
        def pulse_entries():
            for widget in [self.custom_entry, self.mandatory_entry, self.target_entry, self.tol_entry]:
                if random.random() < 0.25:
                    widget.setStyleSheet(f"background:{ENTRY_BG}; color:{NEON_GREEN}; border:1px solid {NEON_GREEN if random.random()<0.5 else BORDER_COLOR}; font-family:{FONT_MONO_FAMILY}; padding:4px;")
                else:
                    widget.setStyleSheet(f"background:{ENTRY_BG}; color:{NEON_GREEN}; border:1px solid {BORDER_COLOR}; font-family:{FONT_MONO_FAMILY}; padding:4px;")
            QtCore.QTimer.singleShot(600, pulse_entries)
        pulse_entries()

        # Progress bar and text (above CALCOLA)
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(14)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {BORDER_COLOR};
                background: {ENTRY_BG};
                height: 14px;
            }}
            QProgressBar::chunk {{
                background: {NEON_GREEN};
            }}
        """)
        left_layout.addWidget(self.progress_bar)
        self.progress_text = QtWidgets.QLabel("")
        self.progress_text.setStyleSheet(f"color:{NEON_GREEN}; font-family:{FONT_MONO_FAMILY};")
        left_layout.addWidget(self.progress_text)

        # cancel button (Annulla)
        self.cancel_btn = QtWidgets.QPushButton("Annulla")
        self.cancel_btn.setStyleSheet(f"background:{ENTRY_BG}; color:{NEON_GREEN}; border:0; font-family:{FONT_MONO_FAMILY};")
        self.cancel_btn.clicked.connect(self.cancel_calculation)
        left_layout.addWidget(self.cancel_btn)

        # CALCOLA button (progress sopra)
        self.calc_btn = QtWidgets.QPushButton(">>> CALCOLA <<<")
        self.calc_btn.setStyleSheet(f"background:{ENTRY_BG}; color:{NEON_GREEN}; font-family:{FONT_MONO_FAMILY}; font-weight:bold;")
        self.calc_btn.clicked.connect(self.on_calculate)
        left_layout.addWidget(self.calc_btn)

        # export / clear buttons
        btns_widget = QtWidgets.QWidget()
        btns_layout = QtWidgets.QVBoxLayout(btns_widget)
        btns_layout.setContentsMargins(0,0,0,0)
        left_layout.addWidget(btns_widget)
        btn_azzera = QtWidgets.QPushButton("Azzera")
        btn_azzera.setStyleSheet(f"background:{ENTRY_BG}; color:{NEON_GREEN}; border:0;")
        btn_azzera.clicked.connect(self.clear_all)
        btns_layout.addWidget(btn_azzera)
        btn_export = QtWidgets.QPushButton("Esporta PNG")
        btn_export.setStyleSheet(f"background:{ENTRY_BG}; color:{NEON_GREEN}; border:0;")
        btn_export.clicked.connect(self.export_png)
        btns_layout.addWidget(btn_export)

        left_layout.addStretch()

        # --- right: treeview + matplotlib canvas ---
        # border wrap to emulate neon border
        border_wrap = QtWidgets.QFrame()
        border_wrap.setStyleSheet(f"background:{NEON_GREEN}; border-radius:6px;")
        right_layout.addWidget(border_wrap, 1)
        border_layout = QtWidgets.QVBoxLayout(border_wrap)
        border_layout.setContentsMargins(4,4,4,4)

        table_frame = QtWidgets.QFrame()
        table_frame.setStyleSheet(f"background:{PANEL_BG};")
        table_layout = QtWidgets.QVBoxLayout(table_frame)
        table_layout.setContentsMargins(2,2,2,2)
        border_layout.addWidget(table_frame, 1)

        # Treeview (QTreeWidget)
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Speakers", "Expr", "Value"])
        self.tree.setStyleSheet(f"""
            QTreeWidget {{ background:{ENTRY_BG}; color:{NEON_GREEN}; font-family:{FONT_MONO_FAMILY}; }}
            QHeaderView::section {{ background:{HEADING_BG}; color:{NEON_GREEN}; font-family:{FONT_MONO_FAMILY}; font-weight:bold; }}
            QTreeWidget::item:selected {{ background:{HEADING_BG}; color:{NEON_GREEN}; }}
        """)
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tree.setColumnWidth(0, 180)
        self.tree.setColumnWidth(2, 120)
        self.tree.itemSelectionChanged.connect(self.on_select)
        table_layout.addWidget(self.tree)

        # matplotlib canvas for drawing networks
        self.canvas_widget_frame = QtWidgets.QFrame()
        self.canvas_widget_frame.setStyleSheet(f"background:{PANEL_BG};")
        border_layout.addWidget(self.canvas_widget_frame, 1)
        canvas_layout = QtWidgets.QVBoxLayout(self.canvas_widget_frame)
        canvas_layout.setContentsMargins(0,0,0,0)

        self._fig = plt.Figure(figsize=(6,3), facecolor='black', dpi=100)
        self._ax = self._fig.add_subplot(111); self._ax.set_facecolor('black')
        self.canvas = FigureCanvas(self._fig)
        canvas_layout.addWidget(self.canvas)

        # internal state
        self.results_list = []
        self.worker = None

        # start audio if requested
        if self.music_cb.isChecked():
            ok = start_audio_pyqt(True)
            if not ok:
                QtWidgets.QMessageBox.warning(self, "Musica disabilitata", "Installa pygame per abilitare la musica")

        # graceful close
        self._closing = False

    # ---------------- UI helper functions ----------------
    def set_status(self, text):
        self.status_label.setText(text)

    def cancel_calculation(self):
        if self.worker and isinstance(self.worker, CalculationWorker):
            self.worker.cancel()
            self.set_status("Cancellazione richiesta...")
    
    def toggle_music(self, state):
        """Abilita o disabilita la musica in base allo stato della checkbox."""
        enabled = bool(state)
        ok = start_audio_pyqt(enabled)
        if not ok and enabled:
            QtWidgets.QMessageBox.warning(
                self, "Musica disabilitata", "Installa pygame per abilitare la musica"
            )


    def clear_all(self):
        self.tree.clear()
        self.set_status("Pulito.")
        self.results_list = []

    def export_png(self):
        """Esporta lo schema attualmente visualizzato come immagine PNG usando il nome dell'espressione selezionata."""
        try:
            current_fig = getattr(self.canvas, "figure", None)
            if current_fig is None:
                QMessageBox.warning(self, "Errore", "Nessuno schema disponibile da esportare.")
                return

            # Prende l'item selezionato
            sel = self.tree.selectedItems()
            if sel:
                expr_name = sel[0].text(1).replace(" ", "_")  # seconda colonna = expr
            else:
                expr_name = "schema"  # default se niente selezionato

            # Finestra di dialogo per scegliere cartella
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Salva schema come PNG", expr_name + ".png", "Immagine PNG (*.png)"
            )
            if not path:
                return

            if not path.lower().endswith(".png"):
                path += ".png"

            # Salva la figura
            current_fig.savefig(path, dpi=300, facecolor='black')
            QMessageBox.information(self, "Esportazione completata", f"Schema salvato come:\n{path}")

        except Exception as e:
            QMessageBox.warning(self, "Errore durante l'esportazione", str(e))

    # plotting functions (conversion diretta del matplotlib tree plot)
    def plot_tree_matplotlib(self, node, title=None):
        if node is None:
            return None

        # Recupera potenza di ingresso (W)
        try:
            input_watts = float(self.power_entry.text())
        except Exception:
            input_watts = 0.0

        # Assegna posizioni per i nodi
        positions = {}; labels = {}; counter = {'x': 0}
        def assign(n, depth=0):
            t = n[0]
            if t == 'leaf':
                x = counter['x']
                positions[id(n)] = (x, -depth)
                labels[id(n)] = f"{float(n[1]):g} Ω"
                counter['x'] += 1
                return positions[id(n)]
            left = n[1]; right = n[2]
            lpos = assign(left, depth + 1)
            rpos = assign(right, depth + 1)
            x = (lpos[0] + rpos[0]) / 2.0
            positions[id(n)] = (x, -depth)
            labels[id(n)] = t  # "S" o "P"
            return positions[id(n)]

        assign(node, depth=0)

        # --- Calcolo corrente e potenza per ogni foglia ---
        # Ricava impedenze effettive per ogni nodo
        def get_impedance(n):
            t = n[0]
            if t == 'leaf':
                return float(n[1])
            a = get_impedance(n[1])
            b = get_impedance(n[2])
            if t == 'S':  # serie
                return a + b
            else:         # parallelo
                return 1.0 / (1.0 / a + 1.0 / b)

        total_R = get_impedance(node)
        if total_R <= 0:
            total_R = 1e-9

        # Tensione totale equivalente
        V_in = (input_watts * total_R) ** 0.5

        # Funzione per calcolare la potenza su ogni leaf
        leaf_powers = {}
        def compute_power(n, V):
            t = n[0]
            if t == 'leaf':
                R = float(n[1])
                P = V * V / R
                leaf_powers[id(n)] = P
                return
            if t == 'S':  # serie → stessa corrente
                aR = get_impedance(n[1]); bR = get_impedance(n[2])
                I = V / (aR + bR)
                compute_power(n[1], I * aR)
                compute_power(n[2], I * bR)
            else:  # parallelo → stessa tensione
                compute_power(n[1], V)
                compute_power(n[2], V)

        compute_power(node, V_in)

        # --- Disegno grafico ---
        fig = plt.Figure(facecolor='black')
        ax_local = fig.add_subplot(111)
        ax_local.set_facecolor('black')

        def draw(n):
            nid = id(n)
            x, y = positions[nid]
            t = n[0]
            if t != 'leaf':
                left = n[1]; right = n[2]
                branch_color = NEON_GREEN if t == 'S' else "white"
                for child in (left, right):
                    cx, cy = positions[id(child)]
                    ax_local.plot([x, cx], [y, cy], color=branch_color, linewidth=1.5)
                    draw(child)
            ax_local.scatter([x], [y], s=100, color=NEON_GREEN)
            if t == 'leaf':
                watts = leaf_powers.get(id(n), 0)
                ax_local.text(
                    x, y,
                    f"{labels[nid]}\n{watts:.1f}W",
                    color='black', fontsize=8, ha='center', va='center',
                    backgroundcolor=NEON_GREEN
                )
            else:
                ax_local.text(
                    x, y,
                    labels[nid],
                    color='black', fontsize=8, ha='center', va='center',
                    backgroundcolor=NEON_GREEN
                )

        draw(node)
        ax_local.axis('off')
        if title:
            ax_local.set_title(title, color=NEON_GREEN)
        fig.tight_layout()
        return fig

    def update_canvas_figure(self, fig_local):
        """
        FIX: assicuro che la figura sia ridimensionata alla dimensione del canvas e venga ridisegnata
        immediatamente (evitando la necessità di ridimensionare manualmente la finestra).
        """
        if fig_local is None:
            return
        try:
            # cerco il dpi della figura; se assente uso 100
            try:
                dpi = getattr(fig_local, "dpi", 100) or 100
            except Exception:
                dpi = 100
            # dimensioni pixel del widget canvas
            w = max(self.canvas.width(), 200)
            h = max(self.canvas.height(), 120)
            # imposta la dimensione della figura in pollici per adattarla al canvas
            try:
                fig_local.set_size_inches(w / dpi, h / dpi)
            except Exception:
                pass
            # assegna e disegna immediatamente
            self.canvas.figure = fig_local
            self.canvas.draw()
            self.canvas.repaint()
            QtWidgets.QApplication.processEvents()
        except Exception:
            pass

    # ---------------- Worker handling and UI callbacks ----------------
    def on_calculate(self):
        # gather selected values
        selected = []
        try:
            for v, cb in self.std_checkboxes.items():
                if cb.isChecked():
                    selected.append(Fraction(str(v)))
        except Exception:
            selected = []
        custom = parse_vals(self.custom_entry.text())
        all_values = sorted(set(selected + custom), key=lambda x: float(x)) if (selected or custom) else []
        if not all_values:
            QtWidgets.QMessageBox.critical(self, "Errore", "Seleziona almeno un valore o inserisci valori personalizzati.")
            return
        mandatory = parse_vals(self.mandatory_entry.text())
        try:
            min_res = int(self.min_res_spin.value()); max_res = int(self.max_res_spin.value())
        except Exception:
            QtWidgets.QMessageBox.critical(self, "Errore", "Min/Max non validi"); return
        try:
            target_frac = Fraction(str(float(self.target_entry.text()))).limit_denominator()
        except Exception:
            QtWidgets.QMessageBox.critical(self, "Errore", "Target non valido"); return
        try:
            tol = float(self.tol_entry.text())
        except Exception:
            tol = 0.05
        versione_completa = bool(self.versione_completa_cb.isChecked())
        if versione_completa and max_res >= 9:
            resp = QtWidgets.QMessageBox.question(self, "Attenzione", "La versione completa con molte resistenze può richiedere molto tempo. Continuare?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if resp != QtWidgets.QMessageBox.StandardButton.Yes:
                return
        # start worker thread
        self.set_status("Preparazione calcolo...")
        self.progress_bar.setValue(0)
        self.progress_text.setText("0/0 (0%)")
        # ensure any previous worker cancelled
        if self.worker and isinstance(self.worker, CalculationWorker):
            self.worker.cancel()
            # wait briefly
            time.sleep(0.05)
        self.worker = CalculationWorker(all_values, mandatory, min_res, max_res, target_frac, tol, versione_completa)
        self.worker.signals.progress.connect(self.handle_progress)
        self.worker.signals.status.connect(self.set_status)
        self.worker.signals.finished.connect(self.show_results)
        self.worker.signals.error.connect(lambda msg: QtWidgets.QMessageBox.information(self, "Info", msg))
        self.worker.start()

    def handle_progress(self, processed, total, pct):
        # update progress bar & text
        if total > 0:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(processed)
            self.progress_text.setText(f"{pct}% - {processed}/{total}")

    def show_results(self, results):
        self.results_list = results
        self.tree.clear()
        for idx, r in enumerate(results):
            speakers_str=[]
            for x in r['speakers']:
                fx=float(x)
                speakers_str.append(str(int(round(fx))) if abs(fx-round(fx))<1e-9 else f"{fx:g}")
            it = QtWidgets.QTreeWidgetItem([",".join(speakers_str), r['expr'], f"{r['value']:.6f}"])
            self.tree.addTopLevelItem(it)
        self.set_status(f"Trovate {len(results)} soluzioni.")
        if results and getattr(self, "canvas", None):
            node = results[0]['tree']
            fig_local = self.plot_tree_matplotlib(node, title=results[0]['expr'])
            self.update_canvas_figure(fig_local)
        # reset progress UI
        self.progress_text.setText("")
        self.progress_bar.setValue(0)

    def on_select(self):
        sel = self.tree.selectedItems()
        if not sel:
            return
        try:
            idx = self.tree.indexOfTopLevelItem(sel[0])
        except Exception:
            return
        if idx < 0 or idx >= len(self.results_list):
            return
        entry = self.results_list[idx]
        node = entry.get('tree')
        fig_local = self.plot_tree_matplotlib(node, title=entry['expr'])
        self.update_canvas_figure(fig_local)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        # graceful close
        try:
            if self.worker and isinstance(self.worker, CalculationWorker):
                self.worker.cancel()
                self.worker.wait(200)
        except Exception:
            pass
        try:
            _audio_stop_event.set()
            time.sleep(0.05)
        except Exception:
            pass
        event.accept()

# ---------------- main ----------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resource_path("icongg.ico")))

    # ---------------- FIX CHECKBOX INDICATOR (STILE GLOBALE) ----------------
    # Questo stylesheet forza le "spunte" verdi e rende visibile l'indicatore con bordo neon.
    app.setStyleSheet(f"""
        QCheckBox {{
            color: {NEON_GREEN};
            background: {PANEL_BG};
            font-family: {FONT_MONO_FAMILY};
        }}
        QCheckBox::indicator {{
            width: 14px;
            height: 14px;
            border: 1px solid {BORDER_COLOR};
            border-radius: 2px;
            background-color: {ENTRY_BG};
        }}
        QCheckBox::indicator:checked {{
            background-color: {NEON_GREEN};
            border: 1px solid {NEON_GREEN_DIM};
        }}
        QCheckBox::indicator:disabled {{
            background-color: #002200;
        }}
    """)

    w = MainWindow()
    w.show()
    QtWidgets.QApplication.processEvents()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
