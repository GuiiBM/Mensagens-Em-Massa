#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def main():
    print("🚀 Instalador Automático - WhatsApp Sender")
    print("=" * 50)
    
    # Detecta SO
    sistema = platform.system()
    print(f"📟 Sistema: {sistema}")
    
    # Verifica Python
    py_version = sys.version_info
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 7):
        print("❌ Python 3.7+ necessário")
        sys.exit(1)
    print(f"✅ Python {py_version.major}.{py_version.minor}")
    
    # Cria pasta de contatos
    os.makedirs("contatos", exist_ok=True)
    print("✅ Pasta 'contatos/' criada")
    
    # Instala dependências
    print("\n📦 Instalando dependências...")
    result = run_cmd(f"{sys.executable} -m pip install -q pywhatkit openpyxl pandas")
    
    if result.returncode == 0:
        print("✅ Dependências instaladas")
    else:
        print("❌ Erro na instalação")
        sys.exit(1)
    
    print("\n✅ INSTALAÇÃO CONCLUÍDA!")
    print("\n▶️  Execute: python3 app.py")

if __name__ == "__main__":
    main()
