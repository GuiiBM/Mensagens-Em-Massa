# 🤖 Web Scraper - Busca Brutal com Crescimento Dinâmico

Sistema de web scraping com busca brutal em 50+ fontes e termos que crescem a cada iteração.

## 🚀 Instalação e Uso

```bash
# Instalar
python3 install.py

# Executar (busca brutal infinita)
python3 scraper_all.py
```

## ✨ Características

✅ **50+ fontes de coleta** - Máxima cobertura
✅ **Arquivo único permanente** - `contatos/merged.csv`
✅ **Busca brutal** - Delays mínimos (0.2-0.8s)
✅ **Crescimento dinâmico** - +2 termos a cada iteração
✅ **Termos correlatos automáticos** - Busca por temas relacionados
✅ **Busca infinita** - Continua enquanto ativo
✅ **Parada imediata** - Ctrl+C para parar
✅ **Sem duplicatas** - Cada número aparece uma vez
✅ **Atualização em tempo real** - Salva cada novo contato

## 📊 Crescimento Dinâmico de Termos

A cada iteração, o scraper adiciona +2 novos termos correlatos:

```
Iteração 1: 10 termos
Iteração 2: 12 termos
Iteração 3: 14 termos
Iteração 4: 16 termos
Iteração 5: 18 termos
...
```

**Exemplo com "restaurante":**
- Iteração 1: restaurante, comida, pizza, burger, sushi, churrascaria, café, bar, lanchonete, padaria
- Iteração 2: + confeitaria, sorveteria
- Iteração 3: + choperia, boteco
- Iteração 4: + cantina, pizzaria
- Iteração 5: + rodízio, buffet
- ...

## 📁 Arquivo Único

`contatos/merged.csv` - Todos os contatos:
```csv
numero,nome,email,fonte,data
5512999999999,João Silva,joao@email.com,Google,2024-01-15
5511988888888,Maria Santos,maria@email.com,OLX,2024-01-15
```

## 🔗 Integração com WhatsApp

```bash
# Terminal 1: Deixar scraper rodando
python3 scraper_all.py
# O que procurar: seu termo

# Terminal 2: Usar contatos
python3 app.py
# Escolha [2] Ler de arquivo
# merged.csv
```

## 📝 Exemplo Completo

```bash
$ python3 scraper_all.py
O que procurar: restaurante

🔍 Buscando: restaurante
🌐 Fontes: 50+
📁 Arquivo: contatos/merged.csv
⏳ Iniciando busca brutal...

Pressione Ctrl+C para parar imediatamente

🔄 Iteração 1 - 14:30:22
📊 Total: 0 contatos
📚 Termos: 10 (+0)

  Google: +5 | Google Maps: +12 | Yellow Pages: +8 | Yelp: +6 | SuperPages: +4 | MerchantCircle: +3 | Angie's List: +2 | Thumbtack: +1 | ServiceMaster: +0 | HomeAdvisor: +2 | Houzz: +1 | Zillow: +0 | Realtor: +3 | Trulia: +2 | Apartments: +0 | Craigslist: +4 | Letgo: +1 | Mercado Livre: +2 | OLX: +5 | Classificados: +3 | Vivanuncios: +2 | Anúncios: +1 | Skokka: +0 | Garotas: +0 | Acompanhantes: +0 | LinkedIn: +1 | LinkedIn Companies: +2 | Twitter: +3 | Reddit: +1 | Quora: +0 | Medium: +0 | GitHub: +0 | Stack Overflow: +0 | Dev.to: +0 | Hashnode: +0 | Pinterest: +2 | Flickr: +1 | Imgur: +0 | Tumblr: +1 | WeHeartIt: +0 | Behance: +0 | Dribbble: +0 | DeviantArt: +0 | ArtStation: +0 | Vimeo: +1 | Dailymotion: +0 | Twitch: +0 | Rumble: +0 | Odysee: +0 | BitChute: +0 | Minds: +0 | Mastodon: +0

  Google: +4 | Google Maps: +10 | Yellow Pages: +6 | Yelp: +5 | ...

🔄 Iteração 2 - 14:35:45
📊 Total: 250 contatos
📚 Termos: 12 (+2)

  Google: +3 | Google Maps: +8 | Yellow Pages: +5 | Yelp: +4 | ...
  Google: +2 | Google Maps: +6 | Yellow Pages: +4 | Yelp: +3 | ...

🔄 Iteração 3 - 14:41:10
📊 Total: 450 contatos
📚 Termos: 14 (+2)

  Google: +2 | Google Maps: +5 | Yellow Pages: +3 | Yelp: +2 | ...
  Google: +1 | Google Maps: +4 | Yellow Pages: +2 | Yelp: +2 | ...
  Google: +1 | Google Maps: +3 | Yellow Pages: +2 | Yelp: +1 | ...
```

Pressione `Ctrl+C` para parar imediatamente.

## ⚙️ Configuração

Edite `scraper_all.py`:
- `delay_min=0.2` - Delay mínimo (brutal)
- `delay_max=0.8` - Delay máximo
- `headless=True` - Sem interface gráfica

## 🎯 Dicas

- Deixe rodando enquanto trabalha
- Quanto mais tempo, mais contatos
- Termos crescem +2 a cada iteração
- Pressione `Ctrl+C` para parar imediatamente
- Arquivo atualiza em tempo real
- Tente diferentes termos

## 🚀 Fluxo Recomendado

1. **Instalar**: `python3 install.py`
2. **Deixar rodando**: `python3 scraper_all.py` (Terminal 1)
3. **Usar contatos**: `python3 app.py` (Terminal 2)
4. **Parar quando quiser**: `Ctrl+C` (parada imediata)

## 📊 Cobertura

- **50+ fontes** de coleta
- **Crescimento dinâmico** de termos (+2 por iteração)
- **Busca infinita** enquanto ativo
- **Sem bloqueios** - Delays respeitosos
- **Dentro da lei** - Sem violação de ToS
- **Parada imediata** - Ctrl+C funciona
