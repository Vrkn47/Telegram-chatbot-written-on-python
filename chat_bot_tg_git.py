from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from collections import defaultdict

# the list of forbidden words
forbidden_words = {'bad_word1', 'bad_word2'}  
# storing user warnings
user_warnings = defaultdict(int)

# the command handler function /repeat
async def repeat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        message_to_repeat = ' '.join(context.args)
        await update.message.reply_text(message_to_repeat)
    else:
        await update.message.reply_text('Please specify the text to repeat (the text is specified in one message after the /repeat command).')

# the handler function of text message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id  # get chat_id
    user_id = update.message.from_user.id  # get user_id
    message_text = update.message.text.lower()  # get the text of message

    # cheking for prohibited words
    if any(word in message_text for word in forbidden_words):
        user_warnings[user_id] += 1
        await update.message.reply_text(f'Warning! You have {user_warnings[user_id]} warnings.')

        # if the user has 3 warnings, then ban him
        if user_warnings[user_id] >= 3:
            await context.bot.kick_chat_member(chat_id, user_id)
            await update.message.reply_text(f'User {update.message.from_user.username} was banned for obscene language.')
            del user_warnings[user_id]  # removing warnings after the ban

        # delete the message
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Enter your descreption of the bot")

async def random_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    import random
    number = random.randint(1, 100)  # generating a random number from 1 to 100
    await update.message.reply_text(f'Random number: {number}')

async def set_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        global forbidden_words
        forbidden_words = set(context.args)
        await update.message.reply_text(f'The list of forbidden words has been updated: {", ".join(forbidden_words)}')
    else:
        await update.message.reply_text('Please specify the words to add (the words are specified in one message after the /setwords command).')

async def show_forbidden_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Current forbidden words: {", ".join(forbidden_words)}')
 
def main():
    # enter your token
    TOKEN = 'YOUR_TOKEN_HERE'

    # creating an application object
    app = ApplicationBuilder().token(TOKEN).build()

    # registration of handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random_number))  # command handler /random
    app.add_handler(CommandHandler("setwords", set_words))
    app.add_handler(CommandHandler("repeat", repeat))  # command handler /repeat
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # bot starting
    app.run_polling()

if __name__ == '__main__':
    main()

