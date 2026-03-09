# Mensagens Em Massa - WhatsApp

Sistema para envio de mensagens em massa via WhatsApp com suporte a números internacionais e leitura de arquivos.

## Instalação Automática

Execute o instalador:
```bash
python3 install.py
```

O instalador irá:
- Detectar seu sistema operacional
- Instalar todas as dependências automaticamente
- Criar a pasta `contatos/` para seus arquivos

## Instalação Manual

```bash
pip install -r requirements.txt
```

## Como usar

Execute:
```bash
python3 app.py
```

### Envio de mensagens:

**[1] Digitar manualmente** - Digite um número com código do país

**[2] Ler de arquivo** - Carrega números de Excel/CSV
- Coloque arquivos `.xlsx`, `.xls` ou `.csv` na pasta `contatos/`
- O sistema detecta automaticamente a coluna com números
- Envia para todos os números do arquivo individualmente

### Agendamento:

- **[Enter]** Enviar agora (daqui a 2 minutos)
- **[1]** Escolher horário específico

## Formato dos arquivos

**CSV:**
```csv
numero
5512999999999
5511988888888
351912345678
```

**Excel:**
| numero | nome |
|--------|------|
| 5512999999999 | João |
| 351912345678 | Maria |

## Funcionalidades

- ✅ Suporte a números internacionais (qualquer país)
- ✅ Formatação automática com código do país
- ✅ Leitura de Excel/CSV
- ✅ Envio em massa individual (2 min entre cada)
- ✅ Agendamento flexível
- ✅ Detecção automática de coluna com números

## Estrutura

```
Mensagens-Em-Massa/
├── install.py         # Instalador automático
├── app.py            # Aplicação principal
├── requirements.txt  # Dependências
├── contatos/         # Seus arquivos Excel/CSV
│   └── exemplo.csv
└── README.md
```

## Observações

- Mantenha o WhatsApp Web logado no navegador
- Não feche o terminal durante o envio
- Para números brasileiros: `5512999999999`
- Para números internacionais: `351912345678` (Portugal), `1234567890` (EUA), etc.
