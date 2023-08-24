import os
import logging
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
import ccxt.async_support as ccxt
from dotenv import load_dotenv
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.storage import BaseStorage, FSMContext
import matplotlib.pyplot as plt
import io
import pandas as pd
import numpy as np


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



class SimpleDictStorage(BaseStorage):

    def __init__(self):
        self.data = {}

    async def close(self):
        self.data.clear()

    async def wait_closed(self):
        pass

    async def get_data(self, chat=None, user=None, default=None):
        key = self.get_key(chat, user)
        return self.data.get(key, default)

    async def set_data(self, data, chat=None, user=None):
        key = self.get_key(chat, user)
        self.data[key] = data

    async def reset_data(self, chat=None, user=None):
        key = self.get_key(chat, user)
        if key in self.data:
            del self.data[key]

    async def get_state(self, chat=None, user=None, default=None):
        data = await self.get_data(chat, user, default)
        if data:
            return data.get('state', default)
        return default

    async def set_state(self, state, chat=None, user=None):
        key = self.get_key(chat, user)
        if key not in self.data:
            self.data[key] = {}
        self.data[key]['state'] = state

    async def update_data(self, data, chat=None, user=None):
        key = self.get_key(chat, user)
        if key in self.data:
            self.data[key].update(data)
        else:
            self.data[key] = data

    def get_key(self, chat, user):
        return f"{chat}:{user}"





# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение переменных окружения
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID'))

# Инициализация MemoryStorage
storage = SimpleDictStorage()


# Инициализация бота и диспетчера с использованием MemoryStorage
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


# Добавление middleware для логирования
dp.middleware.setup(LoggingMiddleware())

# Инициализация подключения к бирже Binance
exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_API_SECRET,
    'enableRateLimit': True
})

user_alerts_status = {}


# Создание инлайн клавиатуры для меню
menu = InlineKeyboardMarkup(row_width=2)
menu.add(InlineKeyboardButton("Balance", callback_data="menu_balance"))
menu.add(InlineKeyboardButton("Price", callback_data="menu_price"))
menu.add(InlineKeyboardButton("Trade History", callback_data="menu_tradehistory"))
menu.add(InlineKeyboardButton("Clear", callback_data="menu_clear"))
menu.add(InlineKeyboardButton("Set Price Alert", callback_data="set_price_alert"))  # Добавляем инлайн-кнопку
cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel_action")
menu.add(InlineKeyboardButton("Activate Alerts", callback_data="activate_alerts"))
menu.add(InlineKeyboardButton("Deactivate Alerts", callback_data="deactivate_alerts"))
menu.add(InlineKeyboardButton("Market Analysis", callback_data="market_analysis"))


admin_id = 379834541  # Замените на ваш идентификатор пользователя в Telegram

async def on_startup(dp):
    await bot.send_message(admin_id, "Бот запущен")
    asyncio.create_task(check_price_alerts())
    # Отправляем приветственное сообщение
    await start_command(types.Message(chat=types.Chat(id=admin_id), from_user=types.User(id=admin_id)))

# Функция для отображения меню после каждого запроса
async def show_menu_after_request(message: types.Message):
    await message.answer("Выберите следующую команду из меню:", reply_markup=menu)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    greeting = (
        "Привет! Я ваш торговый бот для Binance.\n"
        "Используйте команду /help, чтобы узнать больше о доступных командах.\n"
        "Чтобы начать, выберите команду из меню ниже:"
    )
    await message.answer(greeting, reply_markup=menu)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    help_text = (
        "/balance - Показать ваш баланс на Binance.\n"
        "/price - Показать текущую цену BTC.\n"
        "/tradehistory - Показать историю ваших торгов.\n"
        "/clear - 'Очистить' чат.\n"
        "/setpricealert - Установить уведомление о цене.\n"
        "/activatealerts - Активировать уведомления.\n"
        "/deactivatealerts - Деактивировать уведомления.\n"
        "Выберите команду из меню или введите ее вручную:"
    )
    await message.answer(help_text, reply_markup=menu)


@dp.callback_query_handler(lambda c: c.data == 'menu_clear')
async def clear_chat(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Чат очищен.")
    await show_menu_after_request(callback_query.message)
    await callback_query.answer()

class MarketAnalysisState(StatesGroup):
    CoinInput = State()  # Expecting a coin name as input

class MarketAnalysis:
    def __init__(self, bot, exchange):
        self.bot = bot
        self.exchange = exchange

    async def handle_market_analysis(self, callback_query: types.CallbackQuery):
        analysis_result = await self.perform_market_analysis()
        await self.bot.send_message(callback_query.from_user.id, analysis_result)

        # Offering the user to analyze a specific coin or return to the main menu
        markup = InlineKeyboardMarkup(row_width=2)
        item1 = InlineKeyboardButton("Анализировать конкретную монету", callback_data="analyze_specific_coin")
        item2 = InlineKeyboardButton("Вернуться в главное меню", callback_data="return_to_menu")
        markup.add(item1, item2)

        await self.bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=markup)

    async def ask_for_coin(self, callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.answer("Введите название монеты для анализа:")
        await MarketAnalysisState.CoinInput.set()

    async def analyze_specific_coin(self, message: types.Message, state: FSMContext):
        coin_name = message.text.upper()  # Assuming coin names are in uppercase
        # Using the existing logic to analyze the coin
        best_timeframe = "1d"  # This can be changed based on your preference
        score, recommendation = await self.analyze_coin(coin_name, best_timeframe)

        await self.bot.send_message(message.from_user.id, f"Рекомендация для {coin_name}: {recommendation}")
        await state.finish()  # Resetting the state
        await self.bot.send_message(message.from_user.id, "Выберите следующую команду из меню:", reply_markup=menu)

    async def return_to_main_menu(self, callback_query: types.CallbackQuery):
        await self.bot.send_message(callback_query.from_user.id, "Выберите следующую команду из меню:", reply_markup=menu)


    async def perform_market_analysis(self):
        coins = ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC",
                 "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]
        timeframes = ["5m", "15m", "30m", "1h", "4h", "1d"]

        best_coin = None
        best_timeframe = None
        best_score = -float('inf')
        best_recommendation = None

        for coin in coins:
            for timeframe in timeframes:
                score, recommendation = await self.analyze_coin(coin, timeframe)
                if score > best_score:
                    best_score = score
                    best_coin = coin
                    best_timeframe = timeframe
                    best_recommendation = recommendation

        # Compute the volatility, signal_strength, rsi, and macd values based on your data
        volatility = 0.1  # Replace with actual calculation
        signal_strength = 0.5  # Replace with actual calculation
        rsi = 30  # Replace with actual calculation
        macd = -0.02  # Replace with actual calculation

        holding_duration = self.get_holding_duration(
            volatility=volatility, signal_strength=signal_strength,
            rsi=rsi, macd=macd, recommendation=best_recommendation
        )
        return f"Лучшая монета для торговли: {best_coin} на таймфрейме {best_timeframe}. Рекомендация: {best_recommendation}. {holding_duration}"

    def get_holding_duration(self, recommendation, volatility, signal_strength, rsi, macd):
        """
        Возвращает рекомендуемую продолжительность удержания монеты на основе рекомендации, волатильности рынка,
        силы сигнала, RSI и MACD.

        :param recommendation: Строка, указывающая рекомендацию ("Купить", "Продать", "Держать").
        :param volatility: Float, представляющий волатильность рынка.
        :param signal_strength: Float, представляющий силу сигнала покупки/продажи.
        :param rsi: Float, представляющий индекс относительной силы (RSI).
        :param macd: Float, представляющий индикатор схождения/расхождения скользящих средних (MACD).
        :return: Строка с рекомендацией по продолжительности удержания.
        """
        if recommendation == "Купить":
            if volatility > 0.05 or signal_strength > 0.8:
                return "Рекомендуемая продолжительность удержания: 12 часов или до следующего сигнала."
            elif rsi < 30:
                return "Рекомендуемая продолжительность удержания: 48 часов или до следующего сигнала."
            elif macd > 0:
                return "Рекомендуемая продолжительность удержания: 36 часов или до следующего сигнала."
            else:
                return "Рекомендуемая продолжительность удержания: 24 часа или до следующего сигнала."
        elif recommendation == "Продать":
            return "Рассмотрите возможность продажи в течение следующих 12 часов."
        else:  # Держать
            if rsi < 30 or rsi > 70:
                return "Проведите повторную оценку через 12 часов."
            elif macd < 0:
                return "Проведите повторную оценку через 18 часов."
            else:
                return "Проведите повторную оценку через 24 часа."

    async def analyze_coin(self, coin, timeframe):
        """Анализирует монету на заданном таймфрейме и возвращает рекомендацию и оценку."""
        ohlc_data = await self.exchange.fetch_ohlcv(f'{coin}/USDT', timeframe)
        if not ohlc_data:
            return 0, "Нет данных"
        recommendation = self.analyze_data(ohlc_data)

        score = 0
        if recommendation == "Купить":
            score = 1
        elif recommendation == "Продать":
            score = -1

        return score, recommendation

    def compute_ema(self, data, span=14):
        """
        Вычисляет экспоненциальное скользящее среднее (EMA) для данных.

        :param data: Ряд данных для вычисления EMA.
        :param span: Период для EMA.
        :return: Ряд EMA.
        """
        return data.ewm(span=span, adjust=False).mean()

    def compute_rsi(self, data, window=14):
        """
        Вычисляет индекс относительной силы (RSI) для данных.

        :param data: Ряд данных для вычисления RSI.
        :param window: Период для RSI.
        :return: Последнее значение RSI.
        """
        delta = data.diff()
        gain = delta.where(delta > 0, 0).fillna(0)
        loss = -delta.where(delta < 0, 0).fillna(0)

        avg_gain = self.compute_ema(gain, span=window)
        avg_loss = self.compute_ema(loss, span=window)

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1]

    def compute_macd(self, data, short_window=12, long_window=26, signal_window=9):
        """
        Вычисляет индикатор MACD для данных.

        :param data: Ряд данных для вычисления MACD.
        :param short_window: Короткий период для MACD.
        :param long_window: Длинный период для MACD.
        :param signal_window: Период сигнала для MACD.
        :return: Последнее значение гистограммы MACD.
        """
        short_ema = self.compute_ema(data, short_window)
        long_ema = self.compute_ema(data, long_window)
        macd_line = short_ema - long_ema
        signal_line = self.compute_ema(macd_line, signal_window)
        histogram = macd_line - signal_line

        return histogram.iloc[-1]

    def analyze_data(self, data):
        """
        Анализирует данные и предоставляет рекомендацию на основе RSI и MACD.

        :param data: Данные OHLC для анализа.
        :return: Строка с рекомендацией.
        """
        closes = pd.Series([item[4] for item in data])

        rsi = self.compute_rsi(closes)
        macd_histogram = self.compute_macd(closes)

        if rsi < 30 and macd_histogram > 0:
            return "Купить"
        elif rsi > 70 and macd_histogram < 0:
            return "Продать"
        else:
            return "Держать"

    def compute_bollinger_bands(self, data, window=20, num_std=2, plot=False):
        """
        Вычисляет Bollinger Bands для данных цен.
        Parameters:
        - data (pd.Series): Серия данных цен закрытия.
        - window (int): Размер окна для скользящей средней.
        - num_std (int): Количество стандартных отклонений для верхней и нижней ленты.
        - plot (bool): Если True, отображает график.
        Returns:
        - tuple: Верхняя лента, средняя лента (SMA), нижняя лента.
        """
        sma = data.rolling(window=window).mean()
        rolling_std = data.rolling(window=window).std()
        upper_band = sma + (rolling_std * num_std)
        lower_band = sma - (rolling_std * num_std)
        if plot:
            plt.figure(figsize=(10, 6))
            data.plot(label='Close Price')
            upper_band.plot(label=f'Upper Band ({num_std} STD)', linestyle='--')
            lower_band.plot(label=f'Lower Band ({num_std} STD)', linestyle='--')
            sma.plot(label=f'SMA-{window}')
            plt.title('Bollinger Bands')
            plt.legend()
            plt.show()
        return upper_band, sma, lower_band

    def compute_stochastic_oscillator(self, data, window=14, smooth_window=3, plot=False):
        """
        Вычисляет Stochastic Oscillator для данных цен.
        Parameters:
        - data (pd.DataFrame): DataFrame с колонками 'Close', 'High' и 'Low'.
        - window (int): Размер окна для вычисления.
        - smooth_window (int): Размер окна для сглаживания %K для вычисления %D.
        - plot (bool): Если True, отображает график.
        Returns:
        - tuple: %K, %D.
        """
        low_min = data['Low'].rolling(window=window).min()
        high_max = data['High'].rolling(window=window).max()
        k_percent = 100 * ((data['Close'] - low_min) / (high_max - low_min))
        d_percent = k_percent.rolling(window=smooth_window).mean()
        if plot:
            plt.figure(figsize=(10, 6))
            k_percent.plot(label='%K line')
            d_percent.plot(label='%D line', linestyle='--')
            plt.title('Stochastic Oscillator')
            plt.legend()
            plt.show()
        return k_percent, d_percent


    def combined_strategy(self, data, window_size=20, rsi_thresholds=(30, 70), macd_threshold=0, plot=False):
        # Проверяем, есть ли достаточно данных для расчета индикаторов
        if len(data) < window_size:
            return {"status": "error", "message": "Недостаточно данных"}

        # Рассчитываем индикаторы MACD, RSI и Bollinger Bands
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()

        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        sma = data['Close'].rolling(window=window_size).mean()
        std_dev = data['Close'].rolling(window=window_size).std()
        upper = sma + (std_dev * 2)
        lower = sma - (std_dev * 2)

        # Определяем сигналы для покупки и продажи на основе индикаторов
        buy_signal = (macd > signal + macd_threshold) & (rsi < rsi_thresholds[0]) & (data['Close'] < lower)
        sell_signal = (macd < signal - macd_threshold) & (rsi > rsi_thresholds[1]) & (data['Close'] > upper)

        # Возвращаем результаты анализа в виде словаря
        result = {
            "status": "success",
            "recommendation": "Купить" if buy_signal.iloc[-1] else "Продать" if sell_signal.iloc[-1] else "Держать",
            "indicators": {
                "MACD": "Покупка" if macd.iloc[-1] > signal.iloc[-1] + macd_threshold else "Продажа",
                "RSI": "Покупка" if rsi.iloc[-1] < rsi_thresholds[0] else "Продажа" if rsi.iloc[-1] > rsi_thresholds[
                    1] else "Нейтрально",
                "Bollinger Bands": "Покупка" if data['Close'].iloc[-1] < lower.iloc[-1] else "Продажа" if
                data['Close'].iloc[-1] > upper.iloc[-1] else "Нейтрально"
            }
        }

        # Построим графики с индикаторами и сигналами для покупки и продажи, если параметр plot установлен в True
        if plot:
            fig, ax = plt.subplots(3, 1, figsize=(12, 8))
            ax[0].plot(data['Close'], label='Close Price')
            ax[0].plot(upper, label='Upper Bollinger Band', linestyle='--')
            ax[0].plot(lower, label='Lower Bollinger Band', linestyle='--')
            ax[0].scatter(data.index[buy_signal], data['Close'][buy_signal], color='green', label='Buy Signal',
                          marker='^')
            ax[0].scatter(data.index[sell_signal], data['Close'][sell_signal], color='red', label='Sell Signal',
                          marker='v')
            ax[0].legend()

            ax[1].plot(macd, label='MACD')
            ax[1].plot(signal, label='Signal Line')
            ax[1].legend()

            ax[2].plot(rsi, label='RSI')
            ax[2].axhline(y=rsi_thresholds[0], color='green', linestyle='--')
            ax[2].axhline(y=rsi_thresholds[1], color='red', linestyle='--')
            ax[2].legend()

            plt.show()

        return result

    def adaptive_timeframes(self, data):
        # Вычисляем историческую волатильность (стандартное отклонение цен закрытия)
        historical_volatility = data['Close'].std()

        # Вычисляем текущую волатильность (разница между максимальной и минимальной ценой за последние N периодов)
        current_volatility = data['High'].rolling(window=10).max() - data['Low'].rolling(window=10).min()

        # Вычисляем относительную волатильность (отношение текущей волатильности к исторической)
        relative_volatility = current_volatility / historical_volatility

        # Вычисляем средний объем торгов за последние N периодов
        average_volume = data['Volume'].rolling(window=10).mean()

        # Вычисляем ликвидность (средний объем торгов, умноженный на среднюю цену закрытия)
        liquidity = average_volume * data['Close'].rolling(window=10).mean()

        # Вычисляем тренд (направление движения цен)
        trend = np.sign(data['Close'].diff().rolling(window=10).mean())

        # Определяем таймфрейм на основе относительной волатильности, объема торгов, ликвидности и тренда
        if relative_volatility < 0.5 and average_volume < 1000000 and liquidity < 1000000 and trend == 1:
            return '1m'
        elif relative_volatility < 1 and average_volume < 2000000 and liquidity < 2000000 and trend == 1:
            return '5m'
        elif relative_volatility < 2 and average_volume < 3000000 and liquidity < 3000000 and trend == -1:
            return '15m'
        elif relative_volatility < 4 and average_volume < 4000000 and liquidity < 4000000 and trend == -1:
            return '1h'
        elif relative_volatility < 8 and average_volume < 5000000 and liquidity < 5000000 and trend == 1:
            return '4h'
        else:
            return '1d'

    # Обучение с подкреплением
    def reinforcement_learning(self, data, n_episodes=1000):
        n_states = 10
        n_actions = 3  # Купить, продать, держать

        Q = np.zeros((n_states, n_actions))

        alpha = 0.1
        gamma = 0.99
        epsilon = 0.1

        for episode in range(n_episodes):
            for i in range(1, len(data) - 1):
                state = self.get_state(data, i - 1)
                action = self.choose_action(Q, state, epsilon)
                reward = self.get_reward(data, i, action)
                next_state = self.get_state(data, i)
                Q[state, action] = Q[state, action] + alpha * (
                            reward + gamma * np.max(Q[next_state, :]) - Q[state, action])

        return Q

    def choose_action(self, Q, state, epsilon):
        if np.random.uniform(0, 1) < epsilon:
            return np.random.choice(3)
        else:
            return np.argmax(Q[state, :])

    def get_state(self, data, index):
        return int(np.digitize(data['Close'][index], np.linspace(data['Close'].min(), data['Close'].max(), 10)))

    def get_reward(self, data, index, action):
        if action == 0:
            return data['Close'][index + 1] - data['Close'][index]
        elif action == 1:
            return data['Close'][index] - data['Close'][index + 1]
        else:
            return 0

    def get_recommendation(self, data, Q):
        state = self.get_state(data, len(data) - 1)
        action = np.argmax(Q[state, :])
        if action == 0:
            return "Купить"
        elif action == 1:
            return "Продать"
        else:
            return "Держать"

    def backtesting(self, strategy, historical_data, initial_balance=100000, commission=0.001, trade_size=100,
                    stop_loss=0.1, take_profit=0.2):
        # Проверяем, есть ли достаточно данных для бэктестинга
        if len(historical_data) < 2:
            return {"status": "error", "message": "Недостаточно данных"}

        # Создаем копию исторических данных
        data = historical_data.copy()

        # Применяем стратегию к данным
        strategy_results = strategy(data)

        # Создаем столбцы для хранения информации о покупках и продажах
        data['Buy'] = 0
        data['Sell'] = 0
        data['Position'] = None

        # Инициализируем переменные для хранения информации о позиции и балансе
        position = None
        balance = initial_balance
        entry_price = None

        # Проходим по данным и выполняем торговлю на основе сигналов стратегии
        for i in range(1, len(data)):
            if strategy_results['Buy'][i] == 1 and position is None:
                data['Position'][i] = 'Buy'
                position = 'Buy'
                entry_price = data['Close'][i]
                balance -= entry_price * trade_size * (1 + commission)
            elif strategy_results['Sell'][i] == 1 and position == 'Buy':
                data['Position'][i] = 'Sell'
                position = None
                balance += data['Close'][i] * trade_size * (1 - commission)
            elif position == 'Buy':
                if data['Close'][i] <= entry_price * (1 - stop_loss):
                    data['Position'][i] = 'Sell'
                    position = None
                    balance += data['Close'][i] * trade_size * (1 - commission)
                elif data['Close'][i] >= entry_price * (1 + take_profit):
                    data['Position'][i] = 'Sell'
                    position = None
                    balance += data['Close'][i] * trade_size * (1 - commission)

        # Рассчитываем итоговую прибыль
        profit = balance - initial_balance

        # Возвращаем результаты бэктестинга
        return {
            "status": "success",
            "profit": profit,
            "trades": data[['Close', 'Buy', 'Sell', 'Position']]
        }

    def risk_management(self, recommendation, account_balance, risk_tolerance=0.02):
        position_size = account_balance * risk_tolerance
        adjusted_position_size = position_size * recommendation
        return min(adjusted_position_size, account_balance)

    def analysis_frequency(self, data, threshold_low=0.01, threshold_high=0.05):
        volatility = data['Close'].std()
        if volatility < threshold_low:
            return 'daily'
        elif volatility < threshold_high:
            return 'hourly'
        else:
            return 'minute'

    # Пользовательский интерфейс
    def generate_visual_report(self, data, indicators=['SMA', 'EMA']):
        plt.figure(figsize=(12, 6))
        plt.plot(data['Close'], label='Close Price')
        for indicator in indicators:
            if indicator in data.columns:
                plt.plot(data[indicator], label=indicator)
        plt.legend()
        plt.title('Market Analysis Report')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

    # Интеграция с новостными источниками
    def integrate_news_sources(self):
        # TODO: Реализуйте интеграцию с новостными источниками для лучшего понимания рыночных условий
        pass

    # Уведомления
    def send_notifications(self, event):
        # TODO: Реализуйте метод для отправки уведомлений пользователю
        pass


# Создайте экземпляр класса
market_analyzer = MarketAnalysis(bot, exchange)

# Определите обработчики
@dp.callback_query_handler(lambda c: c.data == "market_analysis", state="*")
async def market_analysis_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await market_analyzer.handle_market_analysis(callback_query)

@dp.callback_query_handler(lambda c: c.data == "analyze_specific_coin", state="*")
async def analyze_specific_coin_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await market_analyzer.ask_for_coin(callback_query, state)

@dp.message_handler(state=MarketAnalysisState.CoinInput)
async def coin_input_handler(message: types.Message, state: FSMContext):
    await market_analyzer.analyze_specific_coin(message, state)

@dp.callback_query_handler(lambda c: c.data == "return_to_menu", state="*")
async def return_to_menu_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await market_analyzer.return_to_main_menu(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'menu_balance')
async def get_balance(callback_query: types.CallbackQuery):
    try:
        # Типы кошельков на Binance
        wallet_types = ['spot', 'margin', 'futures']

        async def fetch_wallet_balance(wallet_type):
            balance = await exchange.fetch_balance({'type': wallet_type})
            usdt_balance = balance['total'].get('USDT', 0)
            traded_coins = {coin: amount for coin, amount in balance['total'].items() if coin != 'USDT' and amount > 0}
            response = [f"\n🔹 Кошелек {wallet_type.capitalize()} 🔹", f"Баланс: {usdt_balance:.2f} USDT"]
            if traded_coins:
                for coin, amount in traded_coins.items():
                    ticker = await exchange.fetch_ticker(f'{coin}/USDT')
                    coin_value_usdt = ticker['last'] * amount
                    percentage = (coin_value_usdt / (coin_value_usdt + usdt_balance)) * 100
                    response.append(f"Торгуется {coin_value_usdt:.2f} USDT в {coin} ({percentage:.2f}%)")
            else:
                response.append("Не торгуется депозитом данного кошелька.")
            return response

        responses = await asyncio.gather(*(fetch_wallet_balance(wallet) for wallet in wallet_types))

        # Объединяем все ответы в один список
        all_responses = ["Ваши балансы:"]
        for response in responses:
            all_responses.extend(response)

        await callback_query.message.answer("\n".join(all_responses))
        await show_menu_after_request(callback_query.message)
    except Exception as e:
        logging.error(f"Ошибка при получении баланса: {e}")
        await callback_query.message.answer("Ошибка при получении баланса.")
    await callback_query.answer()


class PriceQuery(StatesGroup):
    input_coin = State()

async def get_listed_coins():
    # Здесь можно использовать API, например, CoinMarketCap или Binance, чтобы получить список монет.
    # Для простоты я буду использовать фиктивный список.
    return ["BTC", "ETH", "BNB", "ADA", "DOGE", "XRP", "DOT", "UNI", "BCH", "LTC", "LINK", "MATIC", "XLM", "ETC", "THETA", "VET", "TRX", "FIL", "XMR", "EOS"]

@dp.callback_query_handler(lambda c: c.data == 'menu_price')
async def menu_price_handler(callback_query: types.CallbackQuery):
    logging.info("Обработчик menu_price_handler вызван.")
    coins = await get_listed_coins()
    markup = InlineKeyboardMarkup(row_width=4)
    for coin in coins:
        button = InlineKeyboardButton(coin, callback_data=f"price_{coin}")
        markup.add(button)
    markup.add(InlineKeyboardButton("Ввести вручную", callback_data="input_manually"))
    await callback_query.message.answer("Выберите монету или введите её вручную:", reply_markup=markup)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'input_manually', state=None)
async def ask_for_coin(callback_query: types.CallbackQuery):
    await PriceQuery.input_coin.set()
    await callback_query.message.answer("Введите название монеты:")
    await callback_query.answer()

@dp.message_handler(state=PriceQuery.input_coin)
async def get_price_for_input(message: types.Message, state: FSMContext):
    logging.info("Обработчик get_price_for_input вызван.")
    coin = message.text.upper()
    coins = await get_listed_coins()  # Получаем список доступных монет
    if coin not in coins:
        await message.answer(f"Монета {coin} не найдена. Пожалуйста, введите другую монету.")
        return
    try:
        ticker = await exchange.fetch_ticker(f'{coin}/USDT')
        await message.answer(f"Текущая цена {coin} равна {ticker['last']} USDT")

        # Предоставляем пользователю возможность выбрать временной интервал для графика
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
        markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
        markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
        markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
        await message.answer("Выберите временной интервал для графика:", reply_markup=markup)

    except Exception as e:
        logging.error(f"Ошибка при получении цены: {e}")
        await message.answer(f"Ошибка при получении цены для {coin}. Пожалуйста, попробуйте позже.")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('price_'))
async def show_coin_price(callback_query: types.CallbackQuery):
    logging.info("Обработчик show_coin_price вызван.")
    coin = callback_query.data.split('_')[1]
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
    markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
    markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
    markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
    # ... добавьте другие интервалы по желанию ...
    await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('interval_'))
async def show_chart(callback_query: types.CallbackQuery):
    logging.info("Обработчик show_chart вызван.")
    interval, coin = callback_query.data.split('_')[1:3]

    try:
        # Получите данные для графика с учетом выбранного интервала
        ohlc_data = await exchange.fetch_ohlcv(f'{coin}/USDT', interval)
        logging.info(f"Получены данные для графика {coin} с интервалом {interval}.")

        # Разделите данные на отдельные списки для времени, открытия, максимума, минимума и закрытия
        times = [x[0] for x in ohlc_data]
        opens = [x[1] for x in ohlc_data]
        highs = [x[2] for x in ohlc_data]
        lows = [x[3] for x in ohlc_data]
        closes = [x[4] for x in ohlc_data]

        # Постройте график
        plt.figure(figsize=(10, 5))
        plt.plot(times, closes, label=f'{coin} price')
        plt.title(f'Price of {coin} for the last {interval}')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()

        # Добавьте аннотацию с текущей ценой на график
        last_price = closes[-1]
        plt.annotate(f'Current price: {last_price}', xy=(times[-1], last_price),
                     xytext=(times[-1] - 0.5, last_price + 0.5),
                     arrowprops=dict(facecolor='black', arrowstyle='->'),
                     horizontalalignment='right')

        # Сохраните график в байтовый поток и отправьте его пользователю
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        await callback_query.message.answer_photo(buf,
                                                  caption=f'Price chart for {coin} ({interval}). Current price: {last_price} USDT')
        buf.close()

        # Закройте график, чтобы освободить память
        plt.close()

    except Exception as e:
        logging.error(f"Ошибка при построении графика для {coin} с интервалом {interval}: {e}")
        await callback_query.message.answer(f"Ошибка при построении графика для {coin}. Пожалуйста, попробуйте позже.")

    # После отправки графика, покажем пользователю кнопки для выбора временного интервала снова
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
    markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
    markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
    markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
    # ... добавьте другие интервалы по желанию ...

    await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
    await callback_query.answer()
    # После отправки графика, отправляем пользователю основное меню
    await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
    await callback_query.answer()



@dp.callback_query_handler(lambda c: c.data.startswith('chart_'))
async def handle_chart_request(callback_query: types.CallbackQuery):
    logging.info("Обработчик handle_chart_request вызван.")
    coin = callback_query.data.split('_')[1]

    try:
        # Получите данные для графика с учетом выбранного интервала
        ohlc_data = await exchange.fetch_ohlcv(f'{coin}/USDT', '1d')  # Пример интервала в 1 день
        logging.info(f"Получены данные для графика {coin} с интервалом 1d.")

        # Разделите данные на отдельные списки для времени, открытия, максимума, минимума и закрытия
        times = [x[0] for x in ohlc_data]
        closes = [x[4] for x in ohlc_data]

        # Постройте график
        plt.figure(figsize=(10, 5))
        plt.plot(times, closes, label=f'{coin} price')
        plt.title(f'Price of {coin} for the last day')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()

        # Добавьте аннотацию с текущей ценой на график
        last_price = closes[-1]
        plt.annotate(f'Current price: {last_price}', xy=(times[-1], last_price),
                     xytext=(times[-1] - 0.5, last_price + 0.5),
                     arrowprops=dict(facecolor='black', arrowstyle='->'),
                     horizontalalignment='right')

        # Сохраните график в байтовый поток и отправьте его пользователю
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        await callback_query.message.answer_photo(buf,
                                                  caption=f'Price chart for {coin} (1d). Current price: {last_price} USDT')
        buf.close()

        # Закройте график, чтобы освободить память
        plt.close()

    except Exception as e:
        logging.error(f"Ошибка при построении графика для {coin} с интервалом 1d: {e}")
        await callback_query.message.answer(f"Ошибка при построении графика для {coin}. Пожалуйста, попробуйте позже.")

    # После отправки графика, покажем пользователю кнопки для выбора временного интервала снова
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Показать график", callback_data=f"chart_{coin}"))
    markup.add(InlineKeyboardButton("1 час", callback_data=f"interval_1h_{coin}"))
    markup.add(InlineKeyboardButton("1 день", callback_data=f"interval_1d_{coin}"))
    markup.add(InlineKeyboardButton("1 неделя", callback_data=f"interval_1w_{coin}"))
    # ... добавьте другие интервалы по желанию ...

    await callback_query.message.answer("Выберите временной интервал для графика:", reply_markup=markup)
    await callback_query.answer()
    # После отправки графика, отправляем пользователю основное меню
    await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
    await callback_query.answer()






@dp.callback_query_handler(lambda c: c.data == 'menu_tradehistory')
async def menu_tradehistory_handler(callback_query: types.CallbackQuery):
    try:
        trades = await exchange.fetch_my_trades('BTC/USDT', limit=5)  # последние 5 сделок
        trade_messages = [f"Сделка {trade['id']}: {trade['amount']} BTC по цене {trade['price']} USDT" for trade in trades]
        await callback_query.message.answer("\n".join(trade_messages))
        await show_menu_after_request(callback_query.message)
    except Exception as e:
        logging.error(f"Ошибка при получении истории торгов: {e}")
        await callback_query.message.answer("Ошибка при получении истории торгов.")
    # После отправки графика, отправляем пользователю основное меню
    await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
    await callback_query.answer()


class PriceAlert(StatesGroup):
    setting_coins = State()
    setting_prices = State()

@dp.callback_query_handler(lambda c: c.data == 'set_price_alert')
async def set_price_alert_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Введите монеты, разделенные запятыми, для которых вы хотите установить уведомление (например, BTC,ETH,ADA):")
    await PriceAlert.setting_coins.set()
    await callback_query.answer()


@dp.message_handler(commands=['setpricealert'])
async def set_price_alert_command(message: types.Message):
    markup = InlineKeyboardMarkup().add(cancel_button)
    await message.answer(
        "Введите монеты, разделенные запятыми, для которых вы хотите установить уведомление (например, BTC,ETH,ADA):",
        reply_markup=markup)


@dp.message_handler(state=PriceAlert.setting_coins)
async def set_alert_coins(message: types.Message, state: FSMContext):
    coins = [coin.strip().upper() for coin in message.text.split(",")]
    await state.update_data({"coins": coins})  # Исправленная строка
    await message.answer(f"Введите пороговые цены для {', '.join(coins)} (например, 50000,3000,2):")
    await PriceAlert.next()


@dp.message_handler(state=PriceAlert.setting_prices)
async def set_price_alerts(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup().add(cancel_button)  # Добавляем кнопку отмены
    user_data = await state.get_data()
    coins = user_data.get("coins")

    # Проверка ввода пользователя
    if not all(is_number(price.strip()) for price in message.text.split(",")):
        await message.answer("Пожалуйста, введите только числовые значения для цен. Попробуйте снова.", reply_markup=markup)
        return

    prices = [float(price.strip()) for price in message.text.split(",")]

    if len(prices) != len(coins):
        await message.answer("Количество монет и цен не совпадает. Пожалуйста, попробуйте снова.", reply_markup=markup)
        return

    # Здесь вы можете сохранить пороговые цены и монеты в базе данных или другом хранилище
    # Например: save_alerts_to_db(user_id=message.from_user.id, alerts=dict(zip(coins, prices)))

    # Создаем клавиатуру с кнопками активации и деактивации уведомлений
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("Activate Alerts", callback_data="activate_alerts"))
    markup.add(InlineKeyboardButton("Deactivate Alerts", callback_data="deactivate_alerts"))
    markup.add(cancel_button)

    await message.answer(
        f"Уведомления установлены для: {', '.join([f'{coin} - {price} USDT' for coin, price in zip(coins, prices)])}. Выберите действие:", reply_markup=markup)
    await state.finish()



@dp.callback_query_handler(lambda c: c.data == "cancel_action", state='*')
async def cancel_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.answer("Действие отменено.")
    # После отправки графика, отправляем пользователю основное меню
    await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
    await callback_query.answer()



@dp.message_handler(lambda message: message.text.lower() == 'отмена', state='*')
async def cancel_text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logging.info(f'Cancelling state {current_state}')
        await state.finish()
        await message.answer('Действие отменено.')
    else:
        await message.answer('Нет активного действия для отмены.')


@dp.callback_query_handler(lambda c: c.data == 'activate_alerts')
async def activate_alerts(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_alerts_status[user_id] = True
    await callback_query.message.answer("Уведомления активированы.")
    # После отправки графика, отправляем пользователю основное меню
    await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data == 'deactivate_alerts')
async def deactivate_alerts(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_alerts_status[user_id] = False
    await callback_query.message.answer("Уведомления деактивированы.")
    # После отправки графика, отправляем пользователю основное меню
    await callback_query.message.answer("Выберите действие из меню:", reply_markup=menu)
    await callback_query.answer()

# Глобальный словарь для хранения уведомлений
# Ключ - ID пользователя, значение - список словарей с монетой и пороговой ценой
alerts = {}

async def check_price_alerts():
    while True:
        for user_id, user_alerts in alerts.items():
            for alert in user_alerts:
                coin = alert['coin']
                threshold_price = alert['price']

                try:
                    # Получение текущей цены монеты
                    ticker = await exchange.fetch_ticker(f'{coin}/USDT')
                    current_price = ticker['last']

                    # Если текущая цена достигла или превысила порог
                    if current_price >= threshold_price:
                        await bot.send_message(user_id, f"Цена {coin} достигла {current_price} USDT!")
                        user_alerts.remove(alert)  # Удалить уведомление после отправки
                except Exception as e:
                    logging.error(f"Ошибка при проверке цены для {coin}: {e}")

        # Пауза перед следующей проверкой
        await asyncio.sleep(300)  # Проверка каждые 5 минут



if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)