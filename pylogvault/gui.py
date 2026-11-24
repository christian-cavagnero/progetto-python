import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from backup_manager.archiver import create_backup_zip, get_old_logs
from backup_manager.config import BACKUP_DIR, DB_PATH, DEFAULT_RETENTION_DAYS, LOGS_DIR
from backup_manager.database import init_db, leggi_storico, salva_scansione
from backup_manager.pdf_reporter import generate_pdf_report


class PyLogVaultApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PyLogVault - Gestione Log e Backup")
        self.root.geometry("560x350")
        self.root.resizable(False, False)

        # Inizializza il database all'avvio
        init_db(DB_PATH)

        # Variabili Tkinter
        self.logs_var = tk.StringVar(value=str(LOGS_DIR))
        self.backup_var = tk.StringVar(value=str(BACKUP_DIR))
        self.days_var = tk.IntVar(value=DEFAULT_RETENTION_DAYS)
        self.delete_var = tk.BooleanVar(value=False)

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        # Cartella Log
        tk.Label(self.root, text="Cartella Log:").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(self.root, textvariable=self.logs_var, width=42).grid(row=0, column=1, **pad)
        tk.Button(self.root, text="Sfoglia", command=self._scegli_logs).grid(row=0, column=2, **pad)

        # Cartella Backup
        tk.Label(self.root, text="Cartella Backup:").grid(row=1, column=0, sticky="w", **pad)
        tk.Entry(self.root, textvariable=self.backup_var, width=42).grid(row=1, column=1, **pad)
        tk.Button(self.root, text="Sfoglia", command=self._scegli_backup).grid(row=1, column=2, **pad)

        # Giorni di retention
        tk.Label(self.root, text="Giorni retention:").grid(row=2, column=0, sticky="w", **pad)
        tk.Spinbox(self.root, from_=0, to=365, textvariable=self.days_var, width=10).grid(
            row=2, column=1, sticky="w", **pad
        )

        # Checkbox eliminazione
        tk.Checkbutton(
            self.root,
            text="Elimina i file .log originali dopo il backup",
            variable=self.delete_var,
        ).grid(row=3, column=1, columnspan=2, sticky="w", **pad)

        # Frame per i pulsanti principali
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=18)

        tk.Button(
            btn_frame,
            text="Avvia Scansione e Backup",
            command=self._avvia_backup,
            bg="#2e7d32",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=12,
            pady=8,
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Visualizza Storico (DB)",
            command=self._mostra_storico,
            bg="#1565c0",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=12,
            pady=8,
        ).pack(side="left", padx=10)

        # Barra di stato
        self.status_label = tk.Label(self.root, text="Pronto.", fg="gray")
        self.status_label.grid(row=5, column=0, columnspan=3, **pad)

    def _scegli_logs(self):
        path = filedialog.askdirectory()
        if path:
            self.logs_var.set(path)

    def _scegli_backup(self):
        path = filedialog.askdirectory()
        if path:
            self.backup_var.set(path)

    def _avvia_backup(self):
        logs_dir = Path(self.logs_var.get())
        backup_dir = Path(self.backup_var.get())
        days = self.days_var.get()
        delete_source = self.delete_var.get()

        old_logs = get_old_logs(logs_dir, days=days)

        if not old_logs:
            salva_scansione(DB_PATH, str(logs_dir), days, delete_source, 0, None)
            self.status_label.config(text="Nessun file .log da archiviare.", fg="orange")
            messagebox.showinfo("Risultato", f"Nessun file .log più vecchio di {days} giorni.")
            return

        zip_path = create_backup_zip(old_logs, backup_dir)
        pdf_path = generate_pdf_report(zip_path, old_logs, backup_dir, days, delete_source)
        salva_scansione(DB_PATH, str(logs_dir), days, delete_source, len(old_logs), zip_path.name)

        if delete_source:
            for f in old_logs:
                f.unlink()

        self.status_label.config(text=f"Completato! Salvato {zip_path.name}", fg="green")
        messagebox.showinfo(
            "Backup Completato",
            f"Archiviati {len(old_logs)} file.\n\n"
            f"ZIP: {zip_path.name}\n"
            f"Report PDF: {pdf_path.name}\n"
            f"Scansione registrata nel database SQLite.",
        )

    def _mostra_storico(self):
        """Apre una seconda finestra con la tabella delle scansioni salvate in SQLite."""
        win = tk.Toplevel(self.root)
        win.title("Storico Scansioni (SQLite3)")
        win.geometry("820x350")

        colonne = ("ID", "Data e Ora", "Tipo", "Giorni", "Eliminati", "File", "Archivio ZIP")
        tree = ttk.Treeview(win, columns=colonne, show="headings")

        larghezze = [40, 140, 60, 60, 70, 50, 220]
        for col, width in zip(colonne, larghezze):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")

        righe = leggi_storico(DB_PATH)
        for r in righe:
            # r = (id, data_ora, cartella_log, tipo_file, giorni, elimina, file_archiviati, nome_archivio)
            eliminati_str = "Sì" if r[5] else "No"
            archivio_str = r[7] if r[7] else "Nessuno"
            tree.insert("", "end", values=(r[0], r[1], r[3], r[4], eliminati_str, r[6], archivio_str))

        tree.pack(fill="both", expand=True, padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = PyLogVaultApp(root)
    root.mainloop()