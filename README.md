# Bot que envia código de verificação de contas de streaming do seu email para grupo no Telegram

Este é um bot para Telegram que busca códigos de verificação de serviços de streaming (Disney+ e Amazon Prime) diretamente do seu e-mail e os envia para um grupo ou chat específico. Ele utiliza Python com as bibliotecas `imaplib`, `email`, `re` e `telegram.ext`.

## Pré-requisitos

1. **Configuração do E-mail**: Use um e-mail Gmail com uma senha de aplicativo (necessária para autenticação IMAP).
2. **Token do Bot**: Crie um bot no Telegram via BotFather e obtenha o `TOKEN_BOT`.
3. **Chat ID**: Identifique o `CHAT_ID` do grupo ou chat onde o bot enviará os códigos.

## Configuração

Edite as variáveis no início do código para configurar corretamente seu bot.

## Instalação

Instale as dependências necessárias executando:

```sh
pip install python-telegram-bot
```

## Como Usar

1. **Inicie o Bot**: Execute o script com o seguinte comando:

   ```sh
   python botqueenviacodigo.py
   ```
   
   Ou utilize um arquivo `.bat` para facilitar a execução (veja abaixo).

2. **No Telegram**: Envie o comando `/codigo` ao bot.

## Hospedando o Bot no Seu PC (Windows)

Para facilitar a execução no Windows, utilize um arquivo `.bat`:

1. Certifique-se de que o Python está instalado (recomendado: versão 3.10).
2. Coloque o arquivo `hospedar_bot_no_seu_pc.bat` no mesmo diretório que `botqueenviacodigo.py`.
3. Dê um duplo clique em `executar_bot.bat` para iniciar o bot.
4. Se o Python não estiver no `PATH`, edite o `.bat` e ajuste o caminho para o executável do Python. Exemplo:

```bat
@echo off
cd /d "C:\caminho\para\seu\bot"
C:\Python39\python.exe botqueenviacodigo.py
pause
```

O bot continuará rodando até que você feche a janela.

## Funcionamento

1. O bot acessa a caixa de entrada do Gmail via IMAP.
2. Procura e-mails específicos dos remetentes configurados:
   - **Disney+**: `disneyplus@trx.mail2.disneyplus.com`
   - **Amazon Prime**: `account-update@amazon.com`
3. Extrai códigos de 6 dígitos usando expressões regulares.
4. Envia o código ao Telegram automaticamente.

### Observações Importantes

- Certifique-se de que o **IMAP** está habilitado no Gmail e que a pasta "Todos os e-mails" está acessível.
- O bot prioriza o e-mail **mais recente** de cada serviço.
- Em caso de erro, o bot exibirá a mensagem de erro e o conteúdo do e-mail (limitado a 4000 caracteres).
