# OSINT Collector — Technical Reference

> Multi-source intelligence scraper with dynamic term expansion, 5-pattern regex extraction and infinite iteration loop.

---

## How It Works

```
User input: "restaurante"
     │
     ▼
CORRELATE_DB lookup
     │
     ├─ Match found → use ONLY correlate terms (not concatenated)
     │   "restaurante" → ["comida", "pizza", "burger", "sushi", ...]
     │
     └─ No match → generate term variations
         "termo" → ["termo", "termo online", "melhor termo", ...]
     │
     ▼
For each term × 50+ sources:
     │
     ├─ HTTP request (requests) → parse HTML → regex extraction
     └─ Selenium (JS-heavy sites) → scroll → parse → regex extraction
     │
     ▼
Phone/email extracted → validate → deduplicate → append to merged.csv
     │
     ▼
Next iteration: +2 new terms → repeat
```

---

## Dynamic Term Expansion

Each iteration unlocks 2 additional correlate terms:

```
Iteration 1:  10 terms
Iteration 2:  12 terms  (+2)
Iteration 3:  14 terms  (+2)
Iteration N:  10 + (N×2) terms
```

**Example — "restaurante":**
```
Iter 1: comida, pizza, burger, sushi, churrascaria, café, bar, lanchonete, padaria, confeitaria
Iter 2: + sorveteria, choperia
Iter 3: + boteco, cantina
Iter 4: + pizzaria, rodízio
...
```

---

## Regex Extraction Engine

Five patterns cover all common phone formats found in the wild:

```python
r'\+?55\s*\(?\d{2}\)?\s*\d{4,5}-?\d{4}'   # +55 (11) 99999-9999
r'\(?\d{2}\)?\s*\d{4,5}-?\d{4}'             # (11) 99999-9999
r'(\d{2})(\d{4,5})(\d{4})'                  # 11999999999
r'\b(\d{10,11})\b'                           # boundary-anchored
r'(\d{2})\s*(\d{4,5})\s*(\d{4})'            # 11 99999 9999
```

Deduplication is handled at extraction time via a `set()` keyed on the cleaned number string.

---

## Source Coverage (50+)

**Brazilian Marketplaces**
Mercado Livre, OLX, Classificados, Vivanuncios, Anúncios

**Business Directories**
Google, Google Maps, Yellow Pages, Yelp, SuperPages, MerchantCircle, Thumbtack, HomeAdvisor

**Professional Networks**
LinkedIn, LinkedIn Companies

**Social / Content**
Twitter, Reddit, Quora, Medium, Tumblr, Pinterest, Flickr, Imgur

**Developer Platforms**
GitHub, Stack Overflow, Dev.to, Hashnode

**Creative Platforms**
Behance, Dribbble, DeviantArt, ArtStation, WeHeartIt

**Video Platforms**
Vimeo, Dailymotion, Twitch, Rumble, Odysee, BitChute

**Decentralized**
Minds, Mastodon

**Real Estate**
Zillow, Realtor, Trulia, Apartments

**Classifieds**
Craigslist, Letgo

---

## Category Intelligence Database

```python
CORRELATE_DB = {
    'restaurante': ['comida', 'pizza', 'burger', 'sushi', 'churrascaria', ...],
    'clínica':     ['médico', 'dentista', 'hospital', 'farmácia', ...],
    'loja':        ['e-commerce', 'vendas', 'produtos', 'varejo', ...],
    'serviço':     ['profissional', 'técnico', 'reparo', 'manutenção', ...],
    'imóvel':      ['casa', 'apartamento', 'aluguel', 'escritório', ...],
    'educação':    ['escola', 'universidade', 'curso', 'professor', ...],
    'beleza':      ['salão', 'cabelo', 'manicure', 'estética', ...],
    'fitness':     ['academia', 'musculação', 'yoga', 'pilates', ...],
    'viagem':      ['hotel', 'pousada', 'turismo', 'hospedagem', ...],
    'transporte':  ['táxi', 'uber', 'frete', 'logística', ...],
}
```

Term resolution is exact-match on category key — no concatenation with the original input.

---

## Anti-Bot Evasion

```python
# Randomized delay between every request
time.sleep(random.uniform(0.2, 0.8))

# Realistic browser fingerprint
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

# Headless Chrome flags
--disable-blink-features=AutomationControlled
--no-sandbox
--disable-dev-shm-usage
--mute-audio
excludeSwitches: ["enable-logging"]
```

---

## Output Schema

`contatos/merged.csv`:

```csv
numero,nome,email,fonte,data
5512999999999,Name,email@domain.com,Google Maps,2025-01-15
5511988888888,Name,,OLX,2025-01-15
```

- Persists across sessions (append-only, no overwrites)
- Deduplicated by phone number on load
- Real-time flush on every new contact found

---

## Configuration

```python
Scraper(
    delay_min=0.2,   # Minimum delay between requests (seconds)
    delay_max=0.8,   # Maximum delay
    headless=True    # False to watch browser in real-time
)
```

---

## Integration with Communication Engine

```bash
# Terminal 1 — run collector
python3 scraper_all.py
# Input: restaurante

# Terminal 2 — run sender (while collector is running)
python3 app.py
# [2] Read from file → contatos/merged.csv
```

The sender reads `merged.csv` at startup — any contacts collected before execution are included automatically.

---

## Graceful Shutdown

`Ctrl+C` triggers `SIGINT` handler:

```python
def signal_handler(sig, frame):
    global STOP_FLAG
    STOP_FLAG = True
    sys.exit(0)
```

All data already written to disk is preserved. No data loss on interrupt.
