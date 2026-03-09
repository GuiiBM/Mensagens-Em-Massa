from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import re
import os
import urllib.parse
from PIL import Image
import io
import pyautogui
import subprocess

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

def is_valid_phone(num_str):
    """Valida se é um número de telefone válido"""
    # Remove caracteres não numéricos
    clean = ''.join(filter(str.isdigit, num_str))
    
    # Tamanho inválido
    if len(clean) < 10 or len(clean) > 15:
        return False
    
    # Ignora datas (padrões comuns)
    # 01062025, 01/06/2025, 2025, etc
    if len(clean) == 8 and (clean.startswith('0') or clean.startswith('1') or clean.startswith('2') or clean.startswith('3')):
        # Pode ser data formato ddmmyyyy
        day = int(clean[:2])
        month = int(clean[2:4])
        if 1 <= day <= 31 and 1 <= month <= 12:
            return False
    
    # Ignora anos (2020-2099)
    if len(clean) == 4 and clean.startswith('20'):
        return False
    
    # Ignora CEP brasileiro (8 dígitos, padrão xxxxx-xxx)
    if len(clean) == 8 and '-' in num_str:
        return False
    
    # Número brasileiro: deve ter 10 ou 11 dígitos
    if len(clean) == 10 or len(clean) == 11:
        # DDD válido (11-99)
        ddd = int(clean[:2])
        if 11 <= ddd <= 99:
            # Se tem 11 dígitos, terceiro deve ser 9 (celular)
            if len(clean) == 11 and clean[2] != '9':
                return False
            return True
    
    # Número internacional: 12-15 dígitos
    if 12 <= len(clean) <= 15:
        return True
    
    return False

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
        ignored_count = 0
        
        # Varre TODAS as células
        for row_idx in range(total_rows):
            for col_idx in range(total_cols):
                try:
                    cell_value = df.iloc[row_idx, col_idx]
                    
                    # Pula células vazias
                    if pd.isna(cell_value) or str(cell_value).strip() == '':
                        continue
                    
                    num_str = str(cell_value).strip()
                    
                    # Valida se é telefone válido
                    if not is_valid_phone(num_str):
                        ignored_count += 1
                        continue
                    
                    # Limpa o número
                    num_clean = num_str
                    for char in [' ', '-', '(', ')', '+', '.', ',', '/', '\\']:
                        num_clean = num_clean.replace(char, '')
                    
                    # Verifica se tem apenas dígitos
                    if not num_clean.isdigit():
                        ignored_count += 1
                        continue
                    
                    formatted = format_phone(num_clean)
                    
                    # Evita duplicatas
                    if formatted not in seen_numbers:
                        seen_numbers.add(formatted)
                        numbers.append(formatted)
                        print(f"✅ [Linha {row_idx+1}, Coluna {col_idx+1}] '{num_str}' → +{formatted}")
                    
                except Exception as e:
                    continue
        
        print("="*60)
        print(f"📊 Valores ignorados (datas/CEP/inválidos): {ignored_count}")
        print(f"✅ Números válidos encontrados: {len(numbers)}\n")
        
        if len(numbers) == 0:
            print("⚠️  NENHUM número válido encontrado!")
            print("Verifique se o arquivo contém telefones válidos\n")
        
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
    print("[3] Enviar imagem (pasta imagens/)")
    print("[4] Enviar imagem + texto digitado")
    print("[5] Enviar imagem + texto salvo")
    escolha = input("\nEscolha: ").strip()
    
    if escolha == '2':
        if not os.path.exists('mensagens'):
            os.makedirs('mensagens')
            print("❌ Pasta 'mensagens/' vazia")
            return None, None
        
        files = [f for f in os.listdir('mensagens') if f.endswith('.txt')]
        
        if not files:
            print("❌ Nenhum arquivo .txt encontrado")
            return None, None
        
        print("\n📄 Mensagens disponíveis:")
        for i, f in enumerate(files, 1):
            print(f"[{i}] {f}")
        
        try:
            idx = int(input("\nEscolha: ").strip()) - 1
            if idx < 0 or idx >= len(files):
                print("❌ Opção inválida")
                return None, None
            file_path = os.path.join('mensagens', files[idx])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                message = f.read().strip()
            
            if not message:
                print("❌ Arquivo vazio")
                return None, None
            
            print("\n📋 Mensagem carregada:")
            print("-" * 40)
            print(message)
            print("-" * 40)
            return message, None
        except ValueError:
            print("❌ Entrada inválida")
            return None, None
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
            return None, None
    
    elif escolha in ['3', '4', '5']:
        if not os.path.exists('imagens'):
            os.makedirs('imagens')
            print("❌ Pasta 'imagens/' vazia")
            return None, None
        
        files = [f for f in os.listdir('imagens') if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        if not files:
            print("❌ Nenhuma imagem encontrada")
            return None, None
        
        print("\n🖼️ Imagens disponíveis:")
        for i, f in enumerate(files, 1):
            print(f"[{i}] {f}")
        
        try:
            idx = int(input("\nEscolha: ").strip()) - 1
            if idx < 0 or idx >= len(files):
                print("❌ Opção inválida")
                return None, None
            image_path = os.path.join('imagens', files[idx])
            
            # Opção 3: Só imagem
            if escolha == '3':
                return "", image_path
            
            # Opção 4: Imagem + texto digitado
            elif escolha == '4':
                msg = input("\n💬 Digite a legenda da imagem: ").strip()
                return msg if msg else "", image_path
            
            # Opção 5: Imagem + texto salvo
            else:
                if not os.path.exists('mensagens'):
                    os.makedirs('mensagens')
                    print("❌ Pasta 'mensagens/' vazia")
                    return None, None
                
                msg_files = [f for f in os.listdir('mensagens') if f.endswith('.txt')]
                
                if not msg_files:
                    print("❌ Nenhum arquivo .txt encontrado")
                    return None, None
                
                print("\n📄 Mensagens disponíveis:")
                for i, f in enumerate(msg_files, 1):
                    print(f"[{i}] {f}")
                
                msg_idx = int(input("\nEscolha: ").strip()) - 1
                if msg_idx < 0 or msg_idx >= len(msg_files):
                    print("❌ Opção inválida")
                    return None, None
                
                msg_path = os.path.join('mensagens', msg_files[msg_idx])
                with open(msg_path, 'r', encoding='utf-8') as f:
                    message = f.read().strip()
                
                print("\n📋 Legenda carregada:")
                print("-" * 40)
                print(message)
                print("-" * 40)
                
                return message if message else "", image_path
                
        except ValueError:
            print("❌ Entrada inválida")
            return None, None
    
    else:
        msg = input("\n💬 Digite a mensagem: ").strip()
        if not msg:
            print("❌ Mensagem vazia")
            return None, None
        return msg, None

def send_whatsapp_messages(numbers, message, image_path=None):
    """Envia mensagens via WhatsApp Web usando Selenium"""
    
    # Se tem imagem, converte para PNG ANTES de abrir navegador
    png_path = None
    if image_path:
        try:
            from PIL import Image
            abs_path = os.path.abspath(image_path)
            
            # Converte para PNG se necessário
            if not abs_path.lower().endswith('.png'):
                img = Image.open(abs_path)
                png_path = abs_path.rsplit('.', 1)[0] + '_temp.png'
                img.save(png_path, 'PNG')
                print(f"✅ Imagem convertida para PNG")
            else:
                png_path = abs_path
        except Exception as e:
            print(f"❌ Erro ao converter imagem: {e}")
            return
    
    print("\n🌐 Abrindo WhatsApp Web...")
    print("⚠️  Escaneie o QR Code e aguarde carregar completamente!\n")
    
    # Configurar Chrome
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
            
            # Se tem imagem
            if png_path:
                url = f"https://web.whatsapp.com/send?phone={number}"
                driver.get(url)
                
                # AGUARDA PÁGINA CARREGAR COMPLETAMENTE
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                    )
                    time.sleep(3)
                except:
                    print("❌ Timeout")
                    continue
                
                try:
                    # Procura inputs file
                    inputs = driver.find_elements(By.XPATH, '//input[@type="file"]')
                    
                    if not inputs:
                        print("❌ Sem inputs")
                        continue
                    
                    # Procura o input que aceita VÍDEO (esse é o de IMAGEM, não figurinha)
                    target_input = None
                    for inp in inputs:
                        accept = inp.get_attribute('accept') or ''
                        if 'video' in accept.lower():
                            target_input = inp
                            break
                    
                    # Se não achou, usa o SEGUNDO input (geralmente figurinha é o primeiro)
                    if not target_input and len(inputs) > 1:
                        target_input = inputs[1]
                    
                    # Se ainda não achou, usa o primeiro
                    if not target_input:
                        target_input = inputs[0]
                    
                    target_input.send_keys(png_path)
                    time.sleep(6)
                    
                    # Clica no botão enviar
                    try:
                        send_btn = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
                        )
                        send_btn.click()
                    except:
                        try:
                            send_btn = driver.find_element(By.XPATH, '//div[@aria-label="Enviar"]')
                            send_btn.click()
                        except:
                            pyautogui.press('enter')
                    
                    time.sleep(4)
                    print("✅ (img) ", end='', flush=True)
                    
                    # Envia texto SEPARADO
                    if message:
                        time.sleep(2)
                        text = urllib.parse.quote(message)
                        driver.get(f"https://web.whatsapp.com/send?phone={number}&text={text}")
                        time.sleep(3)
                        
                        try:
                            send_text = WebDriverWait(driver, 8).until(
                                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Enviar"]'))
                            )
                            send_text.click()
                        except:
                            pyautogui.press('enter')
                        
                        print("✅ (txt)")
                        time.sleep(2)
                    else:
                        print()
                    
                except Exception as e:
                    print(f"❌ {str(e)[:80]}")
            
            # Se é só texto - fluxo rápido
            else:
                # Usa URL com texto pré-preenchido (mais rápido)
                text = urllib.parse.quote(message)
                url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
                driver.get(url)
                time.sleep(2)
                
                try:
                    # Procura botão de enviar
                    send_button = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Enviar"]'))
                    )
                    send_button.click()
                    print("✅")
                    time.sleep(1)
                except:
                    try:
                        # Alternativa: pressiona Enter
                        input_box = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                        )
                        input_box.send_keys(Keys.ENTER)
                        print("✅")
                        time.sleep(1)
                    except:
                        print("❌")
            
        except Exception as e:
            print(f"❌ Erro geral: {str(e)[:50]}")
    
    # Remove arquivo temporário se foi criado
    if png_path and '_temp.png' in png_path:
        try:
            os.remove(png_path)
        except:
            pass
    
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
    message, image_path = get_message()
    if message is None and image_path is None:
        print("❌ Mensagem/imagem vazia")
        return
    
    # Envia mensagens
    send_whatsapp_messages(numbers, message, image_path)

if __name__ == "__main__":
    main()
