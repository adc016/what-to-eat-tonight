import random
import sqlite3
import requests
import json


def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    sql_command = '''
    CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT
    );'''

    cursor.execute(sql_command)

    conn.commit()
    conn.close()
    print("成功创建数据表")

def add_food(food_name, food_category):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 使用占位符?
    sql = "INSERT INTO foods (name, category) VALUES (?, ?)"
    cursor.execute(sql, (food_name, food_category))

    #保存
    conn.commit()
    conn.close()
    print(f"成功把{food_name}加入菜单")

def show_menu():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    #SQL指令: 从foods表展示所有东西
    sql = "SELECT * FROM foods"
    cursor.execute(sql)
    #fetchall(),意思"Fetch All"(抓取所有)
    all_foods = cursor.fetchall()

    #判断列表是否为空
    if not all_foods:
        print("菜单为空，快去添加点菜吧")
    else:
        print(f"菜单里共有{len(all_foods)}道菜:")
        print("-" * 30)

        #遍历每一行数据fenglei
        for food in all_foods:
            # food 是一个元组 (tuple)，比如 (1, '红烧肉', '硬菜')
            # food[0] 是 id, food[1] 是 name, food[2] 是 category
            print(f"ID:{food[0]} | 菜名: {food[1]} | 分类: {food[2]}")

    conn.close()

def pick_any_food():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    user_input = input("今晚吃几个菜：")

    try:
        num = int(user_input)

        if num <= 0:
            print("吃麦当劳。")
            return

        #？是num
        sql = "SELECT * FROM foods ORDER BY RANDOM() LIMIT ?"

        cursor.execute(sql,(num,))

        results = cursor.fetchall()

        if results:
            print("既然你诚心诚意地问了，那我大发慈悲的告诉你，喵喵喵。")
            print("-" * 30)
            for i, food in enumerate(results, 1):
                print(f"{i}: {food[1]} ({food[2]})")
            print("-" * 30)

            if len(results) < num:
                print(f"这是我最后的{len(results)}个菜了,收下吧！！")
        else:
            print("菜单是空的，找找AI吧")
        
    except ValueError:
        print("请输入数字。")

    conn.close()

