# -*- coding: utf-8 -*-

#bot do telegram
import telegram
from telegram.error import NetworkError, Unauthorized
import requests
import speech_recognition as sr
from pydub import AudioSegment

update_id = None
#bot do telegram


def regex_string(variavel, inicio, fim):
	frase_array_primario = variavel.split(inicio)
	frase_array_secundario = frase_array_primario[1].split(fim)
	resultado = frase_array_secundario[0]
	return resultado

def thread_bot_telegram():
	global update_id
	global bot
	global bot_token

	bot_token = '1157046249:AAFVRRiwPd8R-ckdFox1Ck626qyiCFNo6uQ'
	bot = telegram.Bot(bot_token)

	try:
		update_id = bot.get_updates()[0].update_id
	except IndexError:
		update_id = None

	while True:
		try:
			echo(bot)
		except Unauthorized:
			update_id += 1
		except Exception as error:
			print(error)

def echo(bot):
	global update_id

	for update in bot.get_updates(offset=update_id, timeout=10):
		update_id = update.update_id + 1

		if update.message:

			print(update.message)

			#audio
			if ", 'voice': {'" in str(update.message):
				#print(update.message)

				id_arquivo = regex_string(str(update.message), "'file_id': '", "',")
				voz_transcrita = baixar_audio(id_arquivo)
				voz_transcrita = voz_transcrita.lower()
				print(voz_transcrita)

				update.message.reply_text("transcricao do audio: " + voz_transcrita)

			#imagem
			elif "}, 'photo': [{'" in str(update.message):
				#print(update.message)

				id_arquivo = update.message["photo"][2]["file_id"]
				predicao = baixar_foto(id_arquivo)

				update.message.reply_text("interpretacao da imagem: " + predicao)



def baixar_audio(id_arquivo):
	requisicao_1 = requests.get('https://api.telegram.org/bot' + bot_token + '/getFile?file_id=' + id_arquivo)
	caminho_arquivo = regex_string(requisicao_1.text, '"file_path":"', '"')

	requisicao_2 = requests.get('https://api.telegram.org/file/bot' + bot_token + '/' + caminho_arquivo)
	open('audio-capturado.oga', 'wb').write(requisicao_2.content)

	print("[+]download do audio concluido")
	return reconhecer_voz('audio-capturado.oga')


def reconhecer_voz(audio_baixado_path):
	sound = AudioSegment.from_file(audio_baixado_path)
	sound.export("audio-convertido.wav", format="wav")
	print("[+]audio convertido")

	r = sr.Recognizer()
	with sr.AudioFile('audio-convertido.wav') as source:
		audio = r.record(source)

	text_from_audio = r.recognize_google(audio, language='pt-BR')
	return text_from_audio

def baixar_foto(id_arquivo):
	requisicao_1 = requests.get('https://api.telegram.org/bot' + bot_token + '/getFile?file_id=' + id_arquivo)
	caminho_arquivo = regex_string(requisicao_1.text, '"file_path":"', '"')
	full_caminho_arquivo = 'https://api.telegram.org/file/bot' + bot_token + '/' + caminho_arquivo

	headers = {'Accept-Language': 'pt-br'}
	requisicao_2 = requests.get('https://api.us-south.visual-recognition.watson.cloud.ibm.com/v3/classify?url=' + full_caminho_arquivo + '&version=2018-03-19', auth=('apikey', 'rdpaPko36Igl96h-4PAIrChcnF5zZnZi7-mA8vR9kftY'), headers=headers)
	requisicao_2_json = requisicao_2.json()

	output = ""

	for x in range(len(requisicao_2_json['images'][0]['classifiers'][0]['classes'])):

		classe = requisicao_2_json['images'][0]['classifiers'][0]['classes'][x]['class']
		precisao = requisicao_2_json['images'][0]['classifiers'][0]['classes'][x]['score']
		output += classe + ' (precisao de ' + str(precisao * 100) + '%), '


	print(output)
	return str(output.encode('utf-8'))


if __name__ == '__main__':
	thread_bot_telegram()