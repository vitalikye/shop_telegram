import sqlite3
from config import *
import json
from datetime import datetime
#
# db = sqlite3.connect(DATA_BASE_MAIN)
# cursor = db.cursor()
# cursor.execute(""" DELETE FROM orders WHERE user_id=57831246""")
# db.commit()
# db.close()


def insert_wish(id, username, wish):
    db = sqlite3.connect(DATA_BASE_MAIN)
    cursor = db.cursor()
    params = (id, username, wish)
    try:
        cursor.execute(f"INSERT INTO wishes VALUES(?, ?, ?)", params)
    except Exception as exc:
        print(f"ERROR!!! {exc}")
    db.commit()
    db.close()

def get_product_info(id):
    db = sqlite3.connect(DATA_BASE_MAIN)
    sql = db.cursor()
    try:
        sql.execute(f"SELECT name, price, discription FROM products WHERE id = {id}")
    except Exception as e:
        print(f'error with selecting product info{e}')
    result = sql.fetchone()
    db.close()
    return result


def add_to_cart(product_id, weight, user_id):
    print(f'вага яку я додую в кошик {weight, product_id}')
    cart_dict = {}
    db = sqlite3.connect(DATA_BASE_MAIN)
    sql = db.cursor()
    try:
        sql.execute(f"SELECT cart_info FROM cart WHERE user_id={user_id}")
        res = sql.fetchone()[0]
        cart_dict = json.loads(res)
        if str(product_id) in cart_dict:
            print("yes i find it in dict")
            cart_dict[str(product_id)] += weight
        else:
            print("no i didnt find it in dict")
            cart_dict[str(product_id)] = weight
        cart_json = json.dumps(cart_dict)
        sql.execute(f"UPDATE cart SET cart_info = ? WHERE user_id = ?", (cart_json, user_id))

    except Exception as exc:
        print(exc)
        cart_dict[product_id] = weight
        cart_json = json.dumps(cart_dict)
        print("try to INSERT data to cart")
        sql.execute(f"INSERT INTO cart (user_id, cart_info) VALUES (?, ?)", (user_id, cart_json))
    print(f'commited weight in cart')
    db.commit()
    db.close()

def get_cart_info(user_id):
    full_cart_info = list()
    try:
        db = sqlite3.connect(DATA_BASE_MAIN)
        sql = db.cursor()
        sql.execute(f"""SELECT cart_info FROM cart WHERE user_id = {user_id}""")
        res = sql.fetchone()[0]
        cart_dict = json.loads(res)
        for product_id_str, weight in cart_dict.items():
            # print(product_id_str, weight)
            product_id = int(product_id_str)
            sql.execute(f"SELECT name, price FROM products WHERE id = {product_id}")
            res = sql.fetchone()
            total_price = weight * (res[1] / 10)
            tuple_info = (res[0], res[1], weight, total_price)
            full_cart_info.append(tuple_info)
        db.commit()
        db.close()
        return full_cart_info
    except:
        return full_cart_info

def remove_from_cart(id, user_id):
    db = sqlite3.connect(DATA_BASE_MAIN)
    sql = db.cursor()
    if id != 777:
        try:
            sql.execute(f"""SELECT cart_info FROM cart WHERE user_id={user_id}""")
            result_tuple = sql.fetchone()
            result_dict = json.loads(result_tuple[0])
            result_dict.pop(f"{id}", None)
            new_cart_info = json.dumps(result_dict)
            sql.execute("UPDATE cart SET cart_info=? WHERE user_id=?", (new_cart_info, user_id))
            db.commit()
            db.close()
            return "Продукт видалено із вашего кошику"
        except Exception as exc:
            print(f"ERROR!!! {exc}")
            db.close()
            return "Такого продукту не було в вашому кошик, або ви ще нічого не додавали в кошик"
    else:
        try:
            sql.execute(f"DELETE FROM cart WHERE user_id={user_id}")
            db.commit()
            db.close()
            return "Ваш кошик очещено"
        except Exception as exc:
            print(f'another ERROR! {exc}')
            db.close()
            return "Ви ще нічого не додавали в кошик"

def make_order(user_id, order_info):
    timenow = datetime.now()
    datetimestr = timenow.strftime("%d/%m/%Y %H:%M:%S")
    db = sqlite3.connect(DATA_BASE_MAIN)
    sql = db.cursor()
    sql.execute("INSERT INTO orders VALUES(?, ?, ?)", (user_id, order_info, datetimestr))
    db.commit()
    sql.execute(f"SELECT rowid FROM orders WHERE user_id={user_id} ORDER BY rowid DESC")
    order_number = sql.fetchmany()
    return order_number[0][0]

def delete_cart(user_id):
    db = sqlite3.connect(DATA_BASE_MAIN)
    sql = db.cursor()
    sql.execute(f"DELETE FROM cart WHERE user_id = {user_id}")
    db.commit()
    db.close()

def check_cart_exist(user_id):
    db = sqlite3.connect(DATA_BASE_MAIN)
    sql = db.cursor()
    try:
        sql.execute(f"SELECT rowid FROM cart WHERE user_id={user_id}")
        db.close()
        return True
    except Exception as exc:
        print(exc)
        db.close()
        return False






    # sql.execute(f"SELECT price FROM products WHERE id = {product_id}")
    # current_price = sql.fetchone()[0]
    # total_price = current_price * weight
    # print(total_price)


#connect to db
# db = sqlite3.connect(DATA_BASE_MAIN)

#create cursor
# sql = db.cursor()

#CCCCC
#Creating Table
# sql.execute("""CREATE TABLE products (
# id integer,
# name text,
# price integer,
# discription text
# )""")

#adding data in the cells
# sql.execute("INSERT INTO products VALUES(003, 'ginger', 70, 'its ok, no realy')")

#RRR
#select data we need
# sql.execute("SELECT * FROM products")
# sql.execute("SELECT rowid, id FROM products WHERE name = 'standart'") - WHERE additional filters
# sql.execute("SELECT rowid, id FROM products")sql.execute("SELECT rowid, id FROM products WHERE rowid < 5 ORDER BY rowid") - ORDER is sorting by smt add DESC to invert
# print(sql.fetchall())
# sql.fetchmany() - select many with number of results
# sql.fetchone() - select one but in tuple

#UUUU
# sql.execute("UPDATE products SET price = 50 WHERE name = 'standart'")

#DDDD
#DELETE FROM <table_name> WHERE <term> - delete data

#finish work with DB
# db.commit()
# db.close()

