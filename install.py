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
    os.makedirs("mensagens", exist_ok=True)
    os.makedirs("imagens", exist_ok=True)
    print("✅ Pastas 'contatos/', 'mensagens/' e 'imagens/' criadas")
    
    # Instala dependências
    print("\n📦 Instalando dependências...")
    result = run_cmd(f"{sys.executable} -m pip install -q selenium openpyxl pandas pyperclip Pillow pyautogui")
    
    if result.returncode == 0:
        print("✅ Dependências instaladas")
    else:
        print("❌ Erro na instalação")
        sys.exit(1)
    
    # Instala xclip no Linux
    if sistema == "Linux":
        print("\n📦 Instalando xclip...")
        run_cmd("sudo apt-get install -y xclip 2>/dev/null || echo 'xclip já instalado'")
        print("✅ xclip configurado")
    
    print("\n✅ INSTALAÇÃO CONCLUÍDA!")
    print("\n▶️  Execute: python3 app.py")

if __name__ == "__main__":
    main()
