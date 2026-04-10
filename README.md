# Massive OSINT & Communication Framework

> Automated intelligence collection and mass communication framework via WhatsApp Web — built for precision, speed and anti-bot evasion.

---

## Architecture Overview

```
Mensagens-Em-Massa/
├── app.py              # WhatsApp automation engine (Selenium)
├── scraper_all.py      # Multi-source OSINT intelligence collector
├── install.py          # Automated dependency bootstrapper
├── requirements.txt    # Dependency manifest
├── contatos/           # Contact intelligence output (CSV/XLSX)
├── mensagens/          # Message templates (.txt)
└── imagens/            # Media payloads (JPG, PNG, GIF, WEBP)
```

---

## Stack

| Layer                   | Technology                         |
| ----------------------- | ---------------------------------- |
| Automation              | Selenium WebDriver + ChromeDriver  |
| Intelligence Collection | Requests + BeautifulSoup4          |
| Data Processing         | Pandas + Regex Engine (5 patterns) |
| Media Processing        | Pillow (PNG normalization)         |
| Input Simulation        | PyAutoGUI                          |
| Data Ingestion          | openpyxl (Excel), CSV              |

---

## Quick Start

```bash
# Bootstrap environment
python3 install.py

# Run OSINT collector (Terminal 1)
python3 scraper_all.py

# Run communication engine (Terminal 2)
python3 app.py
```

---

## Module 1 — Communication Engine (`app.py`)

Automates WhatsApp Web via Selenium with direct DOM manipulation, bypassing WhatsApp's standard API restrictions.

### Phone Number Validation Pipeline

Multi-layer regex validation that filters noise from raw data:

```
Raw input → Strip non-digits → Length check (10–15) → Pattern match
         → Reject: dates (ddmmyyyy), CEPs (xxxxx-xxx), years (20xx)
         → Accept: BR mobile (11 digits, 3rd digit = 9), international (12–15)
         → Format: auto-prefix 55 for Brazilian numbers
```

**Examples:**

```
"11999999999"   → "5511999999999"  ✅ BR mobile
"351912345678"  → "351912345678"   ✅ International
"01062025"      → rejected         ❌ Date pattern
"12345-678"     → rejected         ❌ CEP pattern
```

### Delivery Modes & Throughput

| Mode         | Process                               | Time/msg | Throughput   |
| ------------ | ------------------------------------- | -------- | ------------ |
| Text only    | URL pre-fill → click send            | ~3s      | ~20 msg/min  |
| Image only   | file input injection → DOM click     | ~13s     | ~4.6 msg/min |
| Image + Text | image send → URL reload → text send | ~18s     | ~3.3 msg/min |

### Sending Flow

```
1. Load contact URL: web.whatsapp.com/send?phone={number}
2. Wait for DOM: //div[@contenteditable="true"][@data-tab="10"]
3. Inject file path into <input type="file"> (image mode)
4. Wait for preview render (6s)
5. Locate send button: //span[@data-icon="send"]
6. Execute click → fallback to PyAutoGUI Enter
7. Verify delivery → next contact
```

### Input Formats

**CSV:**

```csv
numero
5512999999999
5511988888888
351912345678
```

**Excel:** Any column, any sheet — the engine scans all cells.

---

## Module 2 — OSINT Collector (`scraper_all.py`)

Multi-source intelligence collector with dynamic term expansion. Scrapes 50+ public sources simultaneously, extracting phone numbers and emails using a 5-pattern regex engine.

→ Full documentation: [SCRAPER.md](SCRAPER.md)

---

## Phone Regex Engine

Five overlapping patterns ensure maximum extraction coverage:

```python
r'\+?55\s*\(?\d{2}\)?\s*\d{4,5}-?\d{4}'   # BR formatted
r'\(?\d{2}\)?\s*\d{4,5}-?\d{4}'             # BR unformatted
r'(\d{2})(\d{4,5})(\d{4})'                  # Raw digits
r'\b(\d{10,11})\b'                           # Boundary match
r'(\d{2})\s*(\d{4,5})\s*(\d{4})'            # Space-separated
```

---

## Anti-Bot Evasion

- Randomized delays between requests (`0.2–0.8s`)
- Realistic User-Agent header
- Headless Chrome with `--disable-blink-features=AutomationControlled`
- Sequential (not parallel) requests to avoid rate-limit triggers
- DOM-based interaction instead of JavaScript injection where possible

---

## Data Output

`contatos/merged.csv` — deduplicated, persistent across sessions:

```csv
numero,nome,email,fonte,data
5512999999999,Target Name,contact@domain.com,Google Maps,2025-01-15
```

---

## Operational Notes

- No API keys required — operates entirely on public web interfaces
- Local-first: zero data leaves the machine
- WhatsApp session persists via Chrome profile (no repeated QR scans)
- Ctrl+C triggers graceful shutdown with data flush
- Excel files: all sheets, all columns scanned automatically


---

## Ethical Use e Disclaimer

* This project was developed for educational and automation research purposes. The author is not responsible for any misuse of the tool for spamming or violation of terms of service
