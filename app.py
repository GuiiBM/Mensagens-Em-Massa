from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import os
import urllib.parse

def format_phone(number):
    """Formata número - detecta brasileiro automaticamente"""
    clean = re.sub(r'\D', '', number)
    
    if number.strip().startswith('+'):
        return clean
    
    if len(clean) == 11 and clean[2] == '9':
        return f'55{clean}'
    
    if len(clean) == 10:
        return f'55{clean}'
    
    if clean.startswith('55') and len(clean) == 13:
        return clean
    
    return clean

def read_contacts(file_path):
    """Lê números de arquivo Excel/CSV - TODAS as células"""
    try:
        import pandas as pd
        
        # Lê arquivo SEM interpretar nada como NA
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False, na_filter=False, header=None)
        else:
            # Para Excel, lê TODAS as sheets SEM cabeçalho
            excel_file = pd.ExcelFile(file_path)
            all_dfs = []
            for sheet_name in excel_file.sheet_names:
                df_sheet = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, keep_default_na=False, na_filter=False, header=None)
                all_dfs.append(df_sheet)
            df = pd.concat(all_dfs, ignore_index=True)
        
        total_rows = len(df)
        total_cols = len(df.columns)
        total_cells = total_rows * total_cols
        
        print(f"\n📊 Arquivo: {file_path}")
        print(f"📊 Linhas: {total_rows} | Colunas: {total_cols} | Total células: {total_cells}")
        print("\n" + "="*60)
        
        numbers = []
        seen_numbers = set()
        cells_checked = 0
        
        # Varre TODAS as células - linha por linha, coluna por coluna
        for row_idx in range(total_rows):
            for col_idx in range(total_cols):
                cells_checked += 1
                try:
                    cell_value = df.iloc[row_idx, col_idx]
                    
                    # Pula células vazias
                    if pd.isna(cell_value) or str(cell_value).strip() == '':
                        continue
                    
                    # Converte para string e limpa
                    num_str = str(cell_value).strip()
                    num_clean = num_str
                    
                    # Remove todos os caracteres não numéricos
                    for char in [' ', '-', '(', ')', '+', '.', ',', '/', '\\']:
                        num_clean = num_clean.replace(char, '')
                    
                    # Verifica se é número válido (mínimo 8 dígitos)
                    if num_clean.isdigit() and len(num_clean) >= 8:
                        formatted = format_phone(num_clean)
                        
                        # Evita duplicatas
                        if formatted not in seen_numbers:
                            seen_numbers.add(formatted)
                            numbers.append(formatted)
                            print(f"✅ [Linha {row_idx+1}, Coluna {col_idx+1}] '{num_str}' → +{formatted}")
                        
                except Exception as e:
                    continue
        
        print("="*60)
        print(f"\n📊 Células verificadas: {cells_checked}/{total_cells}")
        print(f"✅ Números únicos encontrados: {len(numbers)}\n")
        
        if len(numbers) == 0:
            print("⚠️  NENHUM número encontrado!")
            print("Verifique se o arquivo contém números válidos (mínimo 8 dígitos)\n")
        
        return numbers
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_message():
    """Obtém mensagem (digitada ou de arquivo)"""
    print("\n💬 MENSAGEM:")
    print("[1] Digitar agora")
    print("[2] Usar mensagem salva (pasta mensagens/)")
    escolha = input("\nEscolha: ").strip()
    
    if escolha == '2':
        if not os.path.exists('mensagens'):
            os.makedirs('mensagens')
            print("❌ Pasta 'mensagens/' vazia")
            return None
        
        files = [f for f in os.listdir('mensagens') if f.endswith('.txt')]
        
        if not files:
            print("❌ Nenhum arquivo .txt encontrado")
            return None
        
        print("\n📄 Mensagens disponíveis:")
        for i, f in enumerate(files, 1):
            print(f"[{i}] {f}")
        
        try:
            idx = int(input("\nEscolha: ").strip()) - 1
            if idx < 0 or idx >= len(files):
                print("❌ Opção inválida")
                return None
            file_path = os.path.join('mensagens', files[idx])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                message = f.read().strip()
            
            if not message:
                print("❌ Arquivo vazio")
                return None
            
            print("\n📋 Mensagem carregada:")
            print("-" * 40)
            print(message)
            print("-" * 40)
            return message
        except ValueError:
            print("❌ Entrada inválida")
            return None
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
            return None
    else:
        msg = input("\n💬 Digite a mensagem: ").strip()
        if not msg:
            print("❌ Mensagem vazia")
            return None
        return msg

def send_whatsapp_messages(numbers, message):
    """Envia mensagens via WhatsApp Web usando Selenium"""
    
    print("\n🌐 Abrindo WhatsApp Web...")
    print("⚠️  Escaneie o QR Code e aguarde carregar completamente!\n")
    
    # Configurar Chrome com perfil persistente
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com")
    
    # Aguarda login manual
    print("📱 Aguardando login...")
    print("Pressione ENTER após escanear o QR Code e carregar seus chats")
    input()
    
    print("\n🚀 Iniciando envios...\n")
    
    for i, number in enumerate(numbers, 1):
        try:
            print(f"[{i}/{len(numbers)}] +{number}... ", end='', flush=True)
            
            # Monta URL do WhatsApp
            text = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
            
            driver.get(url)
            
            # Aguarda carregar a conversa (reduzido para 2s)
            time.sleep(2)
            
            # Tenta enviar
            try:
                # Procura botão de enviar
                send_button = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Enviar"]'))
                )
                send_button.click()
                print("✅")
                time.sleep(1)  # Reduzido para 1s
            except:
                # Alternativa: procura caixa de texto e pressiona Enter
                try:
                    input_box = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                    )
                    input_box.send_keys(Keys.ENTER)
                    print("✅")
                    time.sleep(1)  # Reduzido para 1s
                except:
                    print("❌ Não enviado")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n✅ Processo concluído!")
    print("Pressione ENTER para fechar o navegador...")
    input()
    driver.quit()

def main():
    print("🤖 WhatsApp Sender - Envio em Massa (Selenium)")
    print("=" * 50)
    
    # Coleta números
    print("\n📱 ORIGEM DOS NÚMEROS:")
    print("[1] Digitar manualmente")
    print("[2] Ler de arquivo (pasta contatos/)")
    origem = input("\nEscolha: ").strip()
    
    numbers = []
    
    if origem == '2':
        if not os.path.exists('contatos'):
            os.makedirs('contatos')
            print("❌ Pasta 'contatos/' vazia")
            return
        
        files = [f for f in os.listdir('contatos') if f.endswith(('.xlsx', '.xls', '.csv'))]
        
        if not files:
            print("❌ Nenhum arquivo encontrado")
            return
        
        print("\n📁 Arquivos:")
        for i, f in enumerate(files, 1):
            print(f"[{i}] {f}")
        
        try:
            escolha = int(input("\nEscolha: ").strip()) - 1
            if escolha < 0 or escolha >= len(files):
                print("❌ Opção inválida")
                return
            file_path = os.path.join('contatos', files[escolha])
            
            numbers = read_contacts(file_path)
            print(f"\n✅ {len(numbers)} números carregados")
        except ValueError:
            print("❌ Entrada inválida")
            return
    else:
        phone_input = input("\n📱 Número: ").strip()
        if not phone_input:
            print("❌ Número vazio")
            return
        numbers = [format_phone(phone_input)]
        print(f"✅ +{numbers[0]}")
    
    if not numbers:
        print("❌ Nenhum número")
        return
    
    # Coleta mensagem
    message = get_message()
    if not message:
        print("❌ Mensagem vazia")
        return
    
    # Envia mensagens
    send_whatsapp_messages(numbers, message)

if __name__ == "__main__":
    main()
