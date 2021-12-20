# Ferramenta de acessibilidade para aplicativo de mensagens

Bot para o aplicativo Telegram que transcreve áudios e que converte a interpretação de imagens em texto dentro de uma conversa, com o intuito de aumentar a acessibilidade de pessoas com deficiência auditiva ou visual.

A estrutura do programa foi feita por meio da linguagem de programação Python, o reconhecimento de imagens deu-se por meio da API da empresa IBM denominada de Watson Visual Recognition, para a transcrição de voz foi escolhido a API Google Voice Recognition da empresa Google, os comandos de voz e as imagens foram capturadas por meio de um bot do aplicativo de mensagens Telegram

# Bibliotecas necessarias do Python

- speech_recognition 
- pydub 
- python-telegram-bot
- requests

# Tutorial 

1) No terminal de comando (CMD), digite: `python acessibilidadeBot.py`

2) Envie um audio para testar o bot atraves do link: https://t.me/unitins_telegram_bot

# Execução do bot de reconhecimento de imagem.

![image](https://user-images.githubusercontent.com/48680041/141605508-5b7a7023-ece1-4e3b-b899-51992f643cab.png)

# Bot de transcrição de voz em funcionamento.

![image](https://user-images.githubusercontent.com/48680041/141605544-29c6cb62-bbb0-47dd-9d70-43352077fb22.png)
