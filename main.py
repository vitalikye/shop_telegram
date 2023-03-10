
from telebot import *
from config import *
from data_manager import *
from mark_up_manager import *

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_walcome(message):
    bot.reply_to(message, f"Привіт✌️! {message.from_user.first_name}, мене звати @yish_sobi_bot і я допоможу тобі придбати м'яско")
    bot.send_message(message.chat.id, 'Обери в меню потрібну опцію', reply_markup=main_board)

#main text handler. Ir handle most of reply markup buttons
@bot.message_handler(content_types='text')
def main_handler(message):
    if message.text == order_btn:
        msg = bot.send_message(message.chat.id, "Супер!👍 Обери смак, який тобі довподоби.", reply_markup=products_board)
        bot.register_next_step_handler(msg, choice_product)
    elif message.text == send_wish_btn:
        msg = bot.send_message(message.chat.id, "Можеш написати нам все, що забажаєш повідомленням. Ми обов'язково все прочитаємо!")
        bot.register_next_step_handler(msg, send_wish)
    elif message.text == contacts_btn:
        bot.send_message(message.chat.id, "Ти можеш з нами зв'язатися:\n в Telegram - @kokolenko\n або в Instagram - https://instagram.com/yizh_sobi", reply_markup=back_board)
    elif message.text == info_btn:
        bot.send_message(message.chat.id, "Яка саме інформація тебе цікавить?", reply_markup=info_board)
    elif message.text == back_btn:
        bot.send_message(message.chat.id, 'Обери в меню потрібну опцію', reply_markup=main_board)
    elif message.text == info_meat_btn:
        bot.send_message(message.chat.id, product_info_text, reply_markup=subinfo_board, parse_mode='html')
    elif message.text == info_deal_btn:
        bot.send_message(message.chat.id, deal_info_text, reply_markup=subinfo_board, parse_mode='html')
    elif message.text == info_maker_btn:
        bot.send_message(message.chat.id, maker_info_text, reply_markup=subinfo_board, parse_mode='html')
    elif message.text == cart_remove_btn:
        msg = bot.send_message(message.chat.id, "Обери, щоб ти хотів видалити із кошика", reply_markup=cart_remove_board)
        bot.register_next_step_handler(msg, remove_from_cart_handler)
    elif message.text == cart_btn:
        bot.send_message(message.chat.id, "Дивимось, що ти додав у кошик", reply_markup=sub_product_board)
        show_cart_handler(message)
    elif message.text == deal_btn:
        if check_cart_exist(user_id=message.from_user.id):
            msg = bot.send_message(message.chat.id, "Добре, для початку напиши своє Прізвище Імя По батькові", reply_markup=clear_board)
            bot.register_next_step_handler(msg, register_name)
        else:
            bot.send_message(message.chat.id, f"Нажаль ваш кошик поки що порожній, щоб додати товар у кошик перейдіть в {order_btn}", reply_markup=main_board)
    elif message.text == done_btn:
        delete_cart(user_id=message.from_user.id)
        bot.send_message(message.chat.id, "Дякую, що обрали <b>ЇжСобі</b>. Повертайтесь ще🖐.", reply_markup=main_board, parse_mode='html')

    elif message.text == 'send full info':
        print(message)

def choice_product(message):
    global id
    if message.text == standart_tasty_btn:
        id = 1
    elif message.text == chernosliv_tasty_btn:
        id = 2
    elif message.text == ginger_tasty_btn:
        id = 3
    elif message.text == cart_btn:
        id = 0
        show_cart_handler(message)
    else:
        id = 0
        bot.send_message(message.chat.id, "Ой лишенько, щось пішло не так, давай спробуємо за самого початку", reply_markup=main_board)
    if id > 0:
        send_product_info_handler(message, id)

#send pic and all info about product, ask pick a weight
def send_product_info_handler(message, id):
    product_info = get_product_info(id=id)
    name = product_info[0]
    price = product_info[1]
    description = product_info[2]
    print(name, price, description)
    caption = f"М'яско {name}\n----------------\n Ціна - {price}грн. (ціна за 100 грам)\n опис: {description}"
    file_url = f"media/id{id}.jpg"
    try:
        bot.send_photo(message.chat.id, open(file_url, 'rb'), caption=caption, reply_markup=weight_choice_inline)
        bot.send_message(message.chat.id, "Обери потрібну вагу ( у грамах ) ⬆️⬆️⬆️", reply_markup=sub_product_board)
    except Exception as e:
        print(f"От халепа, вийшла якась помилка. Ми над цим попрацюємо і все виправимо")

@bot.callback_query_handler(func=lambda call:True)
def inline_handler(call):
    print(call.data)
    if call.data == btnown:
        msg = bot.send_message(call.message.chat.id,
                               "Напиши скільки ти б хотів придбрати м'яска у грамах (знаками '0-9')", reply_markup=back_board)
        bot.register_next_step_handler(msg, own_weight_handler)
    elif call.data == post_info_yes_callback:
        bot.send_message(call.message.chat.id, "Дякую, Ось твоє замовлення.")
        user_order_info = show_all_order_info(user_id=call.from_user.id)
        bot.send_message(call.message.chat.id, user_order_info,parse_mode='html')
        msg = bot.send_message(call.message.chat.id, "Якщо вся інформація вірна, можеш обрати спосіб оплати", reply_markup=payment_board)
        bot.register_next_step_handler(msg, payment_handler)
    elif call.data == post_info_no_callback:
        msg = bot.send_message(call.message.chat.id, "Зрозумів, давай почнемо з початку, напиши свої ПІБ")
        bot.register_next_step_handler(msg, register_name)
    else:
        weight = int(call.data)
        add_to_cart(id, weight, call.from_user.id)
        bot.send_message(call.message.chat.id, f"Файно! {weight} грам додано в твій кошик. Можеш обрати ще смаки.", reply_markup=sub_product_board)
        bot.send_message(call.message.chat.id, "Можеш перейти до оформлення замовлення, або обрати собі ще м'яска і додати в кошик")

def own_weight_handler(message):
    print(f'id in own weught handler id - {id}')
    try:
        order_weight = int(message.text)
        add_to_cart(id, order_weight, message.from_user.id)
        bot.send_message(message.chat.id, f"Файно! {order_weight} грам додано в твій кошик. Можеш обрати ще смаки",
                         reply_markup=sub_product_board)
    except Exception as e:
        print(f'Помилка із введенням власної ваги {e}')
        msg_error = bot.send_message(message.chat.id, "Тю, щось пішло не так, давай спробуємо ще раз.")
        bot.register_next_step_handler(msg_error, own_weight_handler)

def show_cart_handler(message):
    print('goi into show cart handler')
    user_cart = get_cart_info(user_id=message.from_user.id)
    if len(user_cart) == 0:
        bot.send_message(message.chat.id, "Твій кошик поки що порожній. Обери продукт та додай собі в кошик", reply_markup=sub_product_board)
        bot.send_message(message.chat.id, f"Для того щоб додати собі товар у кошик перейди в '{order_btn}'")

    else:
        print("Формую корзину")
        cart_info = "<b>Назва | Ціна | Вага | Всього </b>\n"
        cart_total_price = 0
        for each_product_info in user_cart:
            product_name, price, weight, total_price = each_product_info[0], each_product_info[1], each_product_info[2], each_product_info[3]
            cart_info += f"{product_name} | {price} | {weight} | {total_price}\n"
            cart_total_price += total_price
        cart_info += f"<b>СУМА ДО СПЛАТИ -------- {cart_total_price}</b>"
        print("Sending CART info to tg")
        bot.send_message(message.chat.id, cart_info, reply_markup = deal_board, parse_mode='html')

def remove_from_cart_handler(message):
    global remove_id
    if message.text == standart_tasty_btn:
        remove_id = 1
    elif message.text == chernosliv_tasty_btn:
        remove_id = 2
    elif message.text == ginger_tasty_btn:
        remove_id = 3
    elif message.text == remove_all_btn:
        remove_id = 777
    else:
        print("message dont readable in remove_from_cart_handler, no remove id")
        msg = bot.send_message(message.chat.id, "От халепа, щось пішло не так. Давай спробуємо ще", reply_markup=cart_remove_board)
        bot.register_next_step_handler(msg, show_cart_handler)
    if remove_id > 0:
        msg_text = remove_from_cart(id=remove_id, user_id=message.from_user.id)
        bot.send_message(message.chat.id, msg_text, reply_markup=cart_remove_board)
        show_cart_handler(message)

def register_name(message):
    global name
    name = message.text
    msg = bot.send_message(message.chat.id, "Дякую, я записав твоє ім'я. Тепер будь ласка вкажи свій <b>номер телефону</b>", parse_mode='html')
    bot.register_next_step_handler(msg, register_phone)

def register_phone(message):
    global phone_number
    phone_number = message.text
    msg = bot.send_message(message.chat.id,"Дякую, Я записав твій номер телефону. Тепер будь ласка відправ інформацію про відправку: <b>Місто, Область, Номер Нової пошти (наприклад: Київ, Київська область, Відділення №121)</b>", parse_mode='html')
    bot.register_next_step_handler(msg, register_post_info)

def register_post_info(message):
    global post_info
    post_info = message.text
    bot.send_message(message.chat.id, f"Відмінно! Подивись, чи вірно я записав всю інформацію:\n ПІБ - <b>{name}</b> \nНомер телефону - <b>{phone_number}</b> \nІнформація про відправку - <b>{post_info}</b> \n Якщо все вірно натисни <b>'Так'</b>, щоб продовжити, або <b>'Ні'</b>, щоб виправити і надіслати нам вірну інформацію\n ⬇️⬇️⬇️⬇️⬇️⬇️⬇️",
                     reply_markup=ask_post_info_board, parse_mode='html')

#function that show user whole info about his order
def show_all_order_info(user_id):
    print(user_id)
    total_order_info = "<b>Ваше замовлення:</b>\n <b>Назва | Ціна | Вага | Всього </b>\n"
    global order_number
    global cart_total_price
    cart_total_price= 0
    cart_info = get_cart_info(user_id)
    for each_product_info in cart_info:
        product_name, price, weight, total_price = each_product_info[0], each_product_info[1], each_product_info[2], each_product_info[3]
        print(product_name, price, weight, total_price)
        total_order_info += f"{product_name} | {price} | {weight} | {total_price}\n"
        cart_total_price += int(total_price)
    total_order_info += f"<b>СУМА ДО СПЛАТИ -------- {cart_total_price}</b>"
    total_order_info += f"\n<b>ПІБ Замовника:</b> {name}\n <b>Номер телефону:</b> {phone_number}\n <b>Інформація про відділення:</b> {post_info}"
    order_number = make_order(user_id, total_order_info)
    total_order_info += f"\n<b>НОМЕР ВАШОГО ЗАМОВЛЕННЯ - {order_number} </b>"
    return total_order_info

#fuinction that ask user wich way he gonna pay?
  # print(name, price, description)
  #   caption = f"М'яско {name}\n----------------\n Ціна - {price} (ціна за 100 грам)\n опис: {description}"
  #   file_url = f"media/id{id}.jpg"
  #   try:
  #       bot.send_photo(message.chat.id, open(file_url, 'rb'), caption=caption, reply_markup=weight_choice_inline)
  #       bot.send_message(message.chat.id, "Обери потрібну вагу ( у грамах ) ⬆️⬆️⬆️", reply_markup=sub_product_board)
  #   except Exception as e:
  #       print(f"От халепа, вийшла якась помилка. Ми над цим попрацюємо і все виправимо")

def payment_handler(message):
    global summary_price
    if message.text == prepay_btn:
        summary_price = cart_total_price
    elif message.text == not_prepay_btn:
        summary_price = 60
    elif message.text == back_btn:
        main_handler(message=message)
    msg_text = f"Ти можеш сплати за номером картки\n <b>5168 7520 0106 2002</b> (на ім'я Буряковський Ігор)\n або перейшовши по QR-коду в зображені\n Сума до сплати - <b>{summary_price}грн</b>\n ❗️❗️❗️ВАЖЛИВО: <b>Вкажи номер замовлення в призначенні платежу</b>\n Твій номер замовлення - <b>{order_number}</b>"
    qr_url = "media/qr.png"
    try:
        bot.send_photo(message.chat.id, open(qr_url, 'rb'), caption=msg_text, parse_mode='html', reply_markup=done_board)
    except Exception as e:
        print(f"FUCK! some problems {e}")
        msg = bot.send_message(message.chat.id, "Ой, щось пішло не так. Ми обов'язково подивимось і виправимов всі проблеми в боті", reply_markup=main_board)
        bot.register_next_step_handler(msg, main_handler)
#function that accept text as message and write it in data base
def send_wish(message):
    wish = str(message.text)
    user_id = message.from_user.id
    user_name = str(message.from_user.username)
    user_full_name = f"name {message.from_user.first_name} {message.from_user.last_name} \n username - {message.from_user.username}"
    insert_wish(user_id, user_name, wish)
    bot.send_message(admin_chat_id, f"Надійшло нове побажання від: {user_full_name} текст побажання: {wish}")
    bot.send_message(message.chat.id, 'Дякую! Ти мій накращий друг тепер!', reply_markup=back_board)

bot.infinity_polling()


