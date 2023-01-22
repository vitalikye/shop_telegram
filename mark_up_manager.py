from telebot import *
from config import *


#main board
wish_main = types.KeyboardButton(send_wish_btn)
order_main = types.KeyboardButton(order_btn)
info_main = types.KeyboardButton(info_btn)
contacts_main = types.KeyboardButton(contacts_btn)
main_board = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_board.add(order_main, info_main, contacts_main, wish_main, row_width=2)

#back board
back_main_button = types.KeyboardButton(back_btn)
back_board = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_board.add(back_main_button)

#info board
info_meat = types.KeyboardButton(info_meat_btn)
info_maker= types.KeyboardButton(info_maker_btn)
info_deal = types.KeyboardButton(info_deal_btn)
info_board = types.ReplyKeyboardMarkup()
info_board.add(info_meat, info_maker, info_deal, contacts_main, back_main_button)

#deal board
deal_board = types.ReplyKeyboardMarkup()
deal_board.add(deal_btn, cart_remove_btn, back_btn)

cart_remove_board = types.ReplyKeyboardMarkup()
cart_remove_board.add(standart_tasty_btn, chernosliv_tasty_btn, ginger_tasty_btn, remove_all_btn, back_btn)

#subinfo bord
subinfo_board = types.ReplyKeyboardMarkup()
subinfo_board.add(info_main, back_main_button)

#products_board
standart_tasty = types.KeyboardButton(standart_tasty_btn)
chernosliv_tasty = types.KeyboardButton(chernosliv_tasty_btn)
ginger_tasty = types.KeyboardButton(ginger_tasty_btn)
cart_main = types.KeyboardButton(cart_btn)
products_board = types.ReplyKeyboardMarkup()
products_board.add(standart_tasty, chernosliv_tasty, ginger_tasty, back_main_button, cart_main)

#subproduct board
sub_product_board = types.ReplyKeyboardMarkup()
sub_product_board.add(order_btn, deal_btn, cart_btn, back_btn)

#inline weight buttons
weight_choice_inline = types.InlineKeyboardMarkup()
weight_50 = types.InlineKeyboardButton(text="+50", callback_data=btn50)
weight_100 = types.InlineKeyboardButton(text="+100", callback_data=btn100)
weight_200 = types.InlineKeyboardButton(text="+200", callback_data=btn200)
weight_500 = types.InlineKeyboardButton(text="+500", callback_data=btn500)
weight_1000 = types.InlineKeyboardButton(text="+1000", callback_data=btn1000)
weight_own = types.InlineKeyboardButton(text="Cвій варіант", callback_data=btnown)
weight_choice_inline.add(weight_50, weight_100, weight_200, weight_500, weight_1000, weight_own)

# #Inline name board
# ask_name_board = types.InlineKeyboardMarkup()
# yes_name_button = types.InlineKeyboardButton(text="Так", callback_data=name_yes_callback)
# no_name_button = types.InlineKeyboardButton(text="Ні", callback_data=name_no_callback)
# ask_name_board.add(yes_name_button, no_name_button)
#
# #Inline phone board
# ask_phone_board = types.InlineKeyboardMarkup()
# yes_phone_button = types.InlineKeyboardButton(text="Так", callback_data=phone_yes_callback)
# no_phone_button = types.InlineKeyboardButton(text="Ні", callback_data=phone_no_callback)
# ask_phone_board.add(yes_phone_button, no_phone_button)

#Inline post info board
ask_post_info_board = types.InlineKeyboardMarkup()
yes_post_info_button = types.InlineKeyboardButton(text="Так", callback_data=post_info_yes_callback)
no_post_info_button = types.InlineKeyboardButton(text="Ні", callback_data=post_info_no_callback)
ask_post_info_board.add(yes_post_info_button, no_post_info_button)

#Payment board
prepay_button = types.KeyboardButton(prepay_btn)
not_prepay_button = types.KeyboardButton(not_prepay_btn)
payment_board = types.ReplyKeyboardMarkup()
payment_board.add(prepay_button, not_prepay_button, back_main_button)

#done_board
done_board = types.ReplyKeyboardMarkup()
done_button = types.KeyboardButton(done_btn)
done_board.add(done_button, back_btn)

#clear all Markups
clear_board = types.ReplyKeyboardRemove()


