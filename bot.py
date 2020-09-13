from telegram.ext import Updater, CommandHandler
import youtube_dl
import os
import logging


def download(url: str) -> None:
    ydl_opts = {
        'audio_format': 'mp3',
        'extract-audio': True,
        'ignore-errors': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        x = ydl.extract_info(url, download=False)
        # from pprint import pprint
        # pprint(x)
        ydl.download([url])
    return x['title']


# download('https://www.youtube.com/watch?v=lr9CmQ7XqS0')


def download_and_send(updater, context):
    if len(context.args) != 1:
        updater.message.reply_text('Provide the url and only it, please.')

    url = context.args[0]

    updater.message.reply_text('Downloading from your link...')
    title = download(url)
    file_path = [x for x in os.listdir() if x.startswith(title)][0]
    with open(file_path, 'rb') as f:
        updater.message.reply_text('Sending the file...')
        updater.message.bot.send_audio(updater.effective_chat.id,
                                       audio=f,
                                       timeout=60)
    os.remove(file_path)


def main():
    token = os.environ.get('TELEGRAM_TOKEN')
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('download', download_and_send))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    main()
