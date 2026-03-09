import pywhatkit
import datetime
import re
import os

def format_phone(number):
    """Formata número - detecta brasileiro automaticamente"""
    clean = re.sub(r'\D', '', number)
    
    # Se já tem +, mantém
    if number.strip().startswith('+'):
        return '+' + clean
    
    # Detecta número brasileiro: 11 dígitos (DDD + 9 dígitos)
    if len(clean) == 11 and clean[2] == '9':
        return f'+55{clean}'
    
    # Número brasileiro antigo: 10 dígitos
    if len(clean) == 10:
        return f'+55{clean}'
    
    # Se já começa com 55 e tem 13 dígitos (55 + 11)
    if clean.startswith('55') and len(clean) == 13:
        return f'+{clean}'
    
    # Outros casos: adiciona + se não tiver
    return f'+{clean}' if not number.startswith('+') else number

def read_contacts(file_path):
    """Lê números de arquivo Excel/CSV"""
    try:
        import pandas as pd
        
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        numbers = []
        
        # Procura coluna com números
        for col in df.columns:
            col_lower = str(col).lower()
            if any(term in col_lower for term in ['numero', 'telefone', 'phone', 'contato', 'number', 'celular']):
                for val in df[col]:
                    if pd.notna(val):
                        num_str = str(val).strip()
                        if '.' in num_str:
                            num_str = num_str.split('.')[0]
                        if num_str and num_str != 'nan':
                            numbers.append(format_phone(num_str))
                return numbers
        
        # Se não achar, usa primeira coluna
        col = df.columns[0]
        for val in df[col]:
            if pd.notna(val):
                num_str = str(val).strip()
                if '.' in num_str:
                    num_str = num_str.split('.')[0]
                if num_str and num_str != 'nan':
                    numbers.append(format_phone(num_str))
        
        return numbers
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return []

def main():
    print("🤖 WhatsApp Sender - Envio em Massa")
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
        
        escolha = int(input("\nEscolha: ")) - 1
        file_path = os.path.join('contatos', files[escolha])
        
        numbers = read_contacts(file_path)
        print(f"\n✅ {len(numbers)} números carregados:")
        for n in numbers:
            print(f"  • {n}")
    else:
        phone_input = input("\n📱 Número: ")
        numbers = [format_phone(phone_input)]
        print(f"✅ {numbers[0]}")
    
    if not numbers:
        print("❌ Nenhum número")
        return
    
    # Coleta mensagem
    message = input("\n💬 Mensagem: ")
    
    # Agendamento
    print("\n--- Opções de Agendamento ---")
    print("[Enter] Enviar agora (daqui a 2 minutos)")
    print("[1] Escolher horário específico")
    opcao = input("Escolha: ")
    
    now = datetime.datetime.now()
    
    if opcao == '1':
        hours = int(input("Hora (0-23): "))
        minutes = int(input("Minutos (0-59): "))
    else:
        scheduled_time = now + datetime.timedelta(minutes=2)
        hours = scheduled_time.hour
        minutes = scheduled_time.minute
    
    # Envia para cada número
    print(f"\n🚀 Iniciando envios às {hours:02d}:{minutes:02d}")
    print("⚠️ Mantenha o navegador aberto!\n")
    
    for i, number in enumerate(numbers, 1):
        print(f"[{i}/{len(numbers)}] {number}... ", end='', flush=True)
        try:
            pywhatkit.sendwhatmsg(number, message, hours, minutes)
            print("✅")
            
            # Próximo envio: 2 min depois
            if i < len(numbers):
                scheduled_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
                hours = scheduled_time.hour
                minutes = scheduled_time.minute
        except Exception as e:
            print(f"❌ {e}")
    
    print("\n✅ Processo concluído!")

if __name__ == "__main__":
    main()
