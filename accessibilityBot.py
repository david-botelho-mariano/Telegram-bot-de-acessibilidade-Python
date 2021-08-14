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

			#audio
			try:
				print(update.message)

				id_arquivo = regex_string(str(update.message), "'file_id': '", "',")
				voz_transcrita = baixar_audio(id_arquivo)
				voz_transcrita = voz_transcrita.lower()
				print(voz_transcrita)

				update.message.reply_text("transcricao do audio: " + voz_transcrita)

			except Exception as error:
				print(error)

			#imagem
			try:
				print(update.message)

				id_arquivo = update.message["photo"][2]["file_id"]
				baixar_foto(id_arquivo)

			except Exception as error:
				print(error)


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

	try:
		text_from_audio = r.recognize_google(audio, language='pt-BR')
		print("[+]transcricao concluida")
		return text_from_audio
	except Exception as error:
		print("[+]falha na transcricao")
		return str(error)

def baixar_foto(id_arquivo):
	requisicao_1 = requests.get('https://api.telegram.org/bot' + bot_token + '/getFile?file_id=' + id_arquivo)
	caminho_arquivo = regex_string(requisicao_1.text, '"file_path":"', '"')	

	requisicao_2 = requests.get('https://api.telegram.org/file/bot' + bot_token + '/' + caminho_arquivo)
	print('imagem em: ', requisicao_2.url)

if __name__ == '__main__':
	thread_bot_telegram()