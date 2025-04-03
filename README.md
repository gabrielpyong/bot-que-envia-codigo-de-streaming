#Bot que envia código de verificação de contas de streaming do seu email para grupo no telegram

Este é um bot para Telegram que busca códigos de verificação de serviços de streaming (Disney+ e Amazon Prime) diretamente do seu e-mail e os envia para um grupo ou chat específico. Ele utiliza Python com as bibliotecas imaplib, email, re e telegram.ext.


#Pré-requisitos
Configuração do E-mail: Use um e-mail Gmail com uma senha de aplicativo (necessária para autenticação IMAP).

Token do Bot: Crie um bot no Telegram via BotFather e obtenha o TOKEN_BOT.

Chat ID: Identifique o CHAT_ID do grupo ou chat onde o bot enviará os códigos.

Configuração
Edite as variáveis no início do código:
https://prnt.sc/yqoBd3BqRBk1

---------

#Instale as dependências:
pip install python-telegram-bot

##Como Usar
Inicie o Bot: Execute o script com python botqueenviacodigo.py ou use o arquivo .bat (veja abaixo).

No Telegram, envie o comando /codigo ao bot.

##Hospedando o Bot no Seu PC (Windows)
Para facilitar a execução no Windows, use o arquivo hospedar_bot_no_seu_pc:
Certifique-se de que o Python está instalado (recomendado: versão 3.10).

Coloque o arquivo hospedar_bot_no_seu_pc no mesmo diretório que botqueenviacodigo.py.

Dê um duplo clique em executar_bot.bat para iniciar o bot.

Se o Python não estiver no PATH, edite o .bat e ajuste o caminho para o executável do Python (ex.: C:\Python39\python.exe).

Exemplo de edição no .bat:
bat
---
@echo off
cd /d "C:\caminho\para\seu\bot"
C:\Python39\python.exe botqueenviacodigo.py
pause
---

O bot continuará rodando até que você feche a janela


Funcionamento
O bot acessa a caixa de entrada do Gmail via IMAP.

Procura e-mails específicos dos remetentes configurados (disneyplus@trx.mail2.disneyplus.com para Disney+ e account-update@amazon.com para Prime).

Extrai códigos de 6 dígitos usando expressões regulares e envia ao Telegram.

OBS:

- Certifique-se de que o IMAP está habilitado no Gmail e que a pasta "Todos os e-mails" está acessível.

- O bot prioriza o e-mail mais recente de cada serviço.

- Em caso de erro, ele exibe a mensagem de erro e o conteúdo do e-mail (limitado a 4000 caracteres).





