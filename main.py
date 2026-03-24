import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from services.reward_service import RewardService
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Сервис наград
reward_service = RewardService()

@dp.message(Command("award"))
async def award_command(message: types.Message):
    if message.chat.type not in ['group', 'supergroup']:
        await message.reply("Эта команда доступна только в групповых чатах.")
        return

    awarded_by_username = message.from_user.username
    if not awarded_by_username:
        await message.reply("У вас должен быть установлен username для использования бота.")
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.reply("Использование: /award @username комментарий")
        return

    _, username_arg, comment = args
    if not username_arg.startswith('@'):
        await message.reply("Укажите пользователя в формате @username")
        return

    awarded_username = username_arg[1:]  # Убираем @

    success, response = reward_service.award_reward(awarded_username, comment, awarded_by_username)
    await message.reply(response)

@dp.message(Command("add_admin"))
async def add_admin_command(message: types.Message):
    if message.chat.type not in ['group', 'supergroup']:
        await message.reply("Эта команда доступна только в групповых чатах.")
        return

    owner_username = message.from_user.username
    if not owner_username:
        await message.reply("У вас должен быть установлен username для использования бота.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Использование: /add_admin @username")
        return

    _, username_arg = args
    if not username_arg.startswith('@'):
        await message.reply("Укажите пользователя в формате @username")
        return

    new_admin_username = username_arg[1:]

    success, response = reward_service.add_admin(owner_username, new_admin_username)
    await message.reply(response)

@dp.message(Command("remove_admin"))
async def remove_admin_command(message: types.Message):
    if message.chat.type not in ['group', 'supergroup']:
        await message.reply("Эта команда доступна только в групповых чатах.")
        return

    owner_username = message.from_user.username
    if not owner_username:
        await message.reply("У вас должен быть установлен username для использования бота.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Использование: /remove_admin @username")
        return

    _, username_arg = args
    if not username_arg.startswith('@'):
        await message.reply("Укажите пользователя в формате @username")
        return

    admin_username = username_arg[1:]

    success, response = reward_service.remove_admin(owner_username, admin_username)
    await message.reply(response)

@dp.message(Command("rewards"))
async def rewards_command(message: types.Message):
    if message.chat.type not in ['group', 'supergroup']:
        await message.reply("Эта команда доступна только в групповых чатах.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Использование: /rewards @username")
        return

    _, username_arg = args
    if not username_arg.startswith('@'):
        await message.reply("Укажите пользователя в формате @username")
        return

    username = username_arg[1:]
    count = reward_service.get_user_reward_count(username)
    await message.reply(f"У пользователя @{username} {count} наград.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())