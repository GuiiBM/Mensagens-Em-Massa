# Mensagens Em Massa - WhatsApp

Sistema para envio de mensagens em massa via WhatsApp Web usando Selenium (rápido e confiável).

## Instalação Automática

Execute o instalador:
```bash
python3 install.py
```

O instalador irá:
- Detectar seu sistema operacional
- Instalar todas as dependências (Selenium, pandas, openpyxl)
- Criar as pastas `contatos/`, `mensagens/` e `imagens/`

## Instalação Manual

```bash
pip install -r requirements.txt
```

## Como usar

Execute:
```bash
python3 app.py
```

### Fluxo:

1. **Escolha origem dos números:**
   - [1] Digitar manualmente
   - [2] Ler de arquivo Excel/CSV

2. **Escolha a mensagem:**
   - [1] Digitar agora
   - [2] Usar mensagem salva (.txt)
   - [3] Enviar imagem
   - [4] Enviar imagem + texto (legenda)

3. **Escaneie QR Code** e pressione ENTER

4. **Envio automático** - Rápido e sequencial!

## Formato dos arquivos

### Contatos (CSV):
```csv
numero
5512999999999
5511988888888
351912345678
```

### Contatos (Excel):
| numero | nome |
|--------|------|
| 5512999999999 | João |
| 351912345678 | Maria |

### Mensagens (.txt):
```
Olá! 👋

Tudo bem?

Mensagem com *formatação* mantida.

Atenciosamente,
Equipe
```

### Imagens:
Coloque arquivos `.jpg`, `.png`, `.gif` ou `.webp` na pasta `imagens/`

## Funcionalidades

- ✅ **Envio RÁPIDO** - ~5 segundos por mensagem
- ✅ Suporte a números internacionais
- ✅ Formatação automática de números brasileiros
- ✅ Leitura de Excel/CSV
- ✅ Mensagens salvas em .txt
- ✅ **Envio de imagens**
- ✅ **Imagens com legenda**
- ✅ Mantém formatação (negrito, itálico, emojis)
- ✅ Uma única aba do navegador
- ✅ Filtra datas e CEPs automaticamente
- ✅ Confiável e estável

## Estrutura

```
Mensagens-Em-Massa/
├── install.py         # Instalador automático
├── app.py            # Aplicação principal
├── requirements.txt  # Dependências
├── contatos/         # Seus arquivos Excel/CSV
│   └── exemplo.csv
├── mensagens/        # Suas mensagens .txt
│   └── exemplo.txt
├── imagens/          # Suas imagens
│   └── .gitkeep
└── README.md
```

## Vantagens desta solução

- 🚀 **Rápido**: ~5 segundos por mensagem (não 2 minutos!)
- 🎯 **Confiável**: Usa Selenium (controle direto do navegador)
- 🔄 **Uma aba**: Não abre 500 abas
- ✅ **Funciona**: Sem bugs de agendamento
- 🖼️ **Imagens**: Envia fotos com ou sem legenda
- 🛡️ **Filtros**: Ignora datas e CEPs automaticamente

## Observações

- Mantenha o WhatsApp Web logado
- Escaneie o QR Code quando solicitado
- Não feche o navegador durante o envio
- Para números brasileiros: `12999999999` ou `11988888888`
- Para números internacionais: `351912345678`, `1234567890`, etc.
- Imagens suportadas: JPG, PNG, GIF, WEBP

## Exemplo de uso

10 mensagens = ~50 segundos (não 20 minutos!)
