# import os
# from aiogram import Bot, Dispatcher, types
# import ccxt
# from dotenv import load_dotenv
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
#
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
# })
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['balance'])
# async def get_balance(message: types.Message):
#     balance = exchange.fetch_balance()
#     await message.answer(f"Ваш баланс: {balance['total']['BTC']} BTC")
#
# # Добавьте другие команды по аналогии
#
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)




# import os
# from aiogram import Bot, Dispatcher, types
# import ccxt
# from dotenv import load_dotenv
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация бота и диспетчера
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
# })
#
# # Создание клавиатуры для меню
# menu = ReplyKeyboardMarkup(resize_keyboard=True)
# menu.add(KeyboardButton("/balance"))
# menu.add(KeyboardButton("/price"))
# menu.add(KeyboardButton("/tradehistory"))
#
# # Обработчик команды /start, который показывает меню
# @dp.message_handler(commands=['start'])
# async def show_menu(message: types.Message):
#     await message.answer("Выберите команду из меню:", reply_markup=menu)
#
# # Обработчик команды /balance для проверки баланса на Binance
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['balance'])
# async def get_balance(message: types.Message):
#     balance = exchange.fetch_balance()
#     await message.answer(f"Ваш баланс: {balance['total']['BTC']} BTC")
#
# # Обработчик команды /price для проверки текущей цены BTC
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['price'])
# async def get_price(message: types.Message):
#     ticker = exchange.fetch_ticker('BTC/USDT')
#     await message.answer(f"Текущая цена BTC: {ticker['last']} USDT")
#
# # Обработчик команды /setalert для установки уведомлений о цене
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['setalert'])
# async def set_alert(message: types.Message):
#     try:
#         _, currency, price = message.text.split()
#         price_alerts[currency.upper()] = float(price)
#         await message.answer(f"Уведомление установлено для {currency.upper()} при цене {price} USDT")
#     except ValueError:
#         await message.answer("Используйте формат: /setalert BTC 50000")
#
# # Обработчик команды /tradehistory для просмотра истории торгов
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['tradehistory'])
# async def trade_history(message: types.Message):
#     trades = exchange.fetch_my_trades('BTC/USDT', limit=5)
#     response = "Последние 5 сделок:\n"
#     for trade in trades:
#         response += f"Тип: {trade['side']} Цена: {trade['price']} Количество: {trade['amount']}\n"
#     await message.answer(response)
#
# # Обработчик команд /buy и /sell для выполнения торговых операций
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['buy', 'sell'])
# async def trade(message: types.Message):
#     try:
#         command, currency, amount = message.text.split()
#         symbol = f"{currency.upper()}/USDT"
#         if command == "/buy":
#             order = exchange.create_market_buy_order(symbol, amount)
#         else:
#             order = exchange.create_market_sell_order(symbol, amount)
#         await message.answer(f"Ордер {order['side']} выполнен по цене {order['price']}")
#     except Exception as e:
#         await message.answer(f"Ошибка: {str(e)}")
#
# # Запуск бота
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)





# import os
# import logging
# from aiogram import Bot, Dispatcher, types
# import ccxt
# from dotenv import load_dotenv
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация бота и диспетчера
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
#     'enableRateLimit': True
# })
#
# # Создание клавиатуры для меню
# menu = ReplyKeyboardMarkup(resize_keyboard=True)
# menu.add(KeyboardButton("/balance"))
# menu.add(KeyboardButton("/price"))
# menu.add(KeyboardButton("/tradehistory"))
# menu.add(KeyboardButton("/clear"))
#
# # Обработчик команды /start
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     greeting = (
#         "Привет! Я ваш торговый бот для Binance.\n"
#         "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
#         "Чтобы начать, выберите команду из меню ниже:"
#     )
#     await message.answer(greeting, reply_markup=menu)
#
# # Обработчик команды /help
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     help_text = (
#         "/balance - Показать ваш баланс на Binance.\n"
#         "/price - Показать текущую цену BTC.\n"
#         "/tradehistory - Показать историю ваших торгов.\n"
#         "/clear - 'Очистить' чат.\n"
#         "Выберите команду из меню или введите ее вручную:"
#     )
#     await message.answer(help_text, reply_markup=menu)
#
# # ... [остальные обработчики]
#
# # Запуск бота
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)



# import os
# import logging
# from aiogram import Bot, Dispatcher, types
# import ccxt.async_support as ccxt  # Используем асинхронную версию ccxt
# from dotenv import load_dotenv
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация бота и диспетчера
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
#     'enableRateLimit': True
# })
#
# # Создание клавиатуры для меню
# menu = ReplyKeyboardMarkup(resize_keyboard=True)
# menu.add(KeyboardButton("/balance"))
# menu.add(KeyboardButton("/price"))
# menu.add(KeyboardButton("/tradehistory"))
# menu.add(KeyboardButton("/clear"))
#
# # Функция для отображения меню после каждого запроса
# async def show_menu_after_request(message: types.Message):
#     await message.answer("Выберите следующую команду из меню:", reply_markup=menu)
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     greeting = (
#         "Привет! Я ваш торговый бот для Binance.\n"
#         "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
#         "Чтобы начать, выберите команду из меню ниже:"
#     )
#     await message.answer(greeting, reply_markup=menu)
#
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     help_text = (
#         "/balance - Показать ваш баланс на Binance.\n"
#         "/price - Показать текущую цену BTC.\n"
#         "/tradehistory - Показать историю ваших торгов.\n"
#         "/clear - 'Очистить' чат.\n"
#         "Выберите команду из меню или введите ее вручную:"
#     )
#     await message.answer(help_text, reply_markup=menu)
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['clear'])
# async def clear_chat(message: types.Message):
#     await message.answer("Чат очищен.")
#     await show_menu_after_request(message)
#
# # @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['balance'])
# # async def get_balance(message: types.Message):
# #     try:
# #         balance = await exchange.fetch_balance()
# #         await message.answer(f"Ваш баланс: {balance['total']['BTC']} BTC")
# #         await show_menu_after_request(message)
# #     except Exception as e:
# #         logging.error(f"Ошибка при получении баланса: {e}")
# #         await message.answer("Ошибка при получении баланса.")
#
#
# # @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['balance'])
# # async def get_balance(message: types.Message):
# #     try:
# #         # Типы кошельков на Binance
# #         wallet_types = ['spot', 'margin', 'futures']
# #
# #         all_balances = {}
# #         for wallet_type in wallet_types:
# #             balance = await exchange.fetch_balance({'type': wallet_type})
# #             non_zero_balances = {coin: amount for coin, amount in balance['total'].items() if amount and amount > 0}
# #             if non_zero_balances:
# #                 all_balances[wallet_type] = non_zero_balances
# #
# #         # Если нет монет с ненулевым балансом
# #         if not all_balances:
# #             await message.answer("На ваших кошельках нет монет. Баланс USDT: 0.0")
# #             return
# #
# #         # Формируем ответное сообщение
# #         response = ["Ваши балансы:"]
# #         for wallet_type, balances in all_balances.items():
# #             response.append(f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹")
# #             for coin, amount in balances.items():
# #                 formatted_amount = f"{amount:.8f}".rstrip('0').rstrip('.')
# #                 response.append(f"• {coin}: {formatted_amount}")
# #
# #         # Если нет USDT в списке, добавляем его со значением 0.0
# #         if not any('USDT' in balances for balances in all_balances.values()):
# #             response.append("\nUSDT: 0.0")
# #
# #         await message.answer("\n".join(response))
# #         await show_menu_after_request(message)
# #     except Exception as e:
# #         logging.error(f"Ошибка при получении баланса: {e}")
# #         await message.answer("Ошибка при получении баланса.")
#
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['balance'])
# async def get_balance(message: types.Message):
#     try:
#         # Типы кошельков на Binance
#         wallet_types = ['spot', 'margin', 'futures']
#
#         response = ["Ваши балансы:"]
#         for wallet_type in wallet_types:
#             balance = await exchange.fetch_balance({'type': wallet_type})
#             usdt_balance = balance['total'].get('USDT', 0)
#             traded_coins = {coin: amount for coin, amount in balance['total'].items() if coin != 'USDT' and amount > 0}
#
#             response.append(f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹")
#             response.append(f"Баланс: {usdt_balance:.2f} USDT")
#
#             if traded_coins:
#                 for coin, amount in traded_coins.items():
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     coin_value_usdt = ticker['last'] * amount
#                     percentage = (coin_value_usdt / (coin_value_usdt + usdt_balance)) * 100
#                     response.append(f"Торгуется {coin_value_usdt:.2f} USDT в {coin} ({percentage:.2f}%)")
#             else:
#                 response.append("Не торгуется депозитом данного кошелька.")
#
#         await message.answer("\n".join(response))
#         await show_menu_after_request(message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении баланса: {e}")
#         await message.answer("Ошибка при получении баланса.")
#
#
#
# # @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['price'])
# # async def get_price(message: types.Message):
# #     try:
# #         price = await exchange.fetch_ticker('BTC/USDT')
# #         await message.answer(f"Текущая цена BTC: {price['last']} USDT")
# #         await show_menu_after_request(message)
# #     except Exception as e:
# #         logging.error(f"Ошибка при получении цены: {e}")
# #         await message.answer("Ошибка при получении цены.")
#
# class PriceQuery(StatesGroup):
#     input_coin = State()
#
#
# async def get_top_20_coins():
#     # Здесь можно использовать API, например, CoinMarketCap или Binance, чтобы получить список топ-20 монет.
#     # Для простоты я буду использовать фиктивный список.
#     return ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC", "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]
#
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['price'])
# async def show_top_20_coins(message: types.Message):
#     top_20 = await get_top_20_coins()
#     markup = InlineKeyboardMarkup(row_width=4)
#     for coin in top_20:
#         button = InlineKeyboardButton(coin, callback_data=f"price_{coin}")
#         markup.add(button)
#     markup.add(InlineKeyboardButton("Ввести вручную", callback_data="input_manually"))
#     await message.answer("Выберите монету или введите её вручную:", reply_markup=markup)
#
# @dp.callback_query_handler(lambda c: c.data == 'input_manually', state=None)
# async def ask_for_coin(callback_query: types.CallbackQuery):
#     await PriceQuery.input_coin.set()
#     await callback_query.message.answer("Введите название монеты:")
#     await callback_query.answer()
#
# @dp.message_handler(state=PriceQuery.input_coin)
# async def get_price_for_input(message: types.Message, state: FSMContext):
#     coin = message.text.upper()
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await message.answer(f"Ошибка при получении цены для {coin}. Убедитесь, что монета существует и попробуйте снова.")
#     await state.finish()
#
# @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# async def show_coin_price(callback_query: types.CallbackQuery):
#     coin = callback_query.data.split('_')[1]
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await callback_query.message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await callback_query.message.answer(f"Ошибка при получении цены для {coin}.")
#     await callback_query.answer()
#
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['tradehistory'])
# async def get_trade_history(message: types.Message):
#     try:
#         trades = await exchange.fetch_my_trades('BTC/USDT', limit=5)  # последние 5 сделок
#         trade_messages = [f"Сделка {trade['id']}: {trade['amount']} BTC по цене {trade['price']} USDT" for trade in trades]
#         await message.answer("\n".join(trade_messages))
#         await show_menu_after_request(message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении истории торгов: {e}")
#         await message.answer("Ошибка при получении истории торгов.")
#
# # Запуск бота
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)



# import os
# import logging
# from aiogram import Bot, Dispatcher, types
# import ccxt.async_support as ccxt  # Используем асинхронную версию ccxt
# from dotenv import load_dotenv
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация бота и диспетчера
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
#     'enableRateLimit': True
# })
#
# # Создание клавиатуры для меню
# menu = ReplyKeyboardMarkup(resize_keyboard=True)
# menu.add(KeyboardButton("/balance"))
# menu.add(KeyboardButton("/price"))
# menu.add(KeyboardButton("/tradehistory"))
# menu.add(KeyboardButton("/clear"))
#
# # Функция для отображения меню после каждого запроса
# async def show_menu_after_request(message: types.Message):
#     await message.answer("Выберите следующую команду из меню:", reply_markup=menu)
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     greeting = (
#         "Привет! Я ваш торговый бот для Binance.\n"
#         "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
#         "Чтобы начать, выберите команду из меню ниже:"
#     )
#     await message.answer(greeting, reply_markup=menu)
#
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     help_text = (
#         "/balance - Показать ваш баланс на Binance.\n"
#         "/price - Показать текущую цену BTC.\n"
#         "/tradehistory - Показать историю ваших торгов.\n"
#         "/clear - 'Очистить' чат.\n"
#         "Выберите команду из меню или введите ее вручную:"
#     )
#     await message.answer(help_text, reply_markup=menu)
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['clear'])
# async def clear_chat(message: types.Message):
#     await message.answer("Чат очищен.")
#     await show_menu_after_request(message)
#
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['balance'])
# async def get_balance(message: types.Message):
#     try:
#         # Типы кошельков на Binance
#         wallet_types = ['spot', 'margin', 'futures']
#
#         response = ["Ваши балансы:"]
#         for wallet_type in wallet_types:
#             balance = await exchange.fetch_balance({'type': wallet_type})
#             usdt_balance = balance['total'].get('USDT', 0)
#             traded_coins = {coin: amount for coin, amount in balance['total'].items() if coin != 'USDT' and amount > 0}
#
#             response.append(f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹")
#             response.append(f"Баланс: {usdt_balance:.2f} USDT")
#
#             if traded_coins:
#                 for coin, amount in traded_coins.items():
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     coin_value_usdt = ticker['last'] * amount
#                     percentage = (coin_value_usdt / (coin_value_usdt + usdt_balance)) * 100
#                     response.append(f"Торгуется {coin_value_usdt:.2f} USDT в {coin} ({percentage:.2f}%)")
#             else:
#                 response.append("Не торгуется депозитом данного кошелька.")
#
#         await message.answer("\n".join(response))
#         await show_menu_after_request(message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении баланса: {e}")
#         await message.answer("Ошибка при получении баланса.")
#
#
# class PriceQuery(StatesGroup):
#     input_coin = State()
#
# async def get_listed_coins():
#     # Здесь можно использовать API, например, CoinMarketCap или Binance, чтобы получить список монет.
#     # Для простоты я буду использовать фиктивный список.
#     return ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC", "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['price'])
# async def show_listed_coins(message: types.Message):
#     coins = await get_listed_coins()
#     markup = InlineKeyboardMarkup(row_width=4)
#     for coin in coins:
#         button = InlineKeyboardButton(coin, callback_data=f"price_{coin}")
#         markup.add(button)
#     markup.add(InlineKeyboardButton("Ввести вручную", callback_data="input_manually"))
#     await message.answer("Выберите монету или введите её вручную:", reply_markup=markup)
#
#
# @dp.callback_query_handler(lambda c: c.data == 'input_manually', state=None)
# async def ask_for_coin(callback_query: types.CallbackQuery):
#     await PriceQuery.input_coin.set()
#     await callback_query.message.answer("Введите название монеты:")
#     await callback_query.answer()
#
# @dp.message_handler(state=PriceQuery.input_coin)
# async def get_price_for_input(message: types.Message, state: FSMContext):
#     coin = message.text.upper()
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await message.answer(f"Ошибка при получении цены для {coin}. Убедитесь, что монета существует и попробуйте снова.")
#     await state.finish()
#
# @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# async def show_coin_price(callback_query: types.CallbackQuery):
#     coin = callback_query.data.split('_')[1]
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await callback_query.message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await callback_query.message.answer(f"Ошибка при получении цены для {coin}.")
#     await callback_query.answer()
#
#
# @dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=['tradehistory'])
# async def get_trade_history(message: types.Message):
#     try:
#         trades = await exchange.fetch_my_trades('BTC/USDT', limit=5)  # последние 5 сделок
#         trade_messages = [f"Сделка {trade['id']}: {trade['amount']} BTC по цене {trade['price']} USDT" for trade in trades]
#         await message.answer("\n".join(trade_messages))
#         await show_menu_after_request(message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении истории торгов: {e}")
#         await message.answer("Ошибка при получении истории торгов.")
#
# # Запуск бота
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)



# import os
# import logging
# import asyncio
# from aiogram import Bot, Dispatcher, types
# import ccxt.async_support as ccxt
# from dotenv import load_dotenv
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.dispatcher.storage import BaseStorage, FSMContext
#
#
# class SimpleDictStorage(BaseStorage):
#
#     def __init__(self):
#         self.data = {}
#
#     async def close(self):
#         self.data.clear()
#
#     async def wait_closed(self):
#         pass
#
#     async def get_data(self, chat=None, user=None, default=None):
#         key = self.get_key(chat, user)
#         return self.data.get(key, default)
#
#     async def set_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         self.data[key] = data
#
#     async def reset_data(self, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             del self.data[key]
#
#     async def get_state(self, chat=None, user=None, default=None):
#         data = await self.get_data(chat, user, default)
#         if data:
#             return data.get('state', default)
#         return default
#
#     async def set_state(self, state, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key not in self.data:
#             self.data[key] = {}
#         self.data[key]['state'] = state
#
#     async def update_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             self.data[key].update(data)
#         else:
#             self.data[key] = data
#
#     def get_key(self, chat, user):
#         return f"{chat}:{user}"
#
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация MemoryStorage
# storage = SimpleDictStorage()
#
#
# # Инициализация бота и диспетчера с использованием MemoryStorage
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot, storage=storage)
#
#
# # Добавление middleware для логирования
# dp.middleware.setup(LoggingMiddleware())
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
#     'enableRateLimit': True
# })
#
# # Создание инлайн клавиатуры для меню
# menu = InlineKeyboardMarkup(row_width=2)
# menu.add(InlineKeyboardButton("Balance", callback_data="menu_balance"))
# menu.add(InlineKeyboardButton("Price", callback_data="menu_price"))
# menu.add(InlineKeyboardButton("Trade History", callback_data="menu_tradehistory"))
# menu.add(InlineKeyboardButton("Clear", callback_data="menu_clear"))
#
# # Функция для отображения меню после каждого запроса
# async def show_menu_after_request(message: types.Message):
#     await message.answer("Выберите следующую команду из меню:", reply_markup=menu)
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     greeting = (
#         "Привет! Я ваш торговый бот для Binance.\n"
#         "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
#         "Чтобы начать, выберите команду из меню ниже:"
#     )
#     await message.answer(greeting, reply_markup=menu)
#
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     help_text = (
#         "/balance - Показать ваш баланс на Binance.\n"
#         "/price - Показать текущую цену BTC.\n"
#         "/tradehistory - Показать историю ваших торгов.\n"
#         "/clear - 'Очистить' чат.\n"
#         "Выберите команду из меню или введите ее вручную:"
#     )
#     await message.answer(help_text, reply_markup=menu)
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_clear')
# async def clear_chat(callback_query: types.CallbackQuery):
#     await callback_query.message.answer("Чат очищен.")
#     await show_menu_after_request(callback_query.message)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_balance')
# async def get_balance(callback_query: types.CallbackQuery):
#     try:
#         # Типы кошельков на Binance
#         wallet_types = ['spot', 'margin', 'futures']
#
#         response = ["Ваши балансы:"]
#         for wallet_type in wallet_types:
#             balance = await exchange.fetch_balance({'type': wallet_type})
#             usdt_balance = balance['total'].get('USDT', 0)
#             traded_coins = {coin: amount for coin, amount in balance['total'].items() if coin != 'USDT' and amount > 0}
#
#             response.append(f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹")
#             response.append(f"Баланс: {usdt_balance:.2f} USDT")
#
#             if traded_coins:
#                 for coin, amount in traded_coins.items():
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     coin_value_usdt = ticker['last'] * amount
#                     percentage = (coin_value_usdt / (coin_value_usdt + usdt_balance)) * 100
#                     response.append(f"Торгуется {coin_value_usdt:.2f} USDT в {coin} ({percentage:.2f}%)")
#             else:
#                 response.append("Не торгуется депозитом данного кошелька.")
#
#         await callback_query.message.answer("\n".join(response))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении баланса: {e}")
#         await callback_query.message.answer("Ошибка при получении баланса.")
#     await callback_query.answer()
#
#
# class PriceQuery(StatesGroup):
#     input_coin = State()
#
# async def get_listed_coins():
#     # Здесь можно использовать API, например, CoinMarketCap или Binance, чтобы получить список монет.
#     # Для простоты я буду использовать фиктивный список.
#     return ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC", "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_price')
# async def menu_price_handler(callback_query: types.CallbackQuery):
#     coins = await get_listed_coins()
#     markup = InlineKeyboardMarkup(row_width=4)
#     for coin in coins:
#         button = InlineKeyboardButton(coin, callback_data=f"price_{coin}")
#         markup.add(button)
#     markup.add(InlineKeyboardButton("Ввести вручную", callback_data="input_manually"))
#     await callback_query.message.answer("Выберите монету или введите её вручную:", reply_markup=markup)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'input_manually', state=None)
# async def ask_for_coin(callback_query: types.CallbackQuery):
#     await PriceQuery.input_coin.set()
#     await callback_query.message.answer("Введите название монеты:")
#     await callback_query.answer()
#
# @dp.message_handler(state=PriceQuery.input_coin)
# async def get_price_for_input(message: types.Message, state: FSMContext):
#     coin = message.text.upper()
#     coins = await get_listed_coins()  # Получаем список доступных монет
#     if coin not in coins:
#         await message.answer(f"Монета {coin} не найдена. Пожалуйста, введите другую монету.")
#         return
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
#     await state.finish()
#
# @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# async def show_coin_price(callback_query: types.CallbackQuery):
#     coin = callback_query.data.split('_')[1]
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await callback_query.message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await callback_query.message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_tradehistory')
# async def menu_tradehistory_handler(callback_query: types.CallbackQuery):
#     try:
#         trades = await exchange.fetch_my_trades('BTC/USDT', limit=5)  # последние 5 сделок
#         trade_messages = [f"Сделка {trade['id']}: {trade['amount']} BTC по цене {trade['price']} USDT" for trade in trades]
#         await callback_query.message.answer("\n".join(trade_messages))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении истории торгов: {e}")
#         await callback_query.message.answer("Ошибка при получении истории торгов.")
#     await callback_query.answer()
#
# # Запуск бота
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)
#
#




# import os
# import logging
# import asyncio
# from aiogram import Bot, Dispatcher, types
# import ccxt.async_support as ccxt
# from dotenv import load_dotenv
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.dispatcher.storage import BaseStorage, FSMContext
#
#
# class SimpleDictStorage(BaseStorage):
#
#     def __init__(self):
#         self.data = {}
#
#     async def close(self):
#         self.data.clear()
#
#     async def wait_closed(self):
#         pass
#
#     async def get_data(self, chat=None, user=None, default=None):
#         key = self.get_key(chat, user)
#         return self.data.get(key, default)
#
#     async def set_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         self.data[key] = data
#
#     async def reset_data(self, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             del self.data[key]
#
#     async def get_state(self, chat=None, user=None, default=None):
#         data = await self.get_data(chat, user, default)
#         if data:
#             return data.get('state', default)
#         return default
#
#     async def set_state(self, state, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key not in self.data:
#             self.data[key] = {}
#         self.data[key]['state'] = state
#
#     async def update_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             self.data[key].update(data)
#         else:
#             self.data[key] = data
#
#     def get_key(self, chat, user):
#         return f"{chat}:{user}"
#
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация MemoryStorage
# storage = SimpleDictStorage()
#
#
# # Инициализация бота и диспетчера с использованием MemoryStorage
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot, storage=storage)
#
#
# # Добавление middleware для логирования
# dp.middleware.setup(LoggingMiddleware())
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
#     'enableRateLimit': True
# })
#
# # Создание инлайн клавиатуры для меню
# menu = InlineKeyboardMarkup(row_width=2)
# menu.add(InlineKeyboardButton("Balance", callback_data="menu_balance"))
# menu.add(InlineKeyboardButton("Price", callback_data="menu_price"))
# menu.add(InlineKeyboardButton("Trade History", callback_data="menu_tradehistory"))
# menu.add(InlineKeyboardButton("Clear", callback_data="menu_clear"))
#
# # Функция для отображения меню после каждого запроса
# async def show_menu_after_request(message: types.Message):
#     await message.answer("Выберите следующую команду из меню:", reply_markup=menu)
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     greeting = (
#         "Привет! Я ваш торговый бот для Binance.\n"
#         "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
#         "Чтобы начать, выберите команду из меню ниже:"
#     )
#     await message.answer(greeting, reply_markup=menu)
#
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     help_text = (
#         "/balance - Показать ваш баланс на Binance.\n"
#         "/price - Показать текущую цену BTC.\n"
#         "/tradehistory - Показать историю ваших торгов.\n"
#         "/clear - 'Очистить' чат.\n"
#         "Выберите команду из меню или введите ее вручную:"
#     )
#     await message.answer(help_text, reply_markup=menu)
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_clear')
# async def clear_chat(callback_query: types.CallbackQuery):
#     await callback_query.message.answer("Чат очищен.")
#     await show_menu_after_request(callback_query.message)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_balance')
# async def get_balance(callback_query: types.CallbackQuery):
#     try:
#         # Типы кошельков на Binance
#         wallet_types = ['spot', 'margin', 'futures']
#
#         async def fetch_wallet_balance(wallet_type):
#             balance = await exchange.fetch_balance({'type': wallet_type})
#             usdt_balance = balance['total'].get('USDT', 0)
#             traded_coins = {coin: amount for coin, amount in balance['total'].items() if coin != 'USDT' and amount > 0}
#             response = [f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹", f"Баланс: {usdt_balance:.2f} USDT"]
#             if traded_coins:
#                 for coin, amount in traded_coins.items():
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     coin_value_usdt = ticker['last'] * amount
#                     percentage = (coin_value_usdt / (coin_value_usdt + usdt_balance)) * 100
#                     response.append(f"Торгуется {coin_value_usdt:.2f} USDT в {coin} ({percentage:.2f}%)")
#             else:
#                 response.append("Не торгуется депозитом данного кошелька.")
#             return response
#
#         responses = await asyncio.gather(*(fetch_wallet_balance(wallet) for wallet in wallet_types))
#
#         # Объединяем все ответы в один список
#         all_responses = ["Ваши балансы:"]
#         for response in responses:
#             all_responses.extend(response)
#
#         await callback_query.message.answer("\n".join(all_responses))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении баланса: {e}")
#         await callback_query.message.answer("Ошибка при получении баланса.")
#     await callback_query.answer()
#
#
# class PriceQuery(StatesGroup):
#     input_coin = State()
#
# async def get_listed_coins():
#     # Здесь можно использовать API, например, CoinMarketCap или Binance, чтобы получить список монет.
#     # Для простоты я буду использовать фиктивный список.
#     return ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC", "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_price')
# async def menu_price_handler(callback_query: types.CallbackQuery):
#     coins = await get_listed_coins()
#     markup = InlineKeyboardMarkup(row_width=4)
#     for coin in coins:
#         button = InlineKeyboardButton(coin, callback_data=f"price_{coin}")
#         markup.add(button)
#     markup.add(InlineKeyboardButton("Ввести вручную", callback_data="input_manually"))
#     await callback_query.message.answer("Выберите монету или введите её вручную:", reply_markup=markup)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'input_manually', state=None)
# async def ask_for_coin(callback_query: types.CallbackQuery):
#     await PriceQuery.input_coin.set()
#     await callback_query.message.answer("Введите название монеты:")
#     await callback_query.answer()
#
# @dp.message_handler(state=PriceQuery.input_coin)
# async def get_price_for_input(message: types.Message, state: FSMContext):
#     coin = message.text.upper()
#     coins = await get_listed_coins()  # Получаем список доступных монет
#     if coin not in coins:
#         await message.answer(f"Монета {coin} не найдена. Пожалуйста, введите другую монету.")
#         return
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#         await show_menu_after_request(message)  # Показываем меню после вывода цены
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
#     await state.finish()
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# async def show_coin_price(callback_query: types.CallbackQuery):
#     coin = callback_query.data.split('_')[1]
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await callback_query.message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await callback_query.message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_tradehistory')
# async def menu_tradehistory_handler(callback_query: types.CallbackQuery):
#     try:
#         trades = await exchange.fetch_my_trades('BTC/USDT', limit=5)  # последние 5 сделок
#         trade_messages = [f"Сделка {trade['id']}: {trade['amount']} BTC по цене {trade['price']} USDT" for trade in trades]
#         await callback_query.message.answer("\n".join(trade_messages))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении истории торгов: {e}")
#         await callback_query.message.answer("Ошибка при получении истории торгов.")
#     await callback_query.answer()
#
# # Запуск бота
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)


# Добавил функции увидомлений
# import os
# import logging
# import asyncio
# from aiogram import Bot, Dispatcher, types
# import ccxt.async_support as ccxt
# from dotenv import load_dotenv
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.dispatcher.storage import BaseStorage, FSMContext
#
# def is_number(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         return False
#
#
#
# class SimpleDictStorage(BaseStorage):
#
#     def __init__(self):
#         self.data = {}
#
#     async def close(self):
#         self.data.clear()
#
#     async def wait_closed(self):
#         pass
#
#     async def get_data(self, chat=None, user=None, default=None):
#         key = self.get_key(chat, user)
#         return self.data.get(key, default)
#
#     async def set_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         self.data[key] = data
#
#     async def reset_data(self, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             del self.data[key]
#
#     async def get_state(self, chat=None, user=None, default=None):
#         data = await self.get_data(chat, user, default)
#         if data:
#             return data.get('state', default)
#         return default
#
#     async def set_state(self, state, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key not in self.data:
#             self.data[key] = {}
#         self.data[key]['state'] = state
#
#     async def update_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             self.data[key].update(data)
#         else:
#             self.data[key] = data
#
#     def get_key(self, chat, user):
#         return f"{chat}:{user}"
#
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация MemoryStorage
# storage = SimpleDictStorage()
#
#
# # Инициализация бота и диспетчера с использованием MemoryStorage
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot, storage=storage)
#
#
# # Добавление middleware для логирования
# dp.middleware.setup(LoggingMiddleware())
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
#     'enableRateLimit': True
# })
#
# user_alerts_status = {}
#
#
# # Создание инлайн клавиатуры для меню
# menu = InlineKeyboardMarkup(row_width=2)
# menu.add(InlineKeyboardButton("Balance", callback_data="menu_balance"))
# menu.add(InlineKeyboardButton("Price", callback_data="menu_price"))
# menu.add(InlineKeyboardButton("Trade History", callback_data="menu_tradehistory"))
# menu.add(InlineKeyboardButton("Clear", callback_data="menu_clear"))
# menu.add(InlineKeyboardButton("Set Price Alert", callback_data="set_price_alert"))  # Добавляем инлайн-кнопку
# cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel_action")
# menu.add(InlineKeyboardButton("Activate Alerts", callback_data="activate_alerts"))
# menu.add(InlineKeyboardButton("Deactivate Alerts", callback_data="deactivate_alerts"))
#
#
#
# # Функция для отображения меню после каждого запроса
# async def show_menu_after_request(message: types.Message):
#     await message.answer("Выберите следующую команду из меню:", reply_markup=menu)
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     greeting = (
#         "Привет! Я ваш торговый бот для Binance.\n"
#         "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
#         "Чтобы начать, выберите команду из меню ниже:"
#     )
#     await message.answer(greeting, reply_markup=menu)
#
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     help_text = (
#         "/balance - Показать ваш баланс на Binance.\n"
#         "/price - Показать текущую цену BTC.\n"
#         "/tradehistory - Показать историю ваших торгов.\n"
#         "/clear - 'Очистить' чат.\n"
#         "Выберите команду из меню или введите ее вручную:"
#     )
#     await message.answer(help_text, reply_markup=menu)
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_clear')
# async def clear_chat(callback_query: types.CallbackQuery):
#     await callback_query.message.answer("Чат очищен.")
#     await show_menu_after_request(callback_query.message)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_balance')
# async def get_balance(callback_query: types.CallbackQuery):
#     try:
#         # Типы кошельков на Binance
#         wallet_types = ['spot', 'margin', 'futures']
#
#         async def fetch_wallet_balance(wallet_type):
#             balance = await exchange.fetch_balance({'type': wallet_type})
#             usdt_balance = balance['total'].get('USDT', 0)
#             traded_coins = {coin: amount for coin, amount in balance['total'].items() if coin != 'USDT' and amount > 0}
#             response = [f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹", f"Баланс: {usdt_balance:.2f} USDT"]
#             if traded_coins:
#                 for coin, amount in traded_coins.items():
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     coin_value_usdt = ticker['last'] * amount
#                     percentage = (coin_value_usdt / (coin_value_usdt + usdt_balance)) * 100
#                     response.append(f"Торгуется {coin_value_usdt:.2f} USDT в {coin} ({percentage:.2f}%)")
#             else:
#                 response.append("Не торгуется депозитом данного кошелька.")
#             return response
#
#         responses = await asyncio.gather(*(fetch_wallet_balance(wallet) for wallet in wallet_types))
#
#         # Объединяем все ответы в один список
#         all_responses = ["Ваши балансы:"]
#         for response in responses:
#             all_responses.extend(response)
#
#         await callback_query.message.answer("\n".join(all_responses))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении баланса: {e}")
#         await callback_query.message.answer("Ошибка при получении баланса.")
#     await callback_query.answer()
#
#
# class PriceQuery(StatesGroup):
#     input_coin = State()
#
# async def get_listed_coins():
#     # Здесь можно использовать API, например, CoinMarketCap или Binance, чтобы получить список монет.
#     # Для простоты я буду использовать фиктивный список.
#     return ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC", "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_price')
# async def menu_price_handler(callback_query: types.CallbackQuery):
#     coins = await get_listed_coins()
#     markup = InlineKeyboardMarkup(row_width=4)
#     for coin in coins:
#         button = InlineKeyboardButton(coin, callback_data=f"price_{coin}")
#         markup.add(button)
#     markup.add(InlineKeyboardButton("Ввести вручную", callback_data="input_manually"))
#     await callback_query.message.answer("Выберите монету или введите её вручную:", reply_markup=markup)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'input_manually', state=None)
# async def ask_for_coin(callback_query: types.CallbackQuery):
#     await PriceQuery.input_coin.set()
#     await callback_query.message.answer("Введите название монеты:")
#     await callback_query.answer()
#
# @dp.message_handler(state=PriceQuery.input_coin)
# async def get_price_for_input(message: types.Message, state: FSMContext):
#     coin = message.text.upper()
#     coins = await get_listed_coins()  # Получаем список доступных монет
#     if coin not in coins:
#         await message.answer(f"Монета {coin} не найдена. Пожалуйста, введите другую монету.")
#         return
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#         await show_menu_after_request(message)  # Показываем меню после вывода цены
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
#     await state.finish()
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# async def show_coin_price(callback_query: types.CallbackQuery):
#     coin = callback_query.data.split('_')[1]
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await callback_query.message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await callback_query.message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_tradehistory')
# async def menu_tradehistory_handler(callback_query: types.CallbackQuery):
#     try:
#         trades = await exchange.fetch_my_trades('BTC/USDT', limit=5)  # последние 5 сделок
#         trade_messages = [f"Сделка {trade['id']}: {trade['amount']} BTC по цене {trade['price']} USDT" for trade in trades]
#         await callback_query.message.answer("\n".join(trade_messages))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении истории торгов: {e}")
#         await callback_query.message.answer("Ошибка при получении истории торгов.")
#     await callback_query.answer()
#
# class PriceAlert(StatesGroup):
#     setting_coins = State()
#     setting_prices = State()
#
# @dp.callback_query_handler(lambda c: c.data == 'set_price_alert')
# async def set_price_alert_callback(callback_query: types.CallbackQuery):
#     await callback_query.message.answer("Введите монеты, разделенные запятыми, для которых вы хотите установить уведомление (например, BTC,ETH,ADA):")
#     await PriceAlert.setting_coins.set()
#     await callback_query.answer()
#
#
# @dp.message_handler(commands=['setpricealert'])
# async def set_price_alert_command(message: types.Message):
#     markup = InlineKeyboardMarkup().add(cancel_button)
#     await message.answer(
#         "Введите монеты, разделенные запятыми, для которых вы хотите установить уведомление (например, BTC,ETH,ADA):",
#         reply_markup=markup)
#
#
# @dp.message_handler(state=PriceAlert.setting_coins)
# async def set_alert_coins(message: types.Message, state: FSMContext):
#     coins = [coin.strip().upper() for coin in message.text.split(",")]
#     await state.update_data({"coins": coins})  # Исправленная строка
#     await message.answer(f"Введите пороговые цены для {', '.join(coins)} (например, 50000,3000,2):")
#     await PriceAlert.next()
#
#
# @dp.message_handler(state=PriceAlert.setting_prices)
# async def м(message: types.Message, state: FSMContext):
#     markup = InlineKeyboardMarkup().add(cancel_button)  # Добавляем кнопку отмены
#     user_data = await state.get_data()
#     coins = user_data.get("coins")
#
#     # Проверка ввода пользователя
#     if not all(is_number(price.strip()) for price in message.text.split(",")):
#         await message.answer("Пожалуйста, введите только числовые значения для цен. Попробуйте снова.", reply_markup=markup)
#         return
#
#     prices = [float(price.strip()) for price in message.text.split(",")]
#
#     if len(prices) != len(coins):
#         await message.answer("Количество монет и цен не совпадает. Пожалуйста, попробуйте снова.", reply_markup=markup)
#         return
#
#     # Здесь вы можете сохранить пороговые цены и монеты в базе данных или другом хранилище
#     # Например: save_alerts_to_db(user_id=message.from_user.id, alerts=dict(zip(coins, prices)))
#     await message.answer(
#         f"Уведомления установлены для: {', '.join([f'{coin} - {price} USDT' for coin, price in zip(coins, prices)])}.", reply_markup=markup)
#     await state.finish()
#
#     user_id = message.from_user.id
#     if not user_alerts_status.get(user_id, True):  # По умолчанию уведомления включены
#         return
#
#     # Сохранение уведомления в глобальном словаре
#     if user_id not in alerts:
#         alerts[user_id] = []
#     for coin, price in zip(coins, prices):
#         alerts[user_id].append({'coin': coin, 'price': price})
#
#
# @dp.callback_query_handler(lambda c: c.data == "cancel_action", state='*')
# async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
#     await state.finish()
#     await callback_query.message.answer("Действие отменено.")
#     await callback_query.answer()
#
#
# @dp.message_handler(lambda message: message.text.lower() == 'отмена', state='*')
# async def cancel_text(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is not None:
#         logging.info(f'Cancelling state {current_state}')
#         await state.finish()
#         await message.answer('Действие отменено.')
#     else:
#         await message.answer('Нет активного действия для отмены.')
#
#
# @dp.callback_query_handler(lambda c: c.data == 'activate_alerts')
# async def activate_alerts(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_alerts_status[user_id] = True
#     await callback_query.message.answer("Уведомления активированы.")
#     await callback_query.answer()
#
# @dp.callback_query_handler(lambda c: c.data == 'deactivate_alerts')
# async def deactivate_alerts(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_alerts_status[user_id] = False
#     await callback_query.message.answer("Уведомления деактивированы.")
#     await callback_query.answer()
#
# # Глобальный словарь для хранения уведомлений
# # Ключ - ID пользователя, значение - список словарей с монетой и пороговой ценой
# alerts = {}
#
# async def check_price_alerts():
#     while True:
#         for user_id, user_alerts in alerts.items():
#             for alert in user_alerts:
#                 coin = alert['coin']
#                 threshold_price = alert['price']
#
#                 try:
#                     # Получение текущей цены монеты
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     current_price = ticker['last']
#
#                     # Если текущая цена достигла или превысила порог
#                     if current_price >= threshold_price:
#                         await bot.send_message(user_id, f"Цена {coin} достигла {current_price} USDT!")
#                         user_alerts.remove(alert)  # Удалить уведомление после отправки
#                 except Exception as e:
#                     logging.error(f"Ошибка при проверке цены для {coin}: {e}")
#
#         # Пауза перед следующей проверкой
#         await asyncio.sleep(300)  # Проверка каждые 5 минут
#
# admin_id = 379834541  # Замените на ваш идентификатор пользователя в Telegram
#
# async def on_startup(dp):
#     await bot.send_message(admin_id, "Бот запущен")
#     asyncio.create_task(check_price_alerts())
#
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, on_startup=on_startup, skip_updates=True)




# Улучшил увидомления, показ меню, доабвил графики
# import os
# import logging
# import asyncio
# from aiogram import Bot, Dispatcher, types
# import ccxt.async_support as ccxt
# from dotenv import load_dotenv
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.dispatcher.storage import BaseStorage, FSMContext
# import matplotlib.pyplot as plt
# import io
#
#
# def is_number(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         return False
#
#
#
# class SimpleDictStorage(BaseStorage):
#
#     def __init__(self):
#         self.data = {}
#
#     async def close(self):
#         self.data.clear()
#
#     async def wait_closed(self):
#         pass
#
#     async def get_data(self, chat=None, user=None, default=None):
#         key = self.get_key(chat, user)
#         return self.data.get(key, default)
#
#     async def set_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         self.data[key] = data
#
#     async def reset_data(self, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             del self.data[key]
#
#     async def get_state(self, chat=None, user=None, default=None):
#         data = await self.get_data(chat, user, default)
#         if data:
#             return data.get('state', default)
#         return default
#
#     async def set_state(self, state, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key not in self.data:
#             self.data[key] = {}
#         self.data[key]['state'] = state
#
#     async def update_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             self.data[key].update(data)
#         else:
#             self.data[key] = data
#
#     def get_key(self, chat, user):
#         return f"{chat}:{user}"
#
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация MemoryStorage
# storage = SimpleDictStorage()
#
#
# # Инициализация бота и диспетчера с использованием MemoryStorage
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot, storage=storage)
#
#
# # Добавление middleware для логирования
# dp.middleware.setup(LoggingMiddleware())
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
#     'enableRateLimit': True
# })
#
# user_alerts_status = {}
#
#
# # Создание инлайн клавиатуры для меню
# menu = InlineKeyboardMarkup(row_width=2)
# menu.add(InlineKeyboardButton("Balance", callback_data="menu_balance"))
# menu.add(InlineKeyboardButton("Price", callback_data="menu_price"))
# menu.add(InlineKeyboardButton("Trade History", callback_data="menu_tradehistory"))
# menu.add(InlineKeyboardButton("Clear", callback_data="menu_clear"))
# menu.add(InlineKeyboardButton("Set Price Alert", callback_data="set_price_alert"))  # Добавляем инлайн-кнопку
# cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel_action")
# menu.add(InlineKeyboardButton("Activate Alerts", callback_data="activate_alerts"))
# menu.add(InlineKeyboardButton("Deactivate Alerts", callback_data="deactivate_alerts"))
#
#
#
# # Функция для отображения меню после каждого запроса
# async def show_menu_after_request(message: types.Message):
#     await message.answer("Выберите следующую команду из меню:", reply_markup=menu)
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     greeting = (
#         "Привет! Я ваш торговый бот для Binance.\n"
#         "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
#         "Чтобы начать, выберите команду из меню ниже:"
#     )
#     await message.answer(greeting, reply_markup=menu)
#
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     help_text = (
#         "/balance - Показать ваш баланс на Binance.\n"
#         "/price - Показать текущую цену BTC.\n"
#         "/tradehistory - Показать историю ваших торгов.\n"
#         "/clear - 'Очистить' чат.\n"
#         "Выберите команду из меню или введите ее вручную:"
#     )
#     await message.answer(help_text, reply_markup=menu)
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_clear')
# async def clear_chat(callback_query: types.CallbackQuery):
#     await callback_query.message.answer("Чат очищен.")
#     await show_menu_after_request(callback_query.message)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_balance')
# async def get_balance(callback_query: types.CallbackQuery):
#     try:
#         # Типы кошельков на Binance
#         wallet_types = ['spot', 'margin', 'futures']
#
#         async def fetch_wallet_balance(wallet_type):
#             balance = await exchange.fetch_balance({'type': wallet_type})
#             usdt_balance = balance['total'].get('USDT', 0)
#             traded_coins = {coin: amount for coin, amount in balance['total'].items() if coin != 'USDT' and amount > 0}
#             response = [f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹", f"Баланс: {usdt_balance:.2f} USDT"]
#             if traded_coins:
#                 for coin, amount in traded_coins.items():
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     coin_value_usdt = ticker['last'] * amount
#                     percentage = (coin_value_usdt / (coin_value_usdt + usdt_balance)) * 100
#                     response.append(f"Торгуется {coin_value_usdt:.2f} USDT в {coin} ({percentage:.2f}%)")
#             else:
#                 response.append("Не торгуется депозитом данного кошелька.")
#             return response
#
#         responses = await asyncio.gather(*(fetch_wallet_balance(wallet) for wallet in wallet_types))
#
#         # Объединяем все ответы в один список
#         all_responses = ["Ваши балансы:"]
#         for response in responses:
#             all_responses.extend(response)
#
#         await callback_query.message.answer("\n".join(all_responses))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении баланса: {e}")
#         await callback_query.message.answer("Ошибка при получении баланса.")
#     await callback_query.answer()
#
#
# class PriceQuery(StatesGroup):
#     input_coin = State()
#
# async def get_listed_coins():
#     # Здесь можно использовать API, например, CoinMarketCap или Binance, чтобы получить список монет.
#     # Для простоты я буду использовать фиктивный список.
#     return ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC", "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_price')
# async def menu_price_handler(callback_query: types.CallbackQuery):
#     logging.info("Обработчик menu_price_handler вызван.")
#     coins = await get_listed_coins()
#     markup = InlineKeyboardMarkup(row_width=4)
#     for coin in coins:
#         button = InlineKeyboardButton(coin, callback_data=f"price_{coin}")
#         markup.add(button)
#     markup.add(InlineKeyboardButton("Ввести вручную", callback_data="input_manually"))
#     await callback_query.message.answer("Выберите монету или введите её вручную:", reply_markup=markup)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'input_manually', state=None)
# async def ask_for_coin(callback_query: types.CallbackQuery):
#     await PriceQuery.input_coin.set()
#     await callback_query.message.answer("Введите название монеты:")
#     await callback_query.answer()
#
# @dp.message_handler(state=PriceQuery.input_coin)
# async def get_price_for_input(message: types.Message, state: FSMContext):
#     logging.info("Обработчик get_price_for_input вызван.")
#     coin = message.text.upper()
#     coins = await get_listed_coins()  # Получаем список доступных монет
#     if coin not in coins:
#         await message.answer(f"Монета {coin} не найдена. Пожалуйста, введите другую монету.")
#         return
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#
#         # Предоставляем пользователю возможность выбрать временной интервал для графика
#         markup = InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
#         markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
#         markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
#         markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
#         await message.answer("Выберите временной интервал для графика:", reply_markup=markup)
#
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
#     await state.finish()
#
#
#
# # @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# # async def show_coin_price(callback_query: types.CallbackQuery):
# #     coin = callback_query.data.split('_')[1]
# #     try:
# #         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
# #         await callback_query.message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
# #         await show_menu_after_request(callback_query.message)
# #     except Exception as e:
# #         logging.error(f"Ошибка при получении цены: {e}")
# #         await callback_query.message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
# #     await callback_query.answer()
#
# @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# async def show_coin_price(callback_query: types.CallbackQuery):
#     logging.info("Обработчик show_coin_price вызван.")
#     coin = callback_query.data.split('_')[1]
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
#     markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
#     markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
#     markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
#     # ... добавьте другие интервалы по желанию ...
#     await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('interval_'))
# async def show_chart(callback_query: types.CallbackQuery):
#     logging.info("Обработчик show_chart вызван.")
#     interval, coin = callback_query.data.split('_')[1:3]
#
#     try:
#         # Получите данные для графика с учетом выбранного интервала
#         ohlc_data = await exchange.fetch_ohlcv(f'{coin}/USDT', interval)
#         logging.info(f"Получены данные для графика {coin} с интервалом {interval}.")
#
#         # Разделите данные на отдельные списки для времени, открытия, максимума, минимума и закрытия
#         times = [x[0] for x in ohlc_data]
#         opens = [x[1] for x in ohlc_data]
#         highs = [x[2] for x in ohlc_data]
#         lows = [x[3] for x in ohlc_data]
#         closes = [x[4] for x in ohlc_data]
#
#         # Постройте график
#         plt.figure(figsize=(10, 5))
#         plt.plot(times, closes, label=f'{coin} price')
#         plt.title(f'Price of {coin} for the last {interval}')
#         plt.xlabel('Time')
#         plt.ylabel('Price')
#         plt.legend()
#
#         # Добавьте аннотацию с текущей ценой на график
#         last_price = closes[-1]
#         plt.annotate(f'Current price: {last_price}', xy=(times[-1], last_price),
#                      xytext=(times[-1] - 0.5, last_price + 0.5),
#                      arrowprops=dict(facecolor='black', arrowstyle='->'),
#                      horizontalalignment='right')
#
#         # Сохраните график в байтовый поток и отправьте его пользователю
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         await callback_query.message.answer_photo(buf,
#                                                   caption=f'Price chart for {coin} ({interval}). Current price: {last_price} USDT')
#         buf.close()
#
#         # Закройте график, чтобы освободить память
#         plt.close()
#
#     except Exception as e:
#         logging.error(f"Ошибка при построении графика для {coin} с интервалом {interval}: {e}")
#         await callback_query.message.answer(f"Ошибка при построении графика для {coin}. Пожалуйста, попробуйте позже.")
#
#     # После отправки графика, покажем пользователю кнопки для выбора временного интервала снова
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
#     markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
#     markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
#     markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
#     # ... добавьте другие интервалы по желанию ...
#
#     await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
#     await callback_query.answer()
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('chart_'))
# async def handle_chart_request(callback_query: types.CallbackQuery):
#     logging.info("Обработчик handle_chart_request вызван.")
#     coin = callback_query.data.split('_')[1]
#
#     try:
#         # Получите данные для графика с учетом выбранного интервала
#         ohlc_data = await exchange.fetch_ohlcv(f'{coin}/USDT', '1d')  # Пример интервала в 1 день
#         logging.info(f"Получены данные для графика {coin} с интервалом 1d.")
#
#         # Разделите данные на отдельные списки для времени, открытия, максимума, минимума и закрытия
#         times = [x[0] for x in ohlc_data]
#         closes = [x[4] for x in ohlc_data]
#
#         # Постройте график
#         plt.figure(figsize=(10, 5))
#         plt.plot(times, closes, label=f'{coin} price')
#         plt.title(f'Price of {coin} for the last day')
#         plt.xlabel('Time')
#         plt.ylabel('Price')
#         plt.legend()
#
#         # Добавьте аннотацию с текущей ценой на график
#         last_price = closes[-1]
#         plt.annotate(f'Current price: {last_price}', xy=(times[-1], last_price),
#                      xytext=(times[-1] - 0.5, last_price + 0.5),
#                      arrowprops=dict(facecolor='black', arrowstyle='->'),
#                      horizontalalignment='right')
#
#         # Сохраните график в байтовый поток и отправьте его пользователю
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         await callback_query.message.answer_photo(buf,
#                                                   caption=f'Price chart for {coin} (1d). Current price: {last_price} USDT')
#         buf.close()
#
#         # Закройте график, чтобы освободить память
#         plt.close()
#
#     except Exception as e:
#         logging.error(f"Ошибка при построении графика для {coin} с интервалом 1d: {e}")
#         await callback_query.message.answer(f"Ошибка при построении графика для {coin}. Пожалуйста, попробуйте позже.")
#
#     # После отправки графика, покажем пользователю кнопки для выбора временного интервала снова
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
#     markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
#     markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
#     markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
#     # ... добавьте другие интервалы по желанию ...
#
#     await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
#     await callback_query.answer()
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
#
#
#
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_tradehistory')
# async def menu_tradehistory_handler(callback_query: types.CallbackQuery):
#     try:
#         trades = await exchange.fetch_my_trades('BTC/USDT', limit=5)  # последние 5 сделок
#         trade_messages = [f"Сделка {trade['id']}: {trade['amount']} BTC по цене {trade['price']} USDT" for trade in trades]
#         await callback_query.message.answer("\n".join(trade_messages))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении истории торгов: {e}")
#         await callback_query.message.answer("Ошибка при получении истории торгов.")
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
#
# class PriceAlert(StatesGroup):
#     setting_coins = State()
#     setting_prices = State()
#
# @dp.callback_query_handler(lambda c: c.data == 'set_price_alert')
# async def set_price_alert_callback(callback_query: types.CallbackQuery):
#     await callback_query.message.answer("Введите монеты, разделенные запятыми, для которых вы хотите установить уведомление (например, BTC,ETH,ADA):")
#     await PriceAlert.setting_coins.set()
#     await callback_query.answer()
#
#
# @dp.message_handler(commands=['setpricealert'])
# async def set_price_alert_command(message: types.Message):
#     markup = InlineKeyboardMarkup().add(cancel_button)
#     await message.answer(
#         "Введите монеты, разделенные запятыми, для которых вы хотите установить уведомление (например, BTC,ETH,ADA):",
#         reply_markup=markup)
#
#
# @dp.message_handler(state=PriceAlert.setting_coins)
# async def set_alert_coins(message: types.Message, state: FSMContext):
#     coins = [coin.strip().upper() for coin in message.text.split(",")]
#     await state.update_data({"coins": coins})  # Исправленная строка
#     await message.answer(f"Введите пороговые цены для {', '.join(coins)} (например, 50000,3000,2):")
#     await PriceAlert.next()
#
#
# @dp.message_handler(state=PriceAlert.setting_prices)
# async def set_price_alerts(message: types.Message, state: FSMContext):
#     markup = InlineKeyboardMarkup().add(cancel_button)  # Добавляем кнопку отмены
#     user_data = await state.get_data()
#     coins = user_data.get("coins")
#
#     # Проверка ввода пользователя
#     if not all(is_number(price.strip()) for price in message.text.split(",")):
#         await message.answer("Пожалуйста, введите только числовые значения для цен. Попробуйте снова.", reply_markup=markup)
#         return
#
#     prices = [float(price.strip()) for price in message.text.split(",")]
#
#     if len(prices) != len(coins):
#         await message.answer("Количество монет и цен не совпадает. Пожалуйста, попробуйте снова.", reply_markup=markup)
#         return
#
#     # Здесь вы можете сохранить пороговые цены и монеты в базе данных или другом хранилище
#     # Например: save_alerts_to_db(user_id=message.from_user.id, alerts=dict(zip(coins, prices)))
#
#     # Создаем клавиатуру с кнопками активации и деактивации уведомлений
#     markup = InlineKeyboardMarkup(row_width=2)
#     markup.add(InlineKeyboardButton("Activate Alerts", callback_data="activate_alerts"))
#     markup.add(InlineKeyboardButton("Deactivate Alerts", callback_data="deactivate_alerts"))
#     markup.add(cancel_button)
#
#     await message.answer(
#         f"Уведомления установлены для: {', '.join([f'{coin} - {price} USDT' for coin, price in zip(coins, prices)])}. Выберите действие:", reply_markup=markup)
#     await state.finish()
#
#
#
# @dp.callback_query_handler(lambda c: c.data == "cancel_action", state='*')
# async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
#     await state.finish()
#     await callback_query.message.answer("Действие отменено.")
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
#
#
# @dp.message_handler(lambda message: message.text.lower() == 'отмена', state='*')
# async def cancel_text(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is not None:
#         logging.info(f'Cancelling state {current_state}')
#         await state.finish()
#         await message.answer('Действие отменено.')
#     else:
#         await message.answer('Нет активного действия для отмены.')
#
#
# @dp.callback_query_handler(lambda c: c.data == 'activate_alerts')
# async def activate_alerts(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_alerts_status[user_id] = True
#     await callback_query.message.answer("Уведомления активированы.")
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
# @dp.callback_query_handler(lambda c: c.data == 'deactivate_alerts')
# async def deactivate_alerts(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_alerts_status[user_id] = False
#     await callback_query.message.answer("Уведомления деактивированы.")
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
# # Глобальный словарь для хранения уведомлений
# # Ключ - ID пользователя, значение - список словарей с монетой и пороговой ценой
# alerts = {}
#
# async def check_price_alerts():
#     while True:
#         for user_id, user_alerts in alerts.items():
#             for alert in user_alerts:
#                 coin = alert['coin']
#                 threshold_price = alert['price']
#
#                 try:
#                     # Получение текущей цены монеты
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     current_price = ticker['last']
#
#                     # Если текущая цена достигла или превысила порог
#                     if current_price >= threshold_price:
#                         await bot.send_message(user_id, f"Цена {coin} достигла {current_price} USDT!")
#                         user_alerts.remove(alert)  # Удалить уведомление после отправки
#                 except Exception as e:
#                     logging.error(f"Ошибка при проверке цены для {coin}: {e}")
#
#         # Пауза перед следующей проверкой
#         await asyncio.sleep(300)  # Проверка каждые 5 минут
#
# admin_id = 379834541  # Замените на ваш идентификатор пользователя в Telegram
#
# async def on_startup(dp):
#     await bot.send_message(admin_id, "Бот запущен")
#     asyncio.create_task(check_price_alerts())
#
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, on_startup=on_startup, skip_updates=True)





# Улучщил команду помошник
# import os
# import logging
# import asyncio
# from aiogram import Bot, Dispatcher, types
# import ccxt.async_support as ccxt
# from dotenv import load_dotenv
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.dispatcher.storage import BaseStorage, FSMContext
# import matplotlib.pyplot as plt
# import io
#
#
# def is_number(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         return False
#
#
#
# class SimpleDictStorage(BaseStorage):
#
#     def __init__(self):
#         self.data = {}
#
#     async def close(self):
#         self.data.clear()
#
#     async def wait_closed(self):
#         pass
#
#     async def get_data(self, chat=None, user=None, default=None):
#         key = self.get_key(chat, user)
#         return self.data.get(key, default)
#
#     async def set_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         self.data[key] = data
#
#     async def reset_data(self, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             del self.data[key]
#
#     async def get_state(self, chat=None, user=None, default=None):
#         data = await self.get_data(chat, user, default)
#         if data:
#             return data.get('state', default)
#         return default
#
#     async def set_state(self, state, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key not in self.data:
#             self.data[key] = {}
#         self.data[key]['state'] = state
#
#     async def update_data(self, data, chat=None, user=None):
#         key = self.get_key(chat, user)
#         if key in self.data:
#             self.data[key].update(data)
#         else:
#             self.data[key] = data
#
#     def get_key(self, chat, user):
#         return f"{chat}:{user}"
#
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# # Загрузка переменных окружения из файла .env
# load_dotenv()
#
# # Получение переменных окружения
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))
#
# # Инициализация MemoryStorage
# storage = SimpleDictStorage()
#
#
# # Инициализация бота и диспетчера с использованием MemoryStorage
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot, storage=storage)
#
#
# # Добавление middleware для логирования
# dp.middleware.setup(LoggingMiddleware())
#
# # Инициализация подключения к бирже Binance
# exchange = ccxt.binance({
#     'apiKey': BINANCE_API_KEY,
#     'secret': BINANCE_API_SECRET,
#     'enableRateLimit': True
# })
#
# user_alerts_status = {}
#
#
# # Создание инлайн клавиатуры для меню
# menu = InlineKeyboardMarkup(row_width=2)
# menu.add(InlineKeyboardButton("Balance", callback_data="menu_balance"))
# menu.add(InlineKeyboardButton("Price", callback_data="menu_price"))
# menu.add(InlineKeyboardButton("Trade History", callback_data="menu_tradehistory"))
# menu.add(InlineKeyboardButton("Clear", callback_data="menu_clear"))
# menu.add(InlineKeyboardButton("Set Price Alert", callback_data="set_price_alert"))  # Добавляем инлайн-кнопку
# cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel_action")
# menu.add(InlineKeyboardButton("Activate Alerts", callback_data="activate_alerts"))
# menu.add(InlineKeyboardButton("Deactivate Alerts", callback_data="deactivate_alerts"))
#
# admin_id = 379834541  # Замените на ваш идентификатор пользователя в Telegram
#
# async def on_startup(dp):
#     await bot.send_message(admin_id, "Бот запущен")
#     asyncio.create_task(check_price_alerts())
#     # Отправляем приветственное сообщение
#     await start_command(types.Message(chat=types.Chat(id=admin_id), from_user=types.User(id=admin_id)))
#
# # Функция для отображения меню после каждого запроса
# async def show_menu_after_request(message: types.Message):
#     await message.answer("Выберите следующую команду из меню:", reply_markup=menu)
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     greeting = (
#         "Привет! Я ваш торговый бот для Binance.\n"
#         "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
#         "Чтобы начать, выберите команду из меню ниже:"
#     )
#     await message.answer(greeting, reply_markup=menu)
#
#
# @dp.message_handler(commands=['help'])
# async def help_command(message: types.Message):
#     help_text = (
#         "/balance - Показать ваш баланс на Binance.\n"
#         "/price - Показать текущую цену BTC.\n"
#         "/tradehistory - Показать историю ваших торгов.\n"
#         "/clear - 'Очистить' чат.\n"
#         "/setpricealert - Установить уведомление о цене.\n"
#         "/activatealerts - Активировать уведомления.\n"
#         "/deactivatealerts - Деактивировать уведомления.\n"
#         "Выберите команду из меню или введите ее вручную:"
#     )
#     await message.answer(help_text, reply_markup=menu)
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_clear')
# async def clear_chat(callback_query: types.CallbackQuery):
#     await callback_query.message.answer("Чат очищен.")
#     await show_menu_after_request(callback_query.message)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_balance')
# async def get_balance(callback_query: types.CallbackQuery):
#     try:
#         # Типы кошельков на Binance
#         wallet_types = ['spot', 'margin', 'futures']
#
#         async def fetch_wallet_balance(wallet_type):
#             balance = await exchange.fetch_balance({'type': wallet_type})
#             usdt_balance = balance['total'].get('USDT', 0)
#             traded_coins = {coin: amount for coin, amount in balance['total'].items() if coin != 'USDT' and amount > 0}
#             response = [f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹", f"Баланс: {usdt_balance:.2f} USDT"]
#             if traded_coins:
#                 for coin, amount in traded_coins.items():
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     coin_value_usdt = ticker['last'] * amount
#                     percentage = (coin_value_usdt / (coin_value_usdt + usdt_balance)) * 100
#                     response.append(f"Торгуется {coin_value_usdt:.2f} USDT в {coin} ({percentage:.2f}%)")
#             else:
#                 response.append("Не торгуется депозитом данного кошелька.")
#             return response
#
#         responses = await asyncio.gather(*(fetch_wallet_balance(wallet) for wallet in wallet_types))
#
#         # Объединяем все ответы в один список
#         all_responses = ["Ваши балансы:"]
#         for response in responses:
#             all_responses.extend(response)
#
#         await callback_query.message.answer("\n".join(all_responses))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении баланса: {e}")
#         await callback_query.message.answer("Ошибка при получении баланса.")
#     await callback_query.answer()
#
#
# class PriceQuery(StatesGroup):
#     input_coin = State()
#
# async def get_listed_coins():
#     # Здесь можно использовать API, например, CoinMarketCap или Binance, чтобы получить список монет.
#     # Для простоты я буду использовать фиктивный список.
#     return ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC", "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_price')
# async def menu_price_handler(callback_query: types.CallbackQuery):
#     logging.info("Обработчик menu_price_handler вызван.")
#     coins = await get_listed_coins()
#     markup = InlineKeyboardMarkup(row_width=4)
#     for coin in coins:
#         button = InlineKeyboardButton(coin, callback_data=f"price_{coin}")
#         markup.add(button)
#     markup.add(InlineKeyboardButton("Ввести вручную", callback_data="input_manually"))
#     await callback_query.message.answer("Выберите монету или введите её вручную:", reply_markup=markup)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data == 'input_manually', state=None)
# async def ask_for_coin(callback_query: types.CallbackQuery):
#     await PriceQuery.input_coin.set()
#     await callback_query.message.answer("Введите название монеты:")
#     await callback_query.answer()
#
# @dp.message_handler(state=PriceQuery.input_coin)
# async def get_price_for_input(message: types.Message, state: FSMContext):
#     logging.info("Обработчик get_price_for_input вызван.")
#     coin = message.text.upper()
#     coins = await get_listed_coins()  # Получаем список доступных монет
#     if coin not in coins:
#         await message.answer(f"Монета {coin} не найдена. Пожалуйста, введите другую монету.")
#         return
#     try:
#         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#         await message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
#
#         # Предоставляем пользователю возможность выбрать временной интервал для графика
#         markup = InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
#         markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
#         markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
#         markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
#         await message.answer("Выберите временной интервал для графика:", reply_markup=markup)
#
#     except Exception as e:
#         logging.error(f"Ошибка при получении цены: {e}")
#         await message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
#     await state.finish()
#
#
#
# # @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# # async def show_coin_price(callback_query: types.CallbackQuery):
# #     coin = callback_query.data.split('_')[1]
# #     try:
# #         ticker = await exchange.fetch_ticker(f'{coin}/USDT')
# #         await callback_query.message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")
# #         await show_menu_after_request(callback_query.message)
# #     except Exception as e:
# #         logging.error(f"Ошибка при получении цены: {e}")
# #         await callback_query.message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
# #     await callback_query.answer()
#
# @dp.callback_query_handler(lambda c: c.data.startswith('price_'))
# async def show_coin_price(callback_query: types.CallbackQuery):
#     logging.info("Обработчик show_coin_price вызван.")
#     coin = callback_query.data.split('_')[1]
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
#     markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
#     markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
#     markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
#     # ... добавьте другие интервалы по желанию ...
#     await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('interval_'))
# async def show_chart(callback_query: types.CallbackQuery):
#     logging.info("Обработчик show_chart вызван.")
#     interval, coin = callback_query.data.split('_')[1:3]
#
#     try:
#         # Получите данные для графика с учетом выбранного интервала
#         ohlc_data = await exchange.fetch_ohlcv(f'{coin}/USDT', interval)
#         logging.info(f"Получены данные для графика {coin} с интервалом {interval}.")
#
#         # Разделите данные на отдельные списки для времени, открытия, максимума, минимума и закрытия
#         times = [x[0] for x in ohlc_data]
#         opens = [x[1] for x in ohlc_data]
#         highs = [x[2] for x in ohlc_data]
#         lows = [x[3] for x in ohlc_data]
#         closes = [x[4] for x in ohlc_data]
#
#         # Постройте график
#         plt.figure(figsize=(10, 5))
#         plt.plot(times, closes, label=f'{coin} price')
#         plt.title(f'Price of {coin} for the last {interval}')
#         plt.xlabel('Time')
#         plt.ylabel('Price')
#         plt.legend()
#
#         # Добавьте аннотацию с текущей ценой на график
#         last_price = closes[-1]
#         plt.annotate(f'Current price: {last_price}', xy=(times[-1], last_price),
#                      xytext=(times[-1] - 0.5, last_price + 0.5),
#                      arrowprops=dict(facecolor='black', arrowstyle='->'),
#                      horizontalalignment='right')
#
#         # Сохраните график в байтовый поток и отправьте его пользователю
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         await callback_query.message.answer_photo(buf,
#                                                   caption=f'Price chart for {coin} ({interval}). Current price: {last_price} USDT')
#         buf.close()
#
#         # Закройте график, чтобы освободить память
#         plt.close()
#
#     except Exception as e:
#         logging.error(f"Ошибка при построении графика для {coin} с интервалом {interval}: {e}")
#         await callback_query.message.answer(f"Ошибка при построении графика для {coin}. Пожалуйста, попробуйте позже.")
#
#     # После отправки графика, покажем пользователю кнопки для выбора временного интервала снова
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
#     markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
#     markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
#     markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
#     # ... добавьте другие интервалы по желанию ...
#
#     await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
#     await callback_query.answer()
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('chart_'))
# async def handle_chart_request(callback_query: types.CallbackQuery):
#     logging.info("Обработчик handle_chart_request вызван.")
#     coin = callback_query.data.split('_')[1]
#
#     try:
#         # Получите данные для графика с учетом выбранного интервала
#         ohlc_data = await exchange.fetch_ohlcv(f'{coin}/USDT', '1d')  # Пример интервала в 1 день
#         logging.info(f"Получены данные для графика {coin} с интервалом 1d.")
#
#         # Разделите данные на отдельные списки для времени, открытия, максимума, минимума и закрытия
#         times = [x[0] for x in ohlc_data]
#         closes = [x[4] for x in ohlc_data]
#
#         # Постройте график
#         plt.figure(figsize=(10, 5))
#         plt.plot(times, closes, label=f'{coin} price')
#         plt.title(f'Price of {coin} for the last day')
#         plt.xlabel('Time')
#         plt.ylabel('Price')
#         plt.legend()
#
#         # Добавьте аннотацию с текущей ценой на график
#         last_price = closes[-1]
#         plt.annotate(f'Current price: {last_price}', xy=(times[-1], last_price),
#                      xytext=(times[-1] - 0.5, last_price + 0.5),
#                      arrowprops=dict(facecolor='black', arrowstyle='->'),
#                      horizontalalignment='right')
#
#         # Сохраните график в байтовый поток и отправьте его пользователю
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         await callback_query.message.answer_photo(buf,
#                                                   caption=f'Price chart for {coin} (1d). Current price: {last_price} USDT')
#         buf.close()
#
#         # Закройте график, чтобы освободить память
#         plt.close()
#
#     except Exception as e:
#         logging.error(f"Ошибка при построении графика для {coin} с интервалом 1d: {e}")
#         await callback_query.message.answer(f"Ошибка при построении графика для {coin}. Пожалуйста, попробуйте позже.")
#
#     # После отправки графика, покажем пользователю кнопки для выбора временного интервала снова
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
#     markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
#     markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
#     markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
#     # ... добавьте другие интервалы по желанию ...
#
#     await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
#     await callback_query.answer()
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
#
#
#
#
#
# @dp.callback_query_handler(lambda c: c.data == 'menu_tradehistory')
# async def menu_tradehistory_handler(callback_query: types.CallbackQuery):
#     try:
#         trades = await exchange.fetch_my_trades('BTC/USDT', limit=5)  # последние 5 сделок
#         trade_messages = [f"Сделка {trade['id']}: {trade['amount']} BTC по цене {trade['price']} USDT" for trade in trades]
#         await callback_query.message.answer("\n".join(trade_messages))
#         await show_menu_after_request(callback_query.message)
#     except Exception as e:
#         logging.error(f"Ошибка при получении истории торгов: {e}")
#         await callback_query.message.answer("Ошибка при получении истории торгов.")
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
#
# class PriceAlert(StatesGroup):
#     setting_coins = State()
#     setting_prices = State()
#
# @dp.callback_query_handler(lambda c: c.data == 'set_price_alert')
# async def set_price_alert_callback(callback_query: types.CallbackQuery):
#     await callback_query.message.answer("Введите монеты, разделенные запятыми, для которых вы хотите установить уведомление (например, BTC,ETH,ADA):")
#     await PriceAlert.setting_coins.set()
#     await callback_query.answer()
#
#
# @dp.message_handler(commands=['setpricealert'])
# async def set_price_alert_command(message: types.Message):
#     markup = InlineKeyboardMarkup().add(cancel_button)
#     await message.answer(
#         "Введите монеты, разделенные запятыми, для которых вы хотите установить уведомление (например, BTC,ETH,ADA):",
#         reply_markup=markup)
#
#
# @dp.message_handler(state=PriceAlert.setting_coins)
# async def set_alert_coins(message: types.Message, state: FSMContext):
#     coins = [coin.strip().upper() for coin in message.text.split(",")]
#     await state.update_data({"coins": coins})  # Исправленная строка
#     await message.answer(f"Введите пороговые цены для {', '.join(coins)} (например, 50000,3000,2):")
#     await PriceAlert.next()
#
#
# @dp.message_handler(state=PriceAlert.setting_prices)
# async def set_price_alerts(message: types.Message, state: FSMContext):
#     markup = InlineKeyboardMarkup().add(cancel_button)  # Добавляем кнопку отмены
#     user_data = await state.get_data()
#     coins = user_data.get("coins")
#
#     # Проверка ввода пользователя
#     if not all(is_number(price.strip()) for price in message.text.split(",")):
#         await message.answer("Пожалуйста, введите только числовые значения для цен. Попробуйте снова.", reply_markup=markup)
#         return
#
#     prices = [float(price.strip()) for price in message.text.split(",")]
#
#     if len(prices) != len(coins):
#         await message.answer("Количество монет и цен не совпадает. Пожалуйста, попробуйте снова.", reply_markup=markup)
#         return
#
#     # Здесь вы можете сохранить пороговые цены и монеты в базе данных или другом хранилище
#     # Например: save_alerts_to_db(user_id=message.from_user.id, alerts=dict(zip(coins, prices)))
#
#     # Создаем клавиатуру с кнопками активации и деактивации уведомлений
#     markup = InlineKeyboardMarkup(row_width=2)
#     markup.add(InlineKeyboardButton("Activate Alerts", callback_data="activate_alerts"))
#     markup.add(InlineKeyboardButton("Deactivate Alerts", callback_data="deactivate_alerts"))
#     markup.add(cancel_button)
#
#     await message.answer(
#         f"Уведомления установлены для: {', '.join([f'{coin} - {price} USDT' for coin, price in zip(coins, prices)])}. Выберите действие:", reply_markup=markup)
#     await state.finish()
#
#
#
# @dp.callback_query_handler(lambda c: c.data == "cancel_action", state='*')
# async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
#     await state.finish()
#     await callback_query.message.answer("Действие отменено.")
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
#
#
# @dp.message_handler(lambda message: message.text.lower() == 'отмена', state='*')
# async def cancel_text(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is not None:
#         logging.info(f'Cancelling state {current_state}')
#         await state.finish()
#         await message.answer('Действие отменено.')
#     else:
#         await message.answer('Нет активного действия для отмены.')
#
#
# @dp.callback_query_handler(lambda c: c.data == 'activate_alerts')
# async def activate_alerts(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_alerts_status[user_id] = True
#     await callback_query.message.answer("Уведомления активированы.")
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
# @dp.callback_query_handler(lambda c: c.data == 'deactivate_alerts')
# async def deactivate_alerts(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_alerts_status[user_id] = False
#     await callback_query.message.answer("Уведомления деактивированы.")
#     # После отправки графика, отправляем пользователю основное меню
#     await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
#     await callback_query.answer()
#
# # Глобальный словарь для хранения уведомлений
# # Ключ - ID пользователя, значение - список словарей с монетой и пороговой ценой
# alerts = {}
#
# async def check_price_alerts():
#     while True:
#         for user_id, user_alerts in alerts.items():
#             for alert in user_alerts:
#                 coin = alert['coin']
#                 threshold_price = alert['price']
#
#                 try:
#                     # Получение текущей цены монеты
#                     ticker = await exchange.fetch_ticker(f'{coin}/USDT')
#                     current_price = ticker['last']
#
#                     # Если текущая цена достигла или превысила порог
#                     if current_price >= threshold_price:
#                         await bot.send_message(user_id, f"Цена {coin} достигла {current_price} USDT!")
#                         user_alerts.remove(alert)  # Удалить уведомление после отправки
#                 except Exception as e:
#                     logging.error(f"Ошибка при проверке цены для {coin}: {e}")
#
#         # Пауза перед следующей проверкой
#         await asyncio.sleep(300)  # Проверка каждые 5 минут
#
#
#
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, on_startup=on_startup, skip_updates=True)




