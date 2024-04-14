from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import openai


load_dotenv()
API_TOKEN = os.getenv("TOKEN")
OPENAI_API_TOKEN = os.getenv("OPENAI_API_KEY")

# connecting with OPENAI
openai.api_key= OPENAI_API_TOKEN


# configure loggin
logging.basicConfig(level=logging.INFO)

MODEL_NAME = "gpt-3.5-turbo"

# initialise bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

class Reference:
    def __init__(self) -> None:
        self.response = ""

reference = Reference()

def clear_history():
    reference.respone = ""

@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    """
    this is the handler for /start command
    """
    await message.reply("Hello, How may I assist you today?")

@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_history()
    await message.reply("I've cleared the past conversation and context.")


@dp.message_handler(commands=["help"])
async def welcome(message: types.Message):
    """
    this is the handler for /help command
    """
    help_command = """
    Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    """
    await message.reply(help_command)

@dp.message_handler()
async def main(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")

    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)



if __name__== "__main__":
    executor.start_polling(dp, skip_updates=True)
