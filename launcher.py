import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import webbrowser

BG     = "#0f1117"
CARD   = "#1a1d2e"
ACCENT = "#e24b4a"
GREEN  = "#1d9e75"
AMBER  = "#ef9f27"
BLUE   = "#378add"
TEXT   = "#f0f0f0"
MUTED  = "#888780"
BORDER = "#2a2d3e"
PURPLE = "#7f77dd"

PROJECT_DIR = r"C:\Users\piyus\Cybersecurity-Projects\PROJECTS\advanced\ai-threat-detection"


def run_bg(cmd, log, cwd=PROJECT_DIR):
    def task():
        try:
            proc = subprocess.Popen(
                cmd, cwd=cwd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in proc.stdout:
                log.config(state="normal")
                log.insert("end", line)
                log.see("end")
                log.config(state="disabled")
            log.config(state="normal")
            log.insert("end", "Done.\n\n")
            log.see("end")
            log.config(state="disabled")
        except Exception as e:
            log.config(state="normal")
            log.insert("end", f"[ERROR] {e}\n\n")
            log.config(state="disabled")
    threading.Thread(target=task, daemon=True).start()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AngelusVigil — AI Threat Detection Launcher")
        self.geometry("820x680")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.build()

    def build(self):
        # ── top accent bar ──
        tk.Frame(self, bg=ACCENT, height=4).pack(fill="x")

        # ── header ──
        hdr = tk.Frame(self, bg=BG, pady=14)
        hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="AngelusVigil", font=("Consolas", 22, "bold"),
                 bg=BG, fg=TEXT).pack(side="left")
        tk.Label(hdr, text="  AI Threat Detection Launcher",
                 font=("Consolas", 12), bg=BG, fg=MUTED).pack(side="left", pady=6)
        tk.Label(hdr, text="⬤ localhost:46969", font=("Consolas", 10),
                 bg=BG, fg=GREEN).pack(side="right")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=24)

        # ── two columns ──
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=24, pady=12)

        left  = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))
        right = tk.Frame(body, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        # ════ LEFT COLUMN ════

        # Docker controls
        self.section(left, "Docker Controls")
        self.btn(left, "▶  Start All Containers", GREEN,
                 "docker compose -f dev.compose.yml up -d && docker compose -f dev-log/compose.yml up -d")
        self.btn(left, "↺  Restart Backend", AMBER,
                 "docker restart vigil-backend-dev")
        self.btn(left, "↺  Restart Frontend", BLUE,
                 "docker restart vigil-frontend-dev")
        self.btn(left, "⬡  Check Status", MUTED,
                 "start cmd /k docker ps")

        tk.Frame(left, bg=BG, height=10).pack()

        # Dashboard
        self.section(left, "Dashboard")
        open_btn = tk.Button(
            left, text="⬛  Open Dashboard in Browser",
            bg=BLUE, fg="#fff", font=("Consolas", 11, "bold"),
            relief="flat", cursor="hand2", pady=10, padx=12,
            activebackground="#185fa5", activeforeground="#fff",
            command=lambda: webbrowser.open("http://localhost:46969")
        )
        open_btn.pack(fill="x", pady=3)

        tk.Frame(left, bg=BG, height=10).pack()

        # STOP / CLOSE
        self.section(left, "Shutdown")
        stop_btn = tk.Button(
            left, text="⬛  Stop All & Close App",
            bg=ACCENT, fg="#fff", font=("Consolas", 11, "bold"),
            relief="flat", cursor="hand2", pady=10, padx=12,
            activebackground="#a32d2d", activeforeground="#fff",
            command=self.on_close
        )
        stop_btn.pack(fill="x", pady=3)

        # ════ RIGHT COLUMN ════

        self.section(right, "Simulate Attacks")

        # Count selector
        count_row = tk.Frame(right, bg=BG)
        count_row.pack(fill="x", pady=(2, 8))
        tk.Label(count_row, text="Count:", bg=BG, fg=MUTED,
                 font=("Consolas", 10)).pack(side="left", padx=(0, 8))
        self.count = tk.IntVar(value=100)
        for n in [25, 50, 100, 200]:
            tk.Radiobutton(
                count_row, text=str(n), variable=self.count, value=n,
                bg=BG, fg=TEXT, selectcolor=CARD,
                activebackground=BG, activeforeground=TEXT,
                font=("Consolas", 10)
            ).pack(side="left", padx=4)

        attacks = [
            ("Mixed  (All Types)",    ACCENT,  "mixed"),
            ("SQL Injection",          "#c0392b","sqli"),
            ("XSS Attack",             AMBER,   "xss"),
            ("Log4Shell",              PURPLE,  "log4shell"),
            ("Path Traversal",         GREEN,   "traversal"),
            ("Command Injection",      "#e67e22","cmdi"),
            ("Port Scanner",           BLUE,    "scanner"),
            ("Flood Attack",           MUTED,   "flood"),
            ("Normal Traffic",         "#5dcaa5","normal"),
        ]

        for label, color, mode in attacks:
            self.attack_btn(right, label, color, mode)

        # ── log box ──
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(6, 4))
        tk.Label(self, text="OUTPUT LOG", bg=BG, fg=MUTED,
                 font=("Consolas", 9)).pack(anchor="w", padx=28)

        log_wrap = tk.Frame(self, bg=CARD)
        log_wrap.pack(fill="x", padx=24, pady=(2, 16))

        self.log = tk.Text(
            log_wrap, height=7, bg=CARD, fg=GREEN,
            font=("Consolas", 9), state="disabled",
            relief="flat", padx=10, pady=8,
            insertbackground=GREEN, wrap="word"
        )
        sb = tk.Scrollbar(log_wrap, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.log.pack(fill="x")

        self.log_write("AngelusVigil launcher ready.\n"
                       "Click 'Start All Containers' to begin, then open the dashboard.\n\n")

    # ── helpers ──────────────────────────────────────────

    def section(self, parent, title):
        tk.Label(parent, text=title.upper(), bg=BG, fg=MUTED,
                 font=("Consolas", 9, "bold")).pack(anchor="w", pady=(4, 2))
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", pady=(0, 6))

    def btn(self, parent, label, color, cmd):
        is_shell = cmd.startswith("start cmd")
        def clicked():
            self.log_write(f"> {label.strip()}\n")
            if is_shell:
                subprocess.Popen(cmd, shell=True, cwd=PROJECT_DIR)
            else:
                run_bg(cmd, self.log)
        tk.Button(
            parent, text=label, bg=CARD, fg=color,
            font=("Consolas", 10), relief="flat", cursor="hand2",
            anchor="w", padx=12, pady=7,
            activebackground=BORDER, activeforeground=color,
            command=clicked
        ).pack(fill="x", pady=2)

    def attack_btn(self, parent, label, color, mode):
        def clicked():
            n = self.count.get()
            cmd = f"python dev-log/simulate.py {mode} -n {n}"
            self.log_write(f"> Simulating {n}x {label.strip()}...\n")
            run_bg(cmd, self.log)
        tk.Button(
            parent, text=label, bg=CARD, fg=color,
            font=("Consolas", 10), relief="flat", cursor="hand2",
            anchor="w", padx=12, pady=6,
            activebackground=BORDER, activeforeground=color,
            command=clicked
        ).pack(fill="x", pady=1)

    def log_write(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg)
        self.log.see("end")
        self.log.config(state="disabled")

    def on_close(self):
        if messagebox.askyesno(
            "Shut Down",
            "Stop all Docker containers and close the launcher?"
        ):
            self.log_write("> Stopping all containers...\n")
            subprocess.Popen(
                "docker compose -f dev.compose.yml down && docker compose -f dev-log/compose.yml down",
                cwd=PROJECT_DIR, shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.after(3000, self.destroy)


if __name__ == "__main__":
    app = App()
    app.mainloop()
