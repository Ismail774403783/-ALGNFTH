from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import API_KEY
from scrapper import get_last_articles


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    last_article = tuple(get_last_articles())[0]
    update.message.reply_text(last_article)


def main():
    updater = Updater(API_KEY)

    dp = updater.dispatcher
    # dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    updater.start_polling()
    updater.idle()


main()
