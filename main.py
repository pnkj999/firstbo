from telegram.ext import Updater, CommandHandler
import requests
import logging
import os, sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def hello(update, context):
    update.message.reply_text('Hello {}'.format(
        update.message.from_user.first_name))


def dog(update, context):
    dog = context.args[0]
    chat_id = update.message.chat.id
    link = "https://dog.ceo/api/breed/{}/images/random".format(dog)
    image = requests.get(link).json()
    url = image['message']
    context.bot.send_photo(chat_id=chat_id, photo=url)


def answer(update, context):
    chat_id = update.message.chat.id
    response = requests.get("https://yesno.wtf/api").json()
    answer = response['answer']
    update.message.reply_text(answer)
    link = response['image']
    context.bot.send_document(chat_id=chat_id, document=link)


def help(update, context):
    text = "How to use this bot?\n"
    text += "/dog breed\n"
    text += "/covid country\n"
    text += "/answer\n"
    update.message.reply_text(text)


def covid(update, context):
    country = context.args[0]

    url = "https://covid-193.p.rapidapi.com/statistics"

    querystring = {"country": country}

    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "IX5gQnPCCSmsht2XxNGDLsqmkLLXp1NSpZwjsnzXYi653VgHr4"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring).json()

    text = str(response)
    update.message.reply_text(text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    try:
        TOKEN = sys.argv[1]
    except IndexError:
        TOKEN = os.environ.get("TOKEN")
	
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(CommandHandler('answer', answer))
    dp.add_handler(CommandHandler('covid', covid))
    dp.add_handler(CommandHandler('dog', dog))
    dp.add_handler(CommandHandler('help', help))
    dp.add_error_handler(error)

    logger.info("Ready to rock..!")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
