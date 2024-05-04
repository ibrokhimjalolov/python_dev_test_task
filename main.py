import asyncio
import logging
import sys
import json
import datetime

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN
from helper import get_period_stat
# Bot token can be obtained via https://t.me/BotFather

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def input_handler(message: Message) -> None:
    try:
        data = json.loads(message.text)
        dt_from = data["dt_from"]
        dt_upto = data["dt_upto"]
        group_type = data["group_type"]
        dt_from = datetime.datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S")
        dt_upto = datetime.datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S")
        assert group_type in ["hour", "day", "month"], "Invalid group type"
    except (json.JSONDecodeError, KeyError, ValueError, AssertionError):
        await message.answer("Invalid JSON")
        return
    result = await get_period_stat(dt_from, dt_upto, group_type)
    await message.answer(json.dumps(result))
    

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
