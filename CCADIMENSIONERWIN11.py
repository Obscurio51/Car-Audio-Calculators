import sys, os, math, random, base64, tempfile, shutil, subprocess, atexit
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTextEdit, QComboBox, QRadioButton, QButtonGroup, QMessageBox)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QTimer
# pygame opzionale
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

BASE64_XM = r"""
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
""".strip()  # Inserisci la musica base64 qui

def resource_path(relative_path):
    """Restituisce il percorso assoluto anche quando eseguito da EXE PyInstaller"""
    try:
        base_path = sys._MEIPASS  # path temporaneo in cui PyInstaller estrae i file
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def shrink_ascii_logo(ascii_logo, scale=0.7):
    lines = ascii_logo.rstrip("\n").splitlines()
    if not lines: return ""
    maxw = max(len(l) for l in lines)
    padded = [l.ljust(maxw) for l in lines]
    new_h = max(1, int(len(padded)*scale))
    new_w = max(1, int(maxw*scale))
    out_lines = []
    for y in range(new_h):
        src_y = min(len(padded)-1, int(y/scale))
        src_line = padded[src_y]
        chars = []
        for x in range(new_w):
            src_x = min(maxw-1, int(x/scale))
            chars.append(src_line[src_x])
        out_lines.append("".join(chars).rstrip())
    return "\n".join(out_lines)

class CableCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path("icongg.ico")))
        self.setWindowTitle("Calcolatore sezione cavi Car Audio")
        self.resize(820, 900)
        self.setStyleSheet("background-color: black; color: #23ff00; font-family: Consolas;")
        self.NEON_GREEN = "#23ff00"
        self.NEON_GREEN_DIM = "#0fa000"
        self.music_on = False
        self.music_temp_path = None
        self.music_wav_path = None
        self.external_player_proc = None

        self.build_ui()
        self.prepare_music_from_base64_string()
        self.start_music()

        # Pulsazioni
        self.logo_timer = QTimer()
        self.logo_timer.timeout.connect(self.logo_pulse_tick)
        self.logo_timer.start(400)
        self.entries_timer = QTimer()
        self.entries_timer.timeout.connect(self.pulse_entries_tick)
        self.entries_timer.start(460)

        # Pulizia
        atexit.register(self.cleanup)

    def build_ui(self):
        layout = QVBoxLayout(self)

        # LOGO ASCII
        self.ORIGINAL_ASCII = r"""                                                                                                     
.oPYo.    .oPYo.         .oo    ooo.   o o     o .oPYo. o    o .oPYo. o .oPYo. o    o .oPYo.  .oPYo. 
8    8    8    8        .P 8    8  `8. 8 8b   d8 8.     8b   8 8      8 8    8 8b   8 8.      8   `8 
8         8            .P  8    8   `8 8 8`b d'8 `boo   8`b  8 `Yooo. 8 8    8 8`b  8 `boo   o8YooP' 
8         8           oPooo8    8    8 8 8 `o' 8 .P     8 `b 8     `8 8 8    8 8 `b 8 .P      8   `b 
8    8    8    8     .P    8    8   .P 8 8     8 8      8  `b8      8 8 8    8 8  `b8 8       8    8 
`YooP' 88 `YooP' 88 .P     8 88 8ooo'  8 8     8 `YooP' 8   `8 `YooP' 8 `YooP' 8   `8 `YooP'  8    8 
:.....:..::.....:..:..:::::....:.....::....::::..:.....:..:::..:.....:..:.....:..:::..:.....::..:::..
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"""
        SMALL_LOGO = shrink_ascii_logo(self.ORIGINAL_ASCII, scale=1)
        self.logo_label = QLabel(SMALL_LOGO)
        self.logo_label.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        self.logo_label.setStyleSheet(f"color:{self.NEON_GREEN};")
        layout.addWidget(self.logo_label)

        # MAIN FRAME
        main_frame = QHBoxLayout()
        layout.addLayout(main_frame)

        # LEFT
        self.left_frame = QVBoxLayout()
        main_frame.addLayout(self.left_frame)

        # RIGHT
        self.right_frame = QVBoxLayout()
        main_frame.addLayout(self.right_frame, stretch=1)

        # ENTRIES
        self.entry_lunghezza = self.make_entry("Lunghezza cavo positivo (solo andata, m):", "5")
        self.entry_potenza = self.make_entry("Potenza RMS totale (W):", "3000")
        self.entry_deltav = self.make_entry("Caduta di tensione ammessa (V) (di solito 0.3–0.5):", "0.5")
        self.entry_tensione = self.make_entry("Tensione nominale (V):", "12.8")
        self.entry_batteria = self.make_entry("Capacità batteria principale (Ah):", "80")
        self.entry_alternatore = self.make_entry("Corrente nominale alternatore (A):", "120")
        self.entry_peukert = self.make_entry("Efficienza batteria (Peukert):", "1.2")

        # Combo classe
        lbl_cl = QLabel("Classe amplificatore:")
        lbl_cl.setStyleSheet(f"color:{self.NEON_GREEN}; font-weight:bold;")
        self.left_frame.addWidget(lbl_cl)
        self.combo_classe = QComboBox()
        self.combo_classe.addItems(["A","AB","D","T","G","H"])
        self.combo_classe.setCurrentIndex(2)
        self.left_frame.addWidget(self.combo_classe)

        # Combo utilizzo
        lbl_util = QLabel("Utilizzo realistico (tipo di uso):")
        lbl_util.setStyleSheet(f"color:{self.NEON_GREEN}; font-weight:bold;")
        self.left_frame.addWidget(lbl_util)
        self.combo_utilizzo = QComboBox()
        self.combo_utilizzo.addItems([
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
        ])
        self.combo_utilizzo.setCurrentIndex(3)
        self.left_frame.addWidget(self.combo_utilizzo)

        # Radio massa
        mass_label = QLabel("Metodo collegamento massa:")
        mass_label.setStyleSheet(f"color:{self.NEON_GREEN}; font-weight:bold;")
        self.left_frame.addWidget(mass_label)
        self.massa_group = QButtonGroup()
        self.rb_battery = QRadioButton("Negativo diretto alla batteria (2×L)")
        self.rb_chassis = QRadioButton("Massa su telaio - buona (1.3×L)")
        self.rb_chassis.setChecked(True)
        for rb in [self.rb_battery, self.rb_chassis]:
            rb.setStyleSheet(f"color:{self.NEON_GREEN};")
            self.left_frame.addWidget(rb)
            self.massa_group.addButton(rb)

        # Pulsanti
        self.calc_btn = self.make_neon_button(">>> GENERA (CALCOLA) <<<", self.calcola)
        self.left_frame.addWidget(self.calc_btn)
        self.music_btn = self.make_neon_button("Musica: OFF (clic per ON)", self.toggle_music)
        self.left_frame.addWidget(self.music_btn)

        # RIGHT output
        self.output_label = QLabel("OUTPUT")
        self.output_label.setStyleSheet(f"color:{self.NEON_GREEN}; font-weight:bold;")
        self.right_frame.addWidget(self.output_label)
        self.text_output = QTextEdit()
        self.text_output.setStyleSheet(f"background:#001100; color:{self.NEON_GREEN}; font-family:Consolas;")
        self.right_frame.addWidget(self.text_output, stretch=1)

    def make_entry(self, label_text, default=""):
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"color:{self.NEON_GREEN}; font-weight:bold;")
        self.left_frame.addWidget(lbl)
        e = QLineEdit()
        e.setStyleSheet(f"background:#001100; color:{self.NEON_GREEN}; border:1px solid #003300;")
        e.setText(default)
        self.left_frame.addWidget(e)
        return e

    def make_neon_button(self, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #001100;
                color: {self.NEON_GREEN};
                border: 2px solid #003300;
                padding: 6px;
            }}
            QPushButton:hover {{
                border: 2px solid {self.NEON_GREEN_DIM};
            }}
            QPushButton:pressed {{
                background-color: #003300;
                border: 2px solid {self.NEON_GREEN};
            }}
            QPushButton:focus {{
                border: 2px solid {self.NEON_GREEN};
            }}
        """)
        return btn

    # ----------------- Pulsazioni -----------------
    def logo_pulse_tick(self):
        self.logo_label.setStyleSheet(f"color:{self.NEON_GREEN_DIM if random.random()<0.4 else self.NEON_GREEN};")

    def pulse_entries_tick(self):
        for e in [self.entry_lunghezza, self.entry_potenza, self.entry_deltav,
                  self.entry_tensione, self.entry_batteria, self.entry_alternatore, self.entry_peukert]:
            e.setStyleSheet(f"background:#001100; color:{self.NEON_GREEN}; border:1px solid {self.NEON_GREEN if random.random()<0.25 else '#003300'};")

    # ----------------- Calcolo -----------------
    def calcola(self):
        try:
            lunghezza = float(self.entry_lunghezza.text().replace(",", "."))
            potenza = float(self.entry_potenza.text().replace(",", "."))
            classe = self.combo_classe.currentText()
            delta_v = float(self.entry_deltav.text().replace(",", "."))
            tensione = float(self.entry_tensione.text().replace(",", "."))
            capacita_batt = float(self.entry_batteria.text().replace(",", "."))
            alternatore_A = float(self.entry_alternatore.text().replace(",", "."))
            peukert = float(self.entry_peukert.text().replace(",", "."))
            utilizzo_text = self.combo_utilizzo.currentText()
            utilizzo = float(utilizzo_text.split("%")[0].strip()) / 100.0

            eff_dict = {"A":0.25, "AB":0.55, "D":0.85, "T":0.80, "G":0.70, "H":0.80}
            eff = eff_dict.get(classe, None)
            if eff is None: raise ValueError("Classe non valida")

            mass_opt = "battery" if self.rb_battery.isChecked() else "chassis"
            fattore_massa = 2.0 if mass_opt=="battery" else 1.3
            lung_eff = lunghezza*fattore_massa
            rho = 0.0175
            corrente = potenza/(tensione*eff)*utilizzo
            if corrente==0: raise ValueError("Utilizzo 0%")

            r_max = delta_v/corrente
            sezione = (rho*lung_eff)/r_max
            metri_equivalenti = lung_eff
            farad = round((potenza/100)*0.03,2)

            def autonomia(capacita, corrente, k):
                if corrente<=0: return 0
                h_nom=20.0
                t = h_nom*(capacita/(corrente*h_nom))**k
                return t
            def formatta_autonomia(ore):
                if ore=="∞ (alternatore sufficiente)": return ore
                if ore<=0: return "0 min"
                if ore<1: return f"{ore*60:.0f} min"
                h=int(ore); m=int((ore-h)*60)
                return f"{h}h {m}m"

            corrente_12v = potenza/(12*eff)*utilizzo
            autonomia_spento = formatta_autonomia(autonomia(capacita_batt, corrente_12v, peukert))
            corrente_14v = potenza/(14.4*eff)*utilizzo
            if alternatore_A>=corrente_14v: autonomia_acceso="∞ (alternatore sufficiente)"
            else:
                corrente_mancante = corrente_14v - alternatore_A
                autonomia_acceso = formatta_autonomia(autonomia(capacita_batt, corrente_mancante, peukert))

            corrente_residua = alternatore_A - corrente
            residuo_msg = (f"✖ Corrente residua alternatore: {corrente_residua:.1f} A" if corrente_residua < 0 else
                           f"△ Corrente residua alternatore: +{corrente_residua:.1f} A" if corrente_residua < 20 else
                           f"✔ Corrente residua alternatore: +{corrente_residua:.1f} A")
            margine = alternatore_A - corrente
            alt_msg = ("✔ Alternatore adeguato al carico previsto." if margine >= 40 else
                       "△ Alternatore vicino al limite: valuta upgrade o batteria aggiuntiva." if margine > 0 else
                       "✖ Alternatore insufficiente: necessario maggiorarlo e maggiorarne il cavo.")
            batt_msg = ("✔ Batteria sufficiente per l’impianto." if corrente < 60 else
                        "△ Corrente elevata: valuta l’aggiunta di una seconda batteria." if corrente <= 100 else
                        "✖ Corrente molto alta: consigliata una batteria aggiuntiva.")
            crest_factor = 10*math.log10(1/utilizzo) if utilizzo>0 else 0

            spieg = ("Nota: 'utilizzo realistico' rappresenta la percentuale di tempo in cui l’amplificatore eroga potenza.\n"
                     "Un valore più basso indica musica più dinamica e assorbimento medio minore.\n\n")
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
                f"{residuo_msg}\n"
                f"Alternatore: {alternatore_A:.0f} A nominali\n\n"
                f"{batt_msg}\n{alt_msg}"
            )
            self.text_output.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))

    # ----------------- Musica -----------------
    def prepare_music_from_base64_string(self):
        if not BASE64_XM.strip(): return
        raw = base64.b64decode("".join(BASE64_XM.split()))
        fd,temp_path = tempfile.mkstemp(prefix="keygen_theme_", suffix=".xm")
        os.close(fd)
        with open(temp_path,"wb") as f: f.write(raw)
        self.music_temp_path = temp_path
        if shutil.which("ffmpeg"):
            fd,wav_path=tempfile.mkstemp(prefix="keygen_theme_",suffix=".wav")
            os.close(fd)
            cmd=["ffmpeg","-y","-loglevel","error","-i",self.music_temp_path,wav_path]
            proc=subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
            if proc.returncode==0: self.music_wav_path=wav_path

    def start_music(self):
        if not self.music_temp_path: return
        if PYGAME_AVAILABLE:
            try:
                if not pygame.mixer.get_init(): pygame.mixer.init()
                pygame.mixer.music.load(self.music_wav_path or self.music_temp_path)
                pygame.mixer.music.set_volume(0.45)
                pygame.mixer.music.play(-1)
                self.music_on=True
                self.music_btn.setText("Musica: ON (clic per OFF)")
                return
            except Exception: pass
        self.music_on=True
        self.music_btn.setText("Musica: ON (clic per OFF)")

    def stop_music(self):
        if PYGAME_AVAILABLE:
            try: pygame.mixer.music.stop()
            except Exception: pass
        self.music_on=False
        self.music_btn.setText("Musica: OFF (clic per ON)")

    def toggle_music(self):
        if self.music_on: self.stop_music()
        else: self.start_music()

    def cleanup(self):
        self.stop_music()
        for f in [self.music_temp_path,self.music_wav_path]:
            try: os.remove(f) if f and os.path.exists(f) else None
            except Exception: pass

if __name__=="__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("icongg.ico")))
    window = CableCalc()
    window.show()
    sys.exit(app.exec())
