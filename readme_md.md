# PyLogVault 📦

**PyLogVault** è un'applicazione grafica e da riga di comando sviluppata in Python per la gestione automatizzata, l'archiviazione e la manutenzione dei file di log di sistema in ambienti **GNU/Linux** e **Windows**.

Il progetto è stato realizzato come prova finale per il corso **Cloud Specialist** presso l'**ITS ICT Piemonte** (Anno Formativo 2025/2027).

---

## 🚀 Caratteristiche Principali

- 🖥️ **Interfaccia Grafica (GUI):** Sviluppata in `tkinter` con file dialog nativi e visualizzatore di storico.
- 📦 **Archiviazione ZIP:** Compressione automatica dei file `.log` più vecchi della soglia di retention selezionata.
- 📄 **Reportistica PDF:** Generazione automatica di un report PDF dettagliato per ogni operazione tramite `fpdf2`.
- 🗄️ **Database SQLite3:** Registrazione persistente di tutte le scansioni (parametri usati, timestamp, file elaborati e dimensione).
- 🧹 **Pulizia Condizionale:** Opzione per la rimozione sicura dei file log sorgenti solo a valle del completamento del backup.

---

## 📁 Struttura del Progetto

```text
pylogvault/
│
├── backup_manager/
│   ├── __init__.py
│   ├── config.py         # Configurazione percorsi e retention default
│   ├── archiver.py       # Scansione file system e compressione ZIP
│   ├── database.py       # Gestione database SQLite3 (history.db)
│   └── pdf_reporter.py   # Generazione del report PDF
│
├── storage/
│   ├── logs/             # Directory contenente i file .log da processare
│   ├── backups/          # Output degli archivi .zip e dei report .pdf
│   └── history.db        # Database SQLite3 creato automaticamente
│
├── gui.py                # Entry point con interfaccia grafica Tkinter
├── requirements.txt      # Dipendenze Python (fpdf2)
└── README.md             # Guida all'uso e documentazione
```

---

## 💻 Requisiti di Sistema

- **Python 3.10+**
- **GNU/Linux** (Ubuntu, Debian, Fedora, RHEL) o **Windows 10/11**
- Pacchetti di sistema (solo per sistemi Linux/Debian): `python3-tk` e `python3-venv`

---

## 🛠️ Guida all'Installazione ed Esecuzione

### 🐧 Esecuzione su GNU/Linux (Ubuntu / Debian)

1. **Installazione delle dipendenze di sistema:**
   ```bash
   sudo apt update
   sudo apt install -y python3-tk python3-venv git
   ```

2. **Clonazione / Estrazione del progetto e spostamento nella cartella:**
   ```bash
   cd pylogvault
   ```

3. **Creazione ed attivazione dell'ambiente virtuale:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Installazione dei pacchetti Python:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Avvio dell'applicazione:**
   ```bash
   python3 gui.py
   ```

---

### 🪟 Esecuzione su Windows

1. Apri PowerShell nella cartella del progetto (`pylogvault`).
2. Attiva l'ambiente virtuale:
   ```powershell
   .\venv\Scripts\activate
   ```
3. Avvia l'interfaccia grafica:
   ```powershell
   python gui.py
   ```

---

## 📖 Come Utilizzare l'Applicazione

1. **Seleziona la cartella dei Log:** Clicca su **Sfoglia** per scegliere la directory contenente i file `.log` da analizzare.
2. **Seleziona la cartella di Backup:** Scegli dove salvare l'archivio `.zip` e il report `.pdf`.
3. **Imposta i Giorni di Retention:** Specifica la soglia temporale (es. `0` per prendere tutti i file di test, oppure `7` per log più vecchi di una settimana).
4. **Cancellazione Sorgenti (Opzionale):** Spunta la casella per eliminare i file `.log` originali dopo l'avvenuta creazione dello ZIP.
5. **Avvia Scansione e Backup:** Clicca sul pulsante verde per avviare il processo.
6. **Visualizza Storico:** Clicca sul pulsante blu per aprire la finestra di consultazione del database **SQLite3**, dove potrai scorrere tutte le operazioni effettuate in precedenza.

---

## 👨‍💻 Autore e Informazioni

- **Studente:** Christian Cavagnero
- **Docente:** Prof. Massimo Papa
- **Corso:** Cloud Specialist — ITS ICT Piemonte
- **Anno Formativo:** 2025/2027