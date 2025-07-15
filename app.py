from flask import Flask, request
import telegram
import os
import logging
from swap_face import process_video
from deepfake_fomm import process_deepfake
from bot_config import TELEGRAM_TOKEN

app = Flask(__name__)
bot = telegram.Bot(token=TELEGRAM_TOKEN)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_sessions = {}

@app.route('/', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id

    try:
        msg_text = update.message.text if update.message.text else ""

        if msg_text.lower() == "/deepfake":
            user_sessions[chat_id] = {'mode': 'deepfake'}
            bot.send_message(chat_id, "🧠 Modo DeepFake ativado. Envie uma imagem (rosto) e depois um vídeo (movimento).")
            return 'ok'

        mode = user_sessions.get(chat_id, {}).get("mode", "")

        # Imagem (rosto) recebida para deepfake
        if update.message.photo and mode == "deepfake":
            photo = update.message.photo[-1].get_file()
            face_path = f'static/deep_source_{chat_id}.jpg'
            photo.download(face_path)
            user_sessions[chat_id]['source_image'] = face_path
            bot.send_message(chat_id, "✅ Rosto recebido. Agora envie o vídeo de referência.")
            return 'ok'

        # Vídeo (driving) recebido para deepfake
        elif update.message.video and mode == "deepfake":
            if 'source_image' not in user_sessions[chat_id]:
                bot.send_message(chat_id, "⚠️ Envie primeiro uma imagem de rosto.")
                return 'ok'

            video = update.message.video.get_file()
            driving_path = f'static/deep_drive_{chat_id}.mp4'
            output_path = f'static/deep_output_{chat_id}.mp4'
            video.download(driving_path)
            bot.send_message(chat_id, "🧪 Gerando DeepFake, aguarde...")

            try:
                process_deepfake(user_sessions[chat_id]['source_image'], driving_path, output_path)
                bot.send_video(chat_id, open(output_path, 'rb'), caption="✅ Aqui está o seu deepfake!")
            except Exception as e:
                logger.exception("Erro ao gerar deepfake")
                bot.send_message(chat_id, f"❌ Falha ao gerar o deepfake: {e}")
            return 'ok'

        # Vídeo recebido (FaceFusion)
        if update.message.video:
            video = update.message.video.get_file()
            file_path = f'static/input_{chat_id}.mp4'
            video.download(file_path)
            user_sessions[chat_id] = {'video': file_path}
            bot.send_message(chat_id, "🎥 Vídeo recebido com sucesso. Agora envie uma imagem com o rosto desejado.")
            logger.info(f"✅ Vídeo recebido de {chat_id} e salvo em {file_path}")

        # Imagem recebida (FaceFusion)
        elif update.message.photo:
            if chat_id not in user_sessions or 'video' not in user_sessions[chat_id]:
                bot.send_message(chat_id, "⚠️ Por favor, envie primeiro o vídeo antes da imagem.")
                return 'ok'

            photo = update.message.photo[-1].get_file()
            photo_path = f'static/face_{chat_id}.jpg'
            photo.download(photo_path)
            logger.info(f"✅ Imagem de rosto recebida de {chat_id} e salva em {photo_path}")

            video_path = user_sessions[chat_id]['video']
            output_path = f'static/output_{chat_id}.mp4'

            bot.send_message(chat_id, "🛠️ Processando vídeo... Isso pode levar alguns segundos.")
            try:
                process_video(video_path, photo_path, output_path)
                if os.path.exists(output_path):
                    bot.send_video(chat_id, open(output_path, 'rb'), caption="✅ Aqui está seu vídeo com o rosto trocado.")
                    logger.info(f"🎉 Vídeo processado enviado para {chat_id}")
                else:
                    bot.send_message(chat_id, "❌ Ocorreu um erro: o vídeo final não foi gerado.")
            except Exception as e:
                bot.send_message(chat_id, f"❌ Falha ao processar o vídeo: {e}")

        else:
            bot.send_message(chat_id, "📤 Envie um vídeo e depois a imagem com o rosto a ser usado.")

    except Exception as e:
        logger.exception("❌ Erro no webhook")
        bot.send_message(chat_id, "❌ Ocorreu um erro inesperado. Tente novamente mais tarde.")

    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)