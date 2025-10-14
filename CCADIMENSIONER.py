import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import time
import base64
import tempfile
import os
import atexit
import shutil
import subprocess
import sys
import threading

def resource_path(relative_path):
    """Restituisce il percorso corretto per il file, anche se è dentro un exe PyInstaller"""
    try:
        # PyInstaller crea questa variabile temporanea
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Prova a importare pygame per la musica
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

# -----------------------
# BASE64 DATA (musica .xm incorporata)
# -----------------------
# Sostituisci il contenuto tra le triple virgolette con il contenuto di xm_base64.txt
# (oppure rimuovi questo blocco e decodifica direttamente dal file con open("xm_base64.txt").read())
BASE64_XM = r"""
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
""".strip()

# -----------------------
# Funzione per ridurre ASCII logo ~70% (nearest-neighbour)
# (la manteniamo perché nello script precedente veniva usata)
# -----------------------
def shrink_ascii_logo(ascii_logo, scale=0.7):
    lines = ascii_logo.rstrip("\n").splitlines()
    if not lines:
        return ""
    maxw = max(len(l) for l in lines)
    # pad lines to same width
    padded = [l.ljust(maxw) for l in lines]
    new_h = max(1, int(len(padded) * scale))
    new_w = max(1, int(maxw * scale))
    out_lines = []
    for y in range(new_h):
        src_y = min(len(padded)-1, int(y / scale))
        src_line = padded[src_y]
        chars = []
        for x in range(new_w):
            src_x = min(maxw-1, int(x / scale))
            chars.append(src_line[src_x])
        out_lines.append("".join(chars).rstrip())
    return "\n".join(out_lines)

# -----------------------
# Funzione calcola (UNICA e INVARIATA)
# -----------------------
def calcola():
    try:
        # Lettura input
        lunghezza = float(entry_lunghezza.get().replace(",", "."))
        potenza = float(entry_potenza.get().replace(",", "."))
        classe = combo_classe.get()
        delta_v = float(entry_deltav.get().replace(",", "."))
        tensione = float(entry_tensione.get().replace(",", "."))
        capacita_batt = float(entry_batteria.get().replace(",", "."))
        alternatore_A = float(entry_alternatore.get().replace(",", "."))
        peukert = float(entry_peukert.get().replace(",", "."))
        utilizzo_text = combo_utilizzo.get()

        utilizzo = float(utilizzo_text.split("%")[0].strip()) / 100.0

        # Efficienza per classe
        eff_dict = {"A":0.25, "AB":0.55, "D":0.85, "T":0.80, "G":0.70, "H":0.80}
        if classe not in eff_dict:
            messagebox.showerror("Errore", "Seleziona una classe valida.")
            return
        eff = eff_dict[classe]

        # Metodo massa
        mass_opt = massa_var.get()
        fattore_massa = 2.0 if mass_opt == "battery" else 1.3

        # Calcoli base
        lung_eff = lunghezza * fattore_massa
        rho = 0.0175  # resistività rame (Ω·mm²/m)
        corrente = potenza / (tensione * eff) * utilizzo
        if corrente == 0:
            messagebox.showerror("Errore", "Il valore di utilizzo selezionato è 0%.")
            return

        r_max = delta_v / corrente
        sezione = (rho * lung_eff) / r_max
        metri_equivalenti = lung_eff

        # Condensatore consigliato (in base alla potenza RMS)
        farad = round((potenza / 100) * 0.03, 2)

        # --- AUTONOMIA BATTERIA CON LEGGE DI PEUKERT ---
        def autonomia(capacita, corrente, k):
            if corrente <= 0:
                return 0
            h_nom = 20.0  # riferimento C20
            t = h_nom * (capacita / (corrente * h_nom)) ** k
            return t

        # --- Formattazione ore/minuti ---
        def formatta_autonomia(ore):
            if ore == "∞ (alternatore sufficiente)":
                return ore
            if ore <= 0:
                return "0 min"
            if ore < 1:
                return f"{ore*60:.0f} min"
            else:
                h = int(ore)
                m = int((ore - h) * 60)
                return f"{h}h {m}m"

        corrente_12v = potenza / (12 * eff) * utilizzo
        autonomia_spento_h = autonomia(capacita_batt, corrente_12v, peukert)
        autonomia_spento = formatta_autonomia(autonomia_spento_h)

        corrente_14v = potenza / (14.4 * eff) * utilizzo
        if alternatore_A >= corrente_14v:
            autonomia_acceso = "∞ (alternatore sufficiente)"
        else:
            corrente_mancante = corrente_14v - alternatore_A
            autonomia_acceso_h = autonomia(capacita_batt, corrente_mancante, peukert)
            autonomia_acceso = formatta_autonomia(autonomia_acceso_h)

        # --- CORRENTE RESIDUA ALTERNATORE ---
        corrente_residua = alternatore_A - corrente
        if corrente_residua < 0:
            residuo_msg = f"❌ Corrente residua alternatore: {corrente_residua:.1f} A"
        elif corrente_residua < 20:
            residuo_msg = f"⚠️ Corrente residua alternatore: +{corrente_residua:.1f} A"
        else:
            residuo_msg = f"✅ Corrente residua alternatore: +{corrente_residua:.1f} A"

        # --- VALUTAZIONE ALTERNATORE ---
        margine = alternatore_A - corrente
        if margine >= 40:
            alt_msg = "✅ Alternatore adeguato al carico previsto."
        elif 0 < margine < 40:
            alt_msg = "⚠️ Alternatore vicino al limite: valuta upgrade o batteria aggiuntiva."
        else:
            alt_msg = "❌ Alternatore insufficiente: necessario maggiorarlo e maggiorarne il cavo."

        # --- VALUTAZIONE BATTERIA ---
        if corrente < 60:
            batt_msg = "✅ Batteria sufficiente per l’impianto."
        elif 60 <= corrente <= 100:
            batt_msg = "⚠️ Corrente elevata: valuta l’aggiunta di una seconda batteria."
        else:
            batt_msg = "❌ Corrente molto alta: consigliata una batteria aggiuntiva."

        crest_factor = 10 * math.log10(1 / utilizzo) if utilizzo > 0 else 0

        # --- RISULTATI ---
        spieg = (
            "Nota: 'utilizzo realistico' rappresenta la percentuale di tempo in cui l’amplificatore eroga potenza.\n"
            "Un valore più basso indica musica più dinamica e assorbimento medio minore.\n\n"
        )

        result = (
            f"{spieg}"
            f"--- Calcolo per UTILIZZO REALISTICO = {utilizzo*100:.0f}% ---\n"
            f"Crest Factor ≈ {crest_factor:.1f} dB\n"
            f"Classe amplificatore: {classe} (efficienza {eff*100:.0f}%)\n"
            f"Corrente stimata: {corrente:.1f} A\n"
            f"Sezione minima teorica: {sezione:.2f} mm²\n"
            f"Metri di cavo equivalenti considerati: {metri_equivalenti:.1f} m\n\n"
            f"Condensatore consigliato: {farad} F\n"
            f"(Basato sulla potenza RMS totale, indipendente dall’utilizzo realistico)\n\n"
            f"Efficienza batteria (Peukert): {peukert}\n"
            f"Capacità batteria: {capacita_batt:.0f} Ah\n"
            f"Autonomia stimata (pieno volume continuo):\n"
            f" - Motore spento (12 V): {autonomia_spento}\n"
            f" - Motore acceso (14.4 V): {autonomia_acceso}\n\n"
            f"{residuo_msg}\n\n"
            f"Alternatore: {alternatore_A:.0f} A nominali\n\n"
            f"{batt_msg}\n{alt_msg}"
        )

        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Errore", str(e))

# -----------------------
# Musica: decodifica base64 -> file xm -> converti con ffmpeg -> play/pause toggle con fallback
# -----------------------
MUSIC_TEMP_PATH = None
MUSIC_WAV_PATH = None
external_player_proc = None
music_on = False

def prepare_music_from_base64_string():
    global MUSIC_TEMP_PATH, MUSIC_WAV_PATH
    try:
        cleaned = "".join(BASE64_XM.split())
        raw = base64.b64decode(cleaned)
    except Exception as ex:
        return False, f"Errore decodifica base64: {ex}"

    try:
        # scrivi xm temporaneo
        fd, temp_path = tempfile.mkstemp(prefix="keygen_theme_", suffix=".xm")
        os.close(fd)
        with open(temp_path, "wb") as outf:
            outf.write(raw)
        MUSIC_TEMP_PATH = temp_path
    except Exception as ex:
        return False, f"Errore scrittura file temporaneo: {ex}"

    # prova a convertire subito in WAV tramite ffmpeg (se disponibile)
    if shutil.which("ffmpeg"):
        ok, info = convert_xm_to_wav_with_ffmpeg(MUSIC_TEMP_PATH)
        if ok:
            return True, MUSIC_WAV_PATH
        else:
            # se conversione fallisce, ritorniamo comunque OK perché potremmo provare fallback player
            return True, MUSIC_TEMP_PATH
    else:
        # non c'è ffmpeg; ritorniamo il percorso xm per i fallback esterni
        return True, MUSIC_TEMP_PATH

def convert_xm_to_wav_with_ffmpeg(xm_path):
    global MUSIC_WAV_PATH
    if not shutil.which("ffmpeg"):
        return False, "ffmpeg non trovato"
    try:
        fd, wav_path = tempfile.mkstemp(prefix="keygen_theme_", suffix=".wav")
        os.close(fd)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", xm_path, wav_path]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if proc.returncode == 0 and os.path.exists(wav_path):
            MUSIC_WAV_PATH = wav_path
            return True, wav_path
        else:
            return False, f"ffmpeg errore: {proc.stderr.decode(errors='ignore')}"
    except Exception as ex:
        return False, str(ex)

def start_music():
    global music_on, external_player_proc, MUSIC_WAV_PATH
    # assicurati che il file xm sia pronto
    if MUSIC_TEMP_PATH is None:
        ok, info = prepare_music_from_base64_string()
        if not ok:
            messagebox.showwarning("Musica", f"Non posso preparare la musica: {info}")
            return

    # 1) tentativo pygame diretto su .xm
    if PYGAME_AVAILABLE:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(MUSIC_TEMP_PATH)
            pygame.mixer.music.set_volume(0.45)
            pygame.mixer.music.play(-1)
            music_on = True
            music_toggle_btn.configure(text="Musica: ON (clic per OFF)", bg="#002200")
            return
        except Exception as e:
            # pygame non riesce a caricare XM direttamente; proviamo conversione
            print("pygame non ha caricato XM direttamente:", e)

        # 2) se ffmpeg disponibile convertiamo e riproduciamo via pygame
        ok, info = convert_xm_to_wav_with_ffmpeg(MUSIC_TEMP_PATH)
        if ok and MUSIC_WAV_PATH:
            try:
                pygame.mixer.music.load(MUSIC_WAV_PATH)
                pygame.mixer.music.set_volume(0.45)
                pygame.mixer.music.play(-1)
                music_on = True
                music_toggle_btn.configure(text="Musica: ON (clic per OFF)", bg="#002200")
                return
            except Exception as e:
                print("Errore riproduzione WAV con pygame:", e)
        else:
            print("Conversione ffmpeg non riuscita o non disponibile:", info)

    # 3) fallback: proviamo player esterno in ordine timidity, ffplay
    for player in ("timidity", "ffplay"):
        path = shutil.which(player)
        if path:
            try:
                if player == "timidity":
                    external_player_proc = subprocess.Popen([path, MUSIC_TEMP_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:  # ffplay
                    external_player_proc = subprocess.Popen([path, "-nodisp", "-autoexit", "-loop", "0", MUSIC_TEMP_PATH],
                                                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                music_on = True
                music_toggle_btn.configure(text=f"Musica: ON (player {player}) - clic per OFF", bg="#002200")
                return
            except Exception as e:
                print(f"Errore avvio player {player}:", e)
                external_player_proc = None

    # se arriviamo qui, non siamo riusciti
    messagebox.showwarning("Musica", "Impossibile riprodurre la musica: pygame/ffmpeg/timidity/ffplay non disponibili o non funzionanti.")

def stop_music():
    global music_on, external_player_proc
    # stop pygame
    if PYGAME_AVAILABLE:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
    # stop external player
    if external_player_proc:
        try:
            external_player_proc.terminate()
        except Exception:
            try:
                external_player_proc.kill()
            except Exception:
                pass
        external_player_proc = None
    music_on = False
    music_toggle_btn.configure(text="Musica: OFF (clic per ON)", bg="#220000")

def toggle_music():
    global music_on
    if music_on:
        stop_music()
    else:
        start_music()

# -----------------------
# GUI (retro keygen green) - INTERFACCIA DA MANTENERE ESATTAMENTE
# -----------------------
root = tk.Tk()
root.title("Calcolo sezione cavi Car Audio")
root.geometry("820x900")
root.configure(bg="black")
root.resizable(True, True)
root.iconbitmap(resource_path("icongg.ico"))


NEON_BG = "#000000"
NEON_GREEN = "#23ff00"
NEON_GREEN_DIM = "#0fa000"

style = ttk.Style()
try:
    style.theme_use('clam')
except Exception:
    pass

# --- Tema Keygen Verde ---
NEON_GREEN = "#23ff00"

# Combobox stile uguale alle entry: verde scuro con cornice chiara
style.configure(
    'Dark.TCombobox',
    fieldbackground='#001100',     # sfondo verde scuro (come entry)
    background='#001100',          # interno stesso tono
    foreground=NEON_GREEN,         # testo verde
    selectbackground='#001100',
    selectforeground=NEON_GREEN,
    bordercolor='#003300',         # cornice verde più chiara
    lightcolor='#003300',          # bordo superiore più chiaro
    darkcolor='#003300',           # bordo inferiore più chiaro
    arrowcolor=NEON_GREEN,         # freccina verde
    relief='flat'
)

# Disattiva variazioni grigie in hover/focus
style.map('Dark.TCombobox',
          fieldbackground=[('readonly', '#001100'),
                           ('active', '#001100'),
                           ('hover', '#001100'),
                           ('pressed', '#001100'),
                           ('focus', '#001100')],
          background=[('readonly', '#001100'),
                      ('active', '#001100'),
                      ('hover', '#001100'),
                      ('pressed', '#001100'),
                      ('focus', '#001100')],
          foreground=[('readonly', NEON_GREEN),
                      ('active', NEON_GREEN),
                      ('hover', NEON_GREEN),
                      ('focus', NEON_GREEN)],
          arrowcolor=[('active', NEON_GREEN),
                      ('hover', NEON_GREEN),
                      ('pressed', NEON_GREEN),
                      ('focus', NEON_GREEN)]
)

# Rimuove il bordo 3D nativo
style.layout('Dark.TCombobox',
             [('Combobox.downarrow', {'side': 'right', 'sticky': ''}),
              ('Combobox.padding', {'side': 'left', 'sticky': 'nswe',
                                    'children': [('Combobox.textarea', {'sticky': 'nswe'})]})])

# Stile per menu a tendina
style.configure('TComboboxPopdownFrame', background='#001100')
root.option_add('*TCombobox*Listbox.background', '#001100')
root.option_add('*TCombobox*Listbox.foreground', NEON_GREEN)
root.option_add('*TCombobox*Listbox.selectBackground', '#003300')
root.option_add('*TCombobox*Listbox.selectForeground', NEON_GREEN)



style.map('Dark.TCombobox',
          fieldbackground=[('readonly', '#001100')],
          foreground=[('readonly', NEON_GREEN)])

# logo originale (non ridotto da te in questo punto: manteniamo il comportamento precedente)
ORIGINAL_ASCII = r"""                                                                                                     
.oPYo.    .oPYo.         .oo    ooo.   o o     o .oPYo. o    o .oPYo. o .oPYo. o    o .oPYo.  .oPYo. 
8    8    8    8        .P 8    8  `8. 8 8b   d8 8.     8b   8 8      8 8    8 8b   8 8.      8   `8 
8         8            .P  8    8   `8 8 8`b d'8 `boo   8`b  8 `Yooo. 8 8    8 8`b  8 `boo   o8YooP' 
8         8           oPooo8    8    8 8 8 `o' 8 .P     8 `b 8     `8 8 8    8 8 `b 8 .P      8   `b 
8    8    8    8     .P    8    8   .P 8 8     8 8      8  `b8      8 8 8    8 8  `b8 8       8    8 
`YooP' 88 `YooP' 88 .P     8 88 8ooo'  8 8     8 `YooP' 8   `8 `YooP' 8 `YooP' 8   `8 `YooP'  8    8 
:.....:..::.....:..:..:::::....:.....::....::::..:.....:..:::..:.....:..:.....:..:::..:.....::..:::..
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::""".strip()

SMALL_LOGO = shrink_ascii_logo(ORIGINAL_ASCII, scale=1)

header_frame = tk.Frame(root, bg=NEON_BG)
header_frame.pack(fill="x", pady=(6,6))
header_canvas = tk.Canvas(header_frame, height=120, bg=NEON_BG, highlightthickness=0)
header_canvas.pack(fill="x", padx=8, pady=(6,2))

def draw_logo_green_glow():
    header_canvas.delete("all")
    x = 6; y = 6
    # layers for green glow
    header_canvas.create_text(x+2, y+2, anchor="nw", text=SMALL_LOGO, font=("Consolas", 9, "bold"), fill="#022200", tags=("logo_base",))
    header_canvas.create_text(x+1, y+1, anchor="nw", text=SMALL_LOGO, font=("Consolas", 10, "bold"), fill=NEON_GREEN_DIM, tags=("logo_glow",))
    header_canvas.create_text(x, y, anchor="nw", text=SMALL_LOGO, font=("Consolas", 10, "bold"), fill=NEON_GREEN, tags=("logo_main",))

draw_logo_green_glow()

frame = tk.Frame(root, bg="#050505", padx=10, pady=10)
frame.pack(fill="both", expand=True, padx=8, pady=6)

left = tk.Frame(frame, bg="#070707")
left.pack(side="left", fill="y", padx=(6,8), pady=6)
right = tk.Frame(frame, bg="#070707")
right.pack(side="right", fill="both", expand=True, padx=(8,6), pady=6)

# entries
def make_entry(parent, label_text, default=""):
    lbl = tk.Label(parent, text=label_text, anchor="w", bg="#070707", fg=NEON_GREEN, font=("Consolas", 10, "bold"))
    lbl.pack(anchor="w", pady=(8,2))
    e = tk.Entry(parent, bg="#001100", fg=NEON_GREEN, insertbackground=NEON_GREEN, font=("Consolas", 11), bd=0, relief="flat")
    e.pack(fill="x", pady=(0,4))
    e.configure(highlightthickness=1, highlightbackground="#003300", highlightcolor=NEON_GREEN)
    if default != "":
        e.insert(0, default)
    return e

entry_lunghezza = make_entry(left, "Lunghezza cavo positivo (solo andata, m):", "5")
entry_potenza = make_entry(left, "Potenza RMS totale (W):", "3000")
entry_deltav = make_entry(left, "Caduta di tensione ammessa (V) (di solito 0.3–0.5):", "0.5")
entry_tensione = make_entry(left, "Tensione nominale (V):", "12.8")
entry_batteria = make_entry(left, "Capacità batteria principale (Ah):", "80")
entry_alternatore = make_entry(left, "Corrente nominale alternatore (A):", "120")
entry_peukert = make_entry(left, "Efficienza batteria (Peukert):", "1.2")

lbl_cl = tk.Label(left, text="Classe amplificatore:", bg="#070707", fg=NEON_GREEN, font=("Consolas", 10, "bold"))
lbl_cl.pack(anchor="w", pady=(8, 2))
combo_classe = ttk.Combobox(left, values=["A","AB","D","T","G","H"], state="readonly", font=("Consolas", 10), style='Dark.TCombobox')
combo_classe.current(2)
combo_classe.pack(fill="x", pady=(0,6))

lbl_util = tk.Label(left, text="Utilizzo realistico (tipo di uso):", bg="#070707", fg=NEON_GREEN, font=("Consolas", 10, "bold"))
lbl_util.pack(anchor="w", pady=(6,2))
combo_utilizzo = ttk.Combobox(
    left,
    values=[
        "10% - burning tesla mode",
        "20% - ",
        "30% - uso leggero",
        "40% - uso comune",
        "50% - ",
        "60% - uso intenso",
        "70% - ",
        "80% - ",
        "90% - SPL",
        "100% - segnale continuo (test)"
    ],
    state="readonly",
    font=("Consolas", 10),
    style='Dark.TCombobox'
)
combo_utilizzo.current(3)
combo_utilizzo.pack(fill="x", pady=(0,6))

massa_var = tk.StringVar(value="chassis")
mass_frame = tk.Frame(left, bg="#070707")
mass_frame.pack(fill="x", pady=(8,6))
tk.Label(mass_frame, text="Metodo collegamento massa:", bg="#070707", fg=NEON_GREEN, font=("Consolas", 10, "bold")).pack(anchor="w")
tk.Radiobutton(mass_frame, text="Negativo diretto alla batteria (2×L)", variable=massa_var, value="battery", bg="#070707", fg=NEON_GREEN, selectcolor="#002200", activebackground="#001100", font=("Consolas", 9)).pack(anchor="w")
tk.Radiobutton(mass_frame, text="Massa su telaio - buona (1.3×L)", variable=massa_var, value="chassis", bg="#070707", fg=NEON_GREEN, selectcolor="#002200", activebackground="#001100", font=("Consolas", 9)).pack(anchor="w")

def make_keygen_button(parent, text, command):
    b = tk.Button(parent, text=text, command=command, bg="#001100", fg=NEON_GREEN, activebackground="#003300",
                  font=("Consolas", 12, "bold"), bd=0, relief="flat")
    b.pack(fill="x", pady=(8,6))
    b.configure(highlightthickness=2, highlightbackground="#003300", highlightcolor=NEON_GREEN)
    return b

calc_btn = make_keygen_button(left, ">>> GENERA (CALCOLA) <<<", calcola)

music_toggle_btn = tk.Button(
    left,
    text="Musica: OFF (clic per ON)",
    command=toggle_music,
    bg="#220000",             # sfondo base (rosso scuro)
    fg=NEON_GREEN,
    activebackground="#330000",  # colore mentre tieni premuto
    activeforeground=NEON_GREEN, # mantiene testo verde
    relief="flat",
    font=("Consolas", 10, "bold"),
    bd=0,
    highlightthickness=2,
    highlightbackground="#003300",
    highlightcolor=NEON_GREEN
)
music_toggle_btn.pack(fill="x", pady=(6,8))


output_label = tk.Label(right, text="OUTPUT", bg="#070707", fg=NEON_GREEN, font=("Consolas", 11, "bold"))
output_label.pack(anchor="w")
text_output = tk.Text(right, wrap="word", height=28, font=("Consolas", 11), bg="#001100", fg=NEON_GREEN, bd=0, relief="flat")
text_output.pack(fill="both", expand=True, pady=(4,6))
text_output.configure(highlightthickness=1, highlightbackground="#003300", highlightcolor=NEON_GREEN)


# animation: gentle pulse
def logo_pulse_tick():
    if random.random() < 0.4:
        header_canvas.itemconfigure("logo_main", fill=NEON_GREEN_DIM)
    else:
        header_canvas.itemconfigure("logo_main", fill=NEON_GREEN)
    root.after(400 + random.randint(-120,120), logo_pulse_tick)

def pulse_entries_tick():
    entries = [entry_lunghezza, entry_potenza, entry_deltav, entry_tensione,
               entry_batteria, entry_alternatore, entry_peukert]
    for e in entries:
        if random.random() < 0.25:
            e.configure(highlightbackground=random.choice([NEON_GREEN, NEON_GREEN_DIM]))
        else:
            e.configure(highlightbackground="#003300")
    root.after(460, pulse_entries_tick)

logo_pulse_tick()
pulse_entries_tick()

def on_resize(event):
    draw_logo_green_glow()

root.bind("<Configure>", on_resize)

def copy_output(event=None):
    root.clipboard_clear()
    root.clipboard_append(text_output.get("1.0", "end-1c"))
    return "break"

root.bind_all("<Control-c>", copy_output)

# -----------------------
# Preparazione musica in background (niente finestra bianca)
# -----------------------


def prepare_music_in_background():
    """Prepara la musica senza bloccare la GUI"""
    print("🎵 Preparazione musica in corso...")
    ok, info = prepare_music_from_base64_string()
    if not ok:
        print("Musica non preparata:", info)
    else:
        start_music()
        print("✅ Musica avviata correttamente.")

# Avvia la preparazione musicale in un thread separato
threading.Thread(target=prepare_music_in_background, daemon=True).start()

# Pulizia finale alla chiusura
def cleanup():
    try:
        stop_music()
    except Exception:
        pass
    try:
        if MUSIC_WAV_PATH and os.path.exists(MUSIC_WAV_PATH):
            os.remove(MUSIC_WAV_PATH)
    except Exception:
        pass
    try:
        if MUSIC_TEMP_PATH and os.path.exists(MUSIC_TEMP_PATH):
            os.remove(MUSIC_TEMP_PATH)
    except Exception:
        pass

atexit.register(cleanup)

# Avvia la GUI
root.mainloop()
