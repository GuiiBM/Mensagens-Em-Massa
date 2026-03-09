import pywhatkit
import datetime

# 1. Coleta os dados básicos
phone_number = input("Digite o número (ex: +5511999999999): ")
message = input("Digite a mensagem: ")

print("\n--- Opções de Agendamento ---")
print("[Enter] Enviar agora (daqui a 2 minutos)")
print("[1] Escolher horário específico")
opcao = input("Escolha uma opção: ")

# 2. Define o horário baseado na escolha
now = datetime.datetime.now()

if opcao == '1':
    # Usuário escolhe a hora
    hours = int(input("Digite a hora (0-23): "))
    minutes = int(input("Digite os minutos (0-59): "))
else:
    # Envio "imediato" (agendado para 2 minutos à frente)
    # Somamos 2 minutos para garantir que o script não dê erro de tempo insuficiente
    scheduled_time = now + datetime.timedelta(minutes=2)
    hours = scheduled_time.hour
    minutes = scheduled_time.minute

# 3. Executa o agendamento
print(f"\nAgendando para às {hours:02d}:{minutes:02d}...")
try:
    # send_time_none=True ajuda em algumas versões, mas o padrão é o horário
    pywhatkit.sendwhatmsg(phone_number, message, hours, minutes)
    print("Sucesso! Mantenha o navegador aberto e o WhatsApp Web logado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")