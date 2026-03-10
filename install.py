#!/usr/bin/env python3
import os
import subprocess
import sys
import csv

def main():
    print("🚀 Instalador - Web Scraper + WhatsApp Sender")
    print("=" * 60)
    
    print("\n📥 Instalando dependências...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependências instaladas")
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    print("\n📁 Criando pastas...")
    folders = ['contatos', 'mensagens', 'imagens']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ {folder}/")
    
    print("\n📝 Criando arquivo merged.csv...")
    merged_file = 'contatos/merged.csv'
    with open(merged_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['numero', 'nome', 'email', 'fonte', 'data'])
        writer.writeheader()
    print(f"✅ {merged_file} criado")
    
    print("\n✅ Instalação concluída!")
    print("\n🚀 Para começar:")
    print("   python3 scraper_all.py")
    print("   python3 app.py")

if __name__ == "__main__":
    main()
