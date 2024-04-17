import telebot
from telebot import types
from MyClass import *
import matplotlib.pyplot as plt


API_TOKEN = "Your_Token"
bot = telebot.TeleBot(API_TOKEN)

# список состояния выполнения задач
numb_task = [0, 0, 0, 0]

obj_kpv = KPV()
obj_balance = MarketEquilibrium()
obj_def = DeficitAndSurplus()
obj_profit = ProfitCompany()


def reset() -> None:
    for i in range(len(numb_task)):
        numb_task[i] = 0
    obj_kpv.reset_data()
    obj_balance.reset_data()
    obj_def.reset_data()
    obj_profit.reset_data()


def buttons_for_task_profit_company(message) -> None:
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    if obj_profit.go_to_button_has_worked():
        button1 = types.InlineKeyboardButton('К расчетам', callback_data="next")
    else:
        button1 = types.InlineKeyboardButton('Перейти', callback_data="next")
    keyboard.add(button1)
    bot.send_message(message.chat.id, obj_profit.get_str())
    bot.send_message(message.chat.id, f"Добавлено {obj_profit.count_costs()} из 5",
                     reply_markup=keyboard)


def is_float(message) -> bool:
    try:
        float(message.text)
    except ValueError:
        return False
    return True


@bot.message_handler(content_types=[
    'animation', 'audio', 'document', 'photo', 'sticker', 'video',
    'video_note', 'voice', 'dice', 'location', 'contact', 'new_chat_members',
    'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo',
    'group_chat_created', 'supergroup_chat_created', 'channel_chat_created',
    'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', ])
def answer_on_incorrect_type(message):
    bot.send_message(message.chat.id, 'Для расчетов используются исключительно числа.')
    handle_start(message)


@bot.message_handler(commands=['start'])
def handle_start(message):
    reset()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Построение общей КПВ', callback_data="KPV")
    button2 = types.InlineKeyboardButton('Нахождение точки р.р.', callback_data='Point')
    button3 = types.InlineKeyboardButton('Дефицит/Излишек', callback_data='Def')
    button4 = types.InlineKeyboardButton('Прибыль фирмы', callback_data='Profit')
    keyboard.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, "Выберите задачу", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Отмена" or message.text == "отмена")
def button_back(message) -> None:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton("Отмена")
    keyboard.add(button1)
    if sum(numb_task) == 0:
        bot.send_message(message.chat.id, "Задачи на выполнения нет", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Выполнение задачи отменено", reply_markup=keyboard)
    reset()

    handle_start(message)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Бот для расчета экономических задач. Таких как:\n'
                          '- Построение общей кривой производственных возможностей для 2 производителей\n'
                          '- Нахождения точки рыночного равновесия\n'
                          '- Расчет объема децифита/излишка\n'
                          '- Расчет прибыли фирмы\n')

    text = ('Для начала работы выберите задачу и следуйте инструкциям.\n'
            'Для отмены выполнения задачи, отправьте "Отмена" '
            'или нажмите на кнопку "Отмена".')
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: True)
def answer_message(message) -> None:
    """
        Основной обработчик при выполнении задач. Работа функции основывается на numb_task.
    """
    message.text = message.text.replace(',', '.')
    try:
        if numb_task[0] == 1 and obj_kpv.is_recording:
            if not is_float(message) or float(message.text) < 0:
                raise MyExcept(obj_kpv.get_str())

            # при заполнении массива данных, выставляется запрет на запись ( is_recordind = 0)
            obj_kpv.add_arr(float(message.text))

            if not obj_kpv.is_recording:
                calculate_kpv(message)
            else:
                bot.send_message(message.chat.id, obj_kpv.get_str())

        elif numb_task[1] == 1 and obj_balance.is_recording:
            if not is_float(message) or float(message.text) < 0:
                raise MyExcept(obj_balance.get_str())

            obj_balance.add_arr(float(message.text))

            if not obj_balance.is_recording:
                calculate_the_market_equilibrium(message)
            else:
                bot.send_message(message.chat.id, f"{obj_balance.get_str()}")

        elif numb_task[2] == 1 and obj_def.is_recording:
            if not is_float(message) or float(message.text) < 0:
                raise MyExcept(obj_def.get_str())

            obj_def.add_arr(float(message.text))

            if not obj_def.is_recording:
                calculate_deficit_or_surplus(message)
            else:
                bot.send_message(message.chat.id, f"{obj_def.get_str()}")

        # В этом блоке ввод данных разделен на 2 части
        elif numb_task[3] == 1 and obj_profit.is_recording:
            # Первая часть: получение данных для двух переменных. Метод in_progress_first_part()
            # указывает, что выполняется первая часть
            if obj_profit.in_progress_first_part():
                if not message.text.isdigit():
                    raise MyExcept(obj_profit.get_str())

                obj_profit.add_numb(int(message.text))

            else:
                # Вторая часть: получение данных для двух массивов
                tmp = message.text.split()
                if len(tmp) != 2 or tmp[0].isdigit() or not tmp[1].isdigit():
                    bot.send_message(message.chat.id,
                                     "Неверный формат данных. Формат:'Название издержки Значение'")
                    buttons_for_task_profit_company(message)
                    return

                tmp[1] = int(tmp[1])
                obj_profit.add_costs(tmp)  # Данные добавляются через общий метод, внутри распределяются

            if not obj_profit.is_recording:
                calculate_profit_company(message)
                return

            #
            if not obj_profit.in_progress_first_part():
                buttons_for_task_profit_company(message)
            else:
                bot.send_message(message.chat.id, obj_profit.get_str())

        else:
            handle_start(message)
    except MyExcept as objExcept:
        bot.send_message(message.chat.id, 'Необходимо вводить только положительные числа!')
        bot.send_message(message.chat.id, objExcept.str_error)


def calculate_the_market_equilibrium(message):
    numb_task[1] = 0
    value_a, value_b, value_c, value_d = obj_balance.get_data()
    try:
        price = (value_a - value_c) / (value_d + value_b)
        result = value_a - value_b * price

        result_str = (f'Рыночное равновесие:\n'
                      f'Цена (P*):{round(price,2)}\n'
                      f'Объем (Q*): {round(result,2)}')

        bot.send_message(message.chat.id, result_str)
    except ZeroDivisionError:
        bot.send_message(message.chat.id, 'Данные не корректны. Деление на ноль не возможно.')

    handle_start(message)


def calculate_deficit_or_surplus(message):
    numb_task[2] = 0
    value_a = obj_def.get_numb_arr(0)
    value_b = obj_def.get_numb_arr(1)
    value_c = obj_def.get_numb_arr(2)
    value_d = obj_def.get_numb_arr(3)
    value_e = obj_def.get_numb_arr(4)

    qd = value_a - value_b * value_e  # дефицит
    qs = value_c + value_d * value_e  # избыток

    result = qd - qs
    if result > 0:
        answer = "излишка"
    elif result < 0:
        answer = "дефицита"
        result *= -1
    else:
        answer = "равновесия"

    text = f"При уровне цены {obj_def.get_numb_arr(4)} денежных единицах на рынке будет ситуация {answer} ."
    text2 = f"Размер {answer} составит: {round(result,2)} единиц."

    if answer != 'равновесия':
        bot.send_message(message.chat.id, text + text2)
    else:
        bot.send_message(message.chat.id, text)
    handle_start(message)


def calculate_kpv(message):
    numb_task[0] = 0
    value_a1, value_b1, value_a2, value_b2 = obj_kpv.get_data()

    point_a = [value_a1 + value_a2, 0]
    point_b = [max(value_a1, value_a2), max(value_b1, value_b2), ]
    point_c = [0, value_b1 + value_b2]

    # Получение координат
    a_x, a_y = point_a
    b_x, b_y = point_b
    c_x, c_y = point_c

    # Построение графика
    plt.figure(figsize=(9, 7))
    plt.scatter([a_y, b_y, c_y], [a_x, b_x, c_x], color="black", label="Точки")

    # Получение отрезков через точки
    plt.plot([a_y, b_y], [a_x, b_x], color="green", linestyle="-", label="Производитель 1")
    plt.plot([b_y, c_y], [b_x, c_x], color="blue", linestyle="-", label="Производитель 2")

    plt.text(a_y, a_x, "A", fontsize=12, ha="right", va="bottom")
    plt.text(b_y, b_x, "B", fontsize=12, ha="left", va="top")
    plt.text(c_y, c_x, "C", fontsize=12, ha="right", va="top")

    # Настройки графики
    plt.title("Общая КПВ")
    plt.xlabel("Производство товара Б")
    plt.ylabel("Производство товара A")
    plt.legend()
    plt.grid(True, linestyle="-", alpha=0.8)
    plt.savefig("graph.png")
    plt.close()
    bot.send_photo(message.chat.id, open("graph.png", "rb"))
    handle_start(message)


def calculate_profit_company(message) -> None:
    bot.send_message(message.chat.id, f"{obj_profit.result()}")
    handle_start(message)


@bot.callback_query_handler(func=lambda callback: True)
def call_keyboard(callback) -> None:
    """
    При нажатии кнопки здесь определяется какая была выбрана. В соответствии с задачей в numb_task устанавливается
    флаг(единица), которая указывает какой алгоритм выполнять в функци answer_message, а так же выставляется для
    объекта этой задачи, флаг на запись данных
    """
    # Здесь действия для кнопок, которые выдаются для решения задачи "Profit company"
    if callback.data == 'next':
        if obj_profit.getting_data():
            obj_profit.abort_getting_data_for_first_arr()
            buttons_for_task_profit_company(callback.message)
        else:
            calculate_profit_company(callback.message)

        return

    # Отрабатывает, если выбрать задачу в списке задач, во время выполнения любой другой
    if sum(numb_task) != 0:
        bot.send_message(callback.message.chat.id, "Выполнение задачи прервано")

    reset()
    if callback.data == 'KPV':
        if sum(numb_task) != 0:
            reset()
        bot.send_message(callback.message.chat.id, obj_kpv.get_str())
        numb_task[0] = 1
        obj_kpv.is_recording = 1
    elif callback.data == 'Point':
        bot.send_message(callback.message.chat.id, obj_balance.get_info())
        numb_task[1] = 1
        bot.send_message(callback.message.chat.id, obj_balance.get_str())
        obj_balance.is_recording = 1
    elif callback.data == 'Def':
        bot.send_message(callback.message.chat.id, obj_def.get_info())
        numb_task[2] = 1
        bot.send_message(callback.message.chat.id, f"{obj_def.get_str()}")
        obj_def.is_recording = 1
    elif callback.data == 'Profit':
        numb_task[3] = 1
        bot.send_message(callback.message.chat.id, obj_profit.get_str())
        obj_profit.is_recording = 1


bot.infinity_polling()


