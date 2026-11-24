import sqlite3
from datetime import datetime
from pathlib import Path


def init_db(db_path: Path):
    """Crea il database SQLite e la tabella scansioni se non esistono."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scansioni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_ora TEXT NOT NULL,
                cartella_log TEXT NOT NULL,
                tipo_file TEXT NOT NULL,
                giorni_retention INTEGER NOT NULL,
                elimina_sorgenti INTEGER NOT NULL,
                file_archiviati INTEGER NOT NULL,
                nome_archivio TEXT
            )
        """)


def salva_scansione(
    db_path: Path,
    cartella_log: str,
    giorni: int,
    elimina_sorgenti: bool,
    file_archiviati: int,
    nome_archivio: str | None,
    tipo_file: str = "*.log",
):
    """Inserisce una nuova riga nel database con i dati della scansione."""
    data_ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO scansioni (
                data_ora, cartella_log, tipo_file, giorni_retention,
                elimina_sorgenti, file_archiviati, nome_archivio
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data_ora,
                cartella_log,
                tipo_file,
                giorni,
                int(elimina_sorgenti),
                file_archiviati,
                nome_archivio,
            ),
        )


def leggi_storico(db_path: Path) -> list[tuple]:
    """Recupera tutte le scansioni salvate dalla più recente alla più vecchia."""
    if not db_path.exists():
        return []
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("""
            SELECT id, data_ora, cartella_log, tipo_file, giorni_retention,
                   elimina_sorgenti, file_archiviati, nome_archivio
            FROM scansioni
            ORDER BY id DESC
        """)
        return cursor.fetchall()