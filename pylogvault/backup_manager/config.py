from pathlib import Path

# Percorso radice del progetto (funziona uguale su Windows e Linux)
BASE_DIR = Path(__file__).resolve().parent.parent

# Cartelle di default
LOGS_DIR = BASE_DIR / "storage" / "logs"
BACKUP_DIR = BASE_DIR / "storage" / "backups"

# File del database SQLite
DB_PATH = BASE_DIR / "storage" / "history.db"

# Giorni di retention di default
DEFAULT_RETENTION_DAYS = 7