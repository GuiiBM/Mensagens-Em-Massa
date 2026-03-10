#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import csv
import os
import re
import signal
import sys
from datetime import datetime
from urllib.parse import urljoin, quote

MERGED_FILE = 'contatos/merged.csv'
STOP_FLAG = False

CORRELATE_DB = {
    'restaurante': ['comida', 'pizza', 'burger', 'sushi', 'churrascaria', 'café', 'bar', 'lanchonete', 'padaria', 'confeitaria', 'sorveteria', 'choperia', 'boteco', 'cantina', 'pizzaria', 'rodízio', 'buffet', 'self-service', 'fast food', 'cozinha', 'gastronomia', 'culinária', 'prato', 'refeição', 'almoço', 'jantar', 'café da manhã', 'brunch', 'happy hour'],
    'clínica': ['médico', 'dentista', 'hospital', 'farmácia', 'saúde', 'consultório', 'psicólogo', 'fisioterapeuta', 'nutricionista', 'dermatologista', 'oftalmologista', 'cardiologista', 'pediatra', 'ginecologista', 'ortopedista', 'cirurgião', 'anestesista', 'radiologista', 'enfermeiro', 'terapeuta', 'acupuntor', 'quiropraxia', 'homeopatia', 'medicina alternativa'],
    'loja': ['loja online', 'e-commerce', 'compras', 'vendas', 'produtos', 'varejo', 'atacado', 'distribuidor', 'fornecedor', 'revendedor', 'franquia', 'boutique', 'outlet', 'shopping', 'galeria', 'centro comercial', 'loja física', 'loja virtual', 'marketplace', 'plataforma'],
    'serviço': ['profissional', 'técnico', 'reparo', 'manutenção', 'instalação', 'limpeza', 'encanador', 'eletricista', 'pintor', 'carpinteiro', 'pedreiro', 'jardineiro', 'mecânico', 'chaveiro', 'vidraceiro', 'marceneiro', 'soldador', 'serralheiro'],
    'imóvel': ['casa', 'apartamento', 'aluguel', 'venda', 'imobiliária', 'terreno', 'condomínio', 'kitnet', 'studio', 'cobertura', 'sobrado', 'chácara', 'sítio', 'fazenda', 'lote', 'sala comercial', 'loja', 'galpão', 'escritório', 'comercial', 'residencial'],
    'educação': ['escola', 'universidade', 'faculdade', 'curso', 'aula', 'professor', 'aluno', 'educação', 'ensino', 'aprendizado', 'treinamento', 'capacitação', 'workshop', 'seminário', 'palestra', 'tutoria', 'mentoria', 'coaching'],
    'beleza': ['salão', 'cabelo', 'manicure', 'pedicure', 'spa', 'massagem', 'estética', 'maquiagem', 'depilação', 'tatuagem', 'piercing', 'unhas', 'cabelereiro', 'cabeleireiro', 'barbeiro', 'sobrancelha', 'limpeza de pele'],
    'fitness': ['academia', 'musculação', 'yoga', 'pilates', 'crossfit', 'personal trainer', 'nutrição', 'dieta', 'treino', 'exercício', 'esporte', 'corrida', 'natação', 'dança', 'zumba', 'boxe', 'muay thai'],
    'viagem': ['hotel', 'pousada', 'hostel', 'resort', 'turismo', 'agência de viagens', 'passagens', 'pacotes', 'roteiros', 'tours', 'excursões', 'hospedagem', 'acomodação', 'destino', 'férias'],
    'transporte': ['táxi', 'uber', 'ônibus', 'metrô', 'trem', 'carro', 'moto', 'bicicleta', 'scooter', 'aluguel de carro', 'motorista', 'frete', 'mudança', 'logística', 'entrega'],
}

def signal_handler(sig, frame):
    global STOP_FLAG
    STOP_FLAG = True
    print("\n\n✅ Parando...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class Scraper:
    def __init__(self, delay_min=0.2, delay_max=0.8, headless=True):
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.headless = headless
        self.all_contacts = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self._load_existing()

    def _load_existing(self):
        if os.path.exists(MERGED_FILE):
            try:
                with open(MERGED_FILE, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('numero'):
                            self.all_contacts[row['numero']] = row
            except:
                pass

    def _delay(self):
        global STOP_FLAG
        if STOP_FLAG:
            sys.exit(0)
        time.sleep(random.uniform(self.delay_min, self.delay_max))

    def _extract_phones(self, text):
        patterns = [
            r'\+?55\s*\(?(\d{2})\)?\s*(\d{4,5})-?(\d{4})',
            r'\(?(\d{2})\)?\s*(\d{4,5})-?(\d{4})',
            r'(\d{2})(\d{4,5})(\d{4})',
            r'\b(\d{10,11})\b',
            r'(\d{2})\s*(\d{4,5})\s*(\d{4})',
        ]
        phones = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                phone = ''.join(match) if isinstance(match, tuple) else match
                if 10 <= len(phone) <= 15:
                    phones.append(phone)
        return list(set(phones))

    def _extract_emails(self, text):
        return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

    def _add_contact(self, numero, nome, email, fonte):
        if numero:
            phone = ''.join(filter(str.isdigit, numero))
            if 10 <= len(phone) <= 15 and phone not in self.all_contacts:
                self.all_contacts[phone] = {
                    'numero': phone,
                    'nome': nome[:100] if nome else '',
                    'email': email[:100] if email else '',
                    'fonte': fonte,
                    'data': datetime.now().strftime('%Y-%m-%d')
                }
                self._save()
                return True
        return False

    def _save(self):
        os.makedirs('contatos', exist_ok=True)
        try:
            with open(MERGED_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['numero', 'nome', 'email', 'fonte', 'data'])
                writer.writeheader()
                writer.writerows(self.all_contacts.values())
        except:
            pass

    def _get_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(options=chrome_options)

    def _scrape_text(self, text, search, fonte):
        global STOP_FLAG
        if STOP_FLAG:
            sys.exit(0)
        phones = self._extract_phones(text)
        emails = self._extract_emails(text)
        count = 0
        for i, phone in enumerate(phones):
            email = emails[i] if i < len(emails) else ''
            if self._add_contact(phone, search, email, fonte):
                count += 1
        return count

    def scrape(self, search, fonte, url_template):
        global STOP_FLAG
        if STOP_FLAG:
            sys.exit(0)
        try:
            url = url_template.format(search=quote(search))
            response = self.session.get(url, timeout=5)
            count = self._scrape_text(response.text, search, fonte)
            return count
        except:
            return 0

    def scrape_selenium(self, search, fonte, url_template):
        global STOP_FLAG
        if STOP_FLAG:
            sys.exit(0)
        try:
            driver = self._get_driver()
            url = url_template.format(search=quote(search))
            driver.get(url)
            time.sleep(1)
            for _ in range(2):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(0.3)
            count = self._scrape_text(driver.page_source, search, fonte)
            driver.quit()
            return count
        except:
            return 0

SOURCES = [
    ('Google', 'https://www.google.com/search?q={search}+telefone'),
    ('Google Maps', 'https://www.google.com/maps/search/{search}'),
    ('Yellow Pages', 'https://www.yellowpages.com/search?search_terms={search}'),
    ('Yelp', 'https://www.yelp.com/search?find_desc={search}'),
    ('SuperPages', 'https://www.superpages.com/search?q={search}'),
    ('MerchantCircle', 'https://www.merchantcircle.com/search?q={search}'),
    ('Angie\'s List', 'https://www.angieslist.com/search?q={search}'),
    ('Thumbtack', 'https://www.thumbtack.com/search?q={search}'),
    ('ServiceMaster', 'https://www.servicemaster.com/search?q={search}'),
    ('HomeAdvisor', 'https://www.homeadvisor.com/search?q={search}'),
    ('Houzz', 'https://www.houzz.com/search?q={search}'),
    ('Zillow', 'https://www.zillow.com/homes/for_sale/{search}'),
    ('Realtor', 'https://www.realtor.com/search?q={search}'),
    ('Trulia', 'https://www.trulia.com/search?q={search}'),
    ('Apartments', 'https://www.apartments.com/search?q={search}'),
    ('Craigslist', 'https://www.craigslist.org/search/sss?query={search}'),
    ('Letgo', 'https://letgo.com/en-us/search?q={search}'),
    ('Mercado Livre', 'https://www.mercadolivre.com.br/jm/search?q={search}'),
    ('OLX', 'https://www.olx.com.br/brasil?q={search}'),
    ('Classificados', 'https://www.classificados.com.br/search?q={search}'),
    ('Vivanuncios', 'https://www.vivanuncios.com.br/search?q={search}'),
    ('Anúncios', 'https://www.anuncios.com.br/search?q={search}'),
    ('Skokka', 'https://www.skokka.com.br/search?q={search}'),
    ('Garotas', 'https://www.garotas.com.br/search?q={search}'),
    ('Acompanhantes', 'https://www.acompanhantes.com.br/search?q={search}'),
    ('Linkedin', 'https://www.linkedin.com/search/results/people/?keywords={search}'),
    ('LinkedIn Companies', 'https://www.linkedin.com/search/results/companies/?keywords={search}'),
    ('Twitter', 'https://twitter.com/search?q={search}'),
    ('Reddit', 'https://www.reddit.com/search/?q={search}'),
    ('Quora', 'https://www.quora.com/search?q={search}'),
    ('Medium', 'https://medium.com/search?q={search}'),
    ('GitHub', 'https://github.com/search?q={search}'),
    ('Stack Overflow', 'https://stackoverflow.com/search?q={search}'),
    ('Dev.to', 'https://dev.to/search?q={search}'),
    ('Hashnode', 'https://hashnode.com/search?q={search}'),
    ('Pinterest', 'https://www.pinterest.com/search/?q={search}'),
    ('Flickr', 'https://www.flickr.com/search/?q={search}'),
    ('Imgur', 'https://imgur.com/search?q={search}'),
    ('Tumblr', 'https://www.tumblr.com/search/{search}'),
    ('WeHeartIt', 'https://weheartit.com/search?query={search}'),
    ('Behance', 'https://www.behance.net/search?search={search}'),
    ('Dribbble', 'https://dribbble.com/search?q={search}'),
    ('DeviantArt', 'https://www.deviantart.com/search?q={search}'),
    ('ArtStation', 'https://www.artstation.com/search?q={search}'),
    ('Vimeo', 'https://vimeo.com/search?q={search}'),
    ('Dailymotion', 'https://www.dailymotion.com/search/{search}'),
    ('Twitch', 'https://www.twitch.tv/search?query={search}'),
    ('Rumble', 'https://rumble.com/search?q={search}'),
    ('Odysee', 'https://odysee.com/$/search?q={search}'),
    ('BitChute', 'https://www.bitchute.com/search/?query={search}'),
    ('Minds', 'https://www.minds.com/search?q={search}'),
    ('Mastodon', 'https://mastodon.social/search?q={search}'),
]

def get_correlate_terms(term, iteration=1):
    found_category = False
    
    for key, values in CORRELATE_DB.items():
        if key in term.lower():
            limit = min(10 + iteration * 2, len(values))
            return values[:limit]
    
    base_terms = [
        term,
        term + ' online',
        term + ' perto de mim',
        term + ' barato',
        term + ' promoção',
        term + ' desconto',
        term + ' 24 horas',
        term + ' entrega',
        term + ' whatsapp',
        term + ' telefone',
        term + ' contato',
        term + ' empresa',
        term + ' profissional',
        term + ' serviço',
        term + ' produto',
        'melhor ' + term,
        'top ' + term,
    ]
    limit = min(10 + iteration * 2, len(base_terms))
    return base_terms[:limit]

def main():
    global STOP_FLAG
    
    print("🤖 Web Scraper - Busca Brutal")
    print("=" * 60)
    
    search_term = input("O que procurar: ").strip()
    if not search_term:
        print("❌ Termo vazio")
        return
    
    scraper = Scraper()
    
    print(f"\n🔍 Buscando: {search_term}")
    print(f"🌐 Fontes: {len(SOURCES)}")
    print(f"📁 Arquivo: {MERGED_FILE}")
    print(f"⏳ Iniciando busca brutal...\n")
    print("Pressione Ctrl+C para parar imediatamente\n")
    
    iteration = 0
    while not STOP_FLAG:
        iteration += 1
        correlates = get_correlate_terms(search_term, iteration)
        
        print(f"\n🔄 Iteração {iteration} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Total: {len(scraper.all_contacts)} contatos")
        print(f"📚 Termos: {len(correlates)} (+{min(2, len(correlates) - 10)})\n")
        
        for term in correlates:
            if STOP_FLAG:
                sys.exit(0)
            for fonte, url_template in SOURCES:
                if STOP_FLAG:
                    sys.exit(0)
                try:
                    if 'instagram' in url_template or 'facebook' in url_template or 'youtube' in url_template or 'tiktok' in url_template:
                        count = scraper.scrape_selenium(term, fonte, url_template)
                    else:
                        count = scraper.scrape(term, fonte, url_template)
                    
                    if count > 0:
                        print(f"  {fonte}: +{count}", end=' | ', flush=True)
                    
                    scraper._delay()
                except:
                    pass
            print()

if __name__ == "__main__":
    main()
