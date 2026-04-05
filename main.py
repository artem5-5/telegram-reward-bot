import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from services.reward_service import RewardService
from aiogram.types import BotCommand
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Сервис наград
reward_service = RewardService()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="award", description="Выдать награду"),
        BotCommand(command="rewards", description="Посмотреть награды"),
        BotCommand(command="remove_award", description="Удалить награду"),
        BotCommand(command="add_admin", description="Добавить администратора"),
        BotCommand(command="remove_admin", description="Удалить администратора"),
    ]

    await bot.set_my_commands(commands)

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

    response = reward_service.format_user_rewards(username)
    await message.reply(response)

@dp.message(Command("remove_award"))
async def remove_award_command(message: types.Message):
    if message.chat.type not in ['group', 'supergroup']:
        await message.reply("Эта команда доступна только в групповых чатах.")
        return

    removed_by_username = message.from_user.username
    if not removed_by_username:
        await message.reply("У вас должен быть установлен username.")
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.reply("Использование: /remove_award @username id")
        return

    _, username_arg, reward_id_arg = args

    if not username_arg.startswith('@'):
        await message.reply("Укажите пользователя в формате @username")
        return

    if not reward_id_arg.isdigit():
        await message.reply("ID должен быть числом")
        return

    target_username = username_arg[1:]
    reward_id = int(reward_id_arg)

    success, response = reward_service.remove_reward_by_id(
        target_username=target_username,
        reward_id=reward_id,
        removed_by=removed_by_username
    )

    await message.reply(response)

async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())