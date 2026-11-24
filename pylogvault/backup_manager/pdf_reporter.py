from datetime import datetime
from pathlib import Path
from fpdf import FPDF


def generate_pdf_report(
    backup_zip: Path,
    processed_files: list[Path],
    backup_dir: Path,
    days: int,
    deleted: bool,
) -> Path:
    """Genera un report in formato PDF con i dettagli del backup eseguito."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Intestazione
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "PyLogVault - Report di Elaborazione Log", ln=True, align="C")
    pdf.ln(5)

    # Calcolo dimensioni
    total_bytes = sum(f.stat().st_size for f in processed_files)
    total_kb = round(total_bytes / 1024, 2)
    zip_kb = round(backup_zip.stat().st_size / 1024, 2)

    # Parametri e risultati
    pdf.set_font("Helvetica", "", 11)
    righe_info = [
        f"Data e ora scansione: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "Tipo di file cercati: *.log",
        f"Soglia giorni (retention): {days} giorni",
        f"Sorgenti originali eliminati: {'Si' if deleted else 'No'}",
        f"Archivio ZIP generato: {backup_zip.name} ({zip_kb} KB)",
        f"Numero file archiviati: {len(processed_files)} ({total_kb} KB totali)",
    ]

    for riga in righe_info:
        pdf.cell(0, 8, riga, ln=True)

    # Elenco dei file inseriti nello ZIP
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Elenco dei file archiviati:", ln=True)

    pdf.set_font("Helvetica", "", 10)
    for f in processed_files:
        pdf.cell(0, 6, f"- {f.name}", ln=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = backup_dir / f"report_{timestamp}.pdf"
    pdf.output(str(pdf_path))
    return pdf_path