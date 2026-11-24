import zipfile
from datetime import datetime, timedelta
from pathlib import Path


def get_old_logs(logs_dir: Path, days: int) -> list[Path]:
    """Trova tutti i file .log modificati prima della soglia di giorni impostata."""
    cutoff_time = datetime.now() - timedelta(days=days)
    old_files = []

    if not logs_dir.exists():
        return []

    for file_path in logs_dir.glob("*.log"):
        if file_path.is_file():
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_mtime < cutoff_time:
                old_files.append(file_path)

    return old_files


def create_backup_zip(files_to_backup: list[Path], backup_dir: Path) -> Path:
    """Comprime i file selezionati in un unico archivio ZIP con data e ora."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = backup_dir / f"backup_logs_{timestamp}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_backup:
            zipf.write(file, arcname=file.name)

    return zip_path