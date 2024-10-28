import speech_recognition as sr
from pydub import AudioSegment

def transcreva_audio(ogg_file, wav_file, language="pt-BR"):
    """
    Transcreve um arquivo de áudio de OGG para texto usando o Google Speech Recognition.

    Parâmetros:
    ogg_file (str): Caminho para o arquivo OGG de entrada.
    wav_file (str): Caminho para o arquivo WAV de saída.
    language (str): Código de idioma para transcrição (o padrão é Português Brasileiro).

    Retorna:
    str: Texto transcrito ou uma mensagem de erro.
    """

    # Converte OGG para WAV
    audio = AudioSegment.from_file(ogg_file, format="ogg")
    audio.export(wav_file, format="wav")

    # Inicializa o reconhecedor
    recognizer = sr.Recognizer()

    # Carrega e transcreve o arquivo WAV
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        try:
            # Transcreve o arquivo de áudio
            text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return "Não foi possível entender o áudio"
        except sr.RequestError as e:
            return f"Não foi possível solicitar resultados; verifique sua conexão com a internet: {e}"


if __name__ == "__main__":
    # Exemplo de uso
    ogg_file = "Hackathon.ogg"
    wav_file = "converted.wav"
    transcribed_text = transcreva_audio(ogg_file, wav_file)
    print("Texto Transcrito:", transcribed_text)
