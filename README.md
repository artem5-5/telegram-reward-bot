# Telegram Reward Bot

Бот для учета наград в Telegram группах.

## Установка

1. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

2. Настройте `config.py`:
   - Получите токен бота от @BotFather в Telegram.
   - Укажите ваш `BOT_TOKEN`.
   - Укажите ваш `OWNER_ID` (числовой ID).
   - Укажите ваш `OWNER_USERNAME` (без @).

3. Запустите бота:
   ```
   python main.py
   ```

## Команды

- `/award @username комментарий` - Выдать награду пользователю с комментарием.
- `/add_admin @username` - Добавить администратора (только владелец).
- `/remove_admin @username` - Удалить администратора (только владелец).
- `/rewards @username` - Показать количество наград у пользователя.

## Структура проекта

- `main.py` - Основной файл бота.
- `services/reward_service.py` - Логика сервиса наград.
- `repo/admin_repo.py` - Репозиторий администраторов.
- `repo/reward_repo.py` - Репозиторий наград.
- `config.py` - Конфигурация.
- `data/` - Директория для данных (admins.json, rewards.json).