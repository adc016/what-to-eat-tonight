import sqlite3
import ai_chef
import cook

# def add_food(food_name, food_category):
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     # 使用占位符?
#     sql = "INSERT INTO foods (name, category) VALUES (?, ?)"
#     cursor.execute(sql, (food_name, food_category))

#     #保存
#     conn.commit()
#     conn.close()
#     print(f"成功把{food_name}加入菜单")

def ai_interaction_menu():
    while True:
        print("\n" + "="*30)
        print("🤖 AI 智能厨房中心")
        print("1. 💡 帮我想几个菜（批量生成 + 一键入库）")
        print("2. 📖 我不会做，教教我（查询食谱）")
        print("3. 🎲 就在家吃 (随机抽取我的菜单)")
        print("4. 📋 看看冰箱 (查看我的菜单)")
        print("5. 📝 手动加菜 (手动录入)")
        print("0. 🔙 返回主菜单")
        
        choice = input("👉 请选择功能：")
        
        if choice == '1':
            flavor = input("想吃什么口味？(默认：家常菜)：") or "家常菜"
            # 1. 调用 AI 生成列表
            dishes = ai_chef.generate_dishes(count=5, flavor=flavor)
            
            if dishes:
                print(f"\n✨ AI 推荐了以下菜品：")
                for i, dish in enumerate(dishes, 1):
                    print(f"{i}. {dish}")
                
                print("\n要做什么？")
                print("可以直接输入序号保存到菜单（例如输入 '1 3' 保存第1和第3个）")
                print("或者直接回车放弃。")
                
                # 2. 用户多选逻辑
                user_picks = input("👉 请输入序号：")
                if user_picks:
                    indices = user_picks.split() # 把 "1 3" 切割成 ['1', '3']
                    for idx in indices:
                        try:
                            # 列表索引是从0开始，所以要减1
                            real_index = int(idx) - 1
                            if 0 <= real_index < len(dishes):
                                selected_dish = dishes[real_index]
                                # 自动保存进数据库
                                cook.add_food(selected_dish, f"AI推荐-{flavor}")
                            else:
                                print(f"⚠️ 序号 {idx} 不存在")
                        except ValueError:
                            print(f"⚠️ {idx} 不是数字")
                            
        elif choice == '2':
            dish_name = input("你想学哪道菜？：")
            # 3. 调用 AI 获取详情
            recipe = ai_chef.get_recipe(dish_name)
            
            if isinstance(recipe, dict): # 如果成功解析成字典
                print("\n" + "*"*40)
                print(f"🍲 【{dish_name}】 烹饪指南")
                print("-" * 20)
                print("🛒 准备材料：")
                for item in recipe['ingredients']:
                    print(f"  - {item}")
                
                print("\n🍳 烹饪步骤：")
                for i, step in enumerate(recipe['steps'], 1):
                    print(f"  {i}. {step}")
                
                print(f"\n⚠️ 核心秘诀：{recipe['tips']}")
                print("*"*40)
            else:
                # 如果解析失败，直接打印 AI 回复的原文
                print(recipe)
        
        elif choice == '3':
            cook.pick_any_food()
        
        elif choice == '4':
            cook.show_menu()
        
        elif choice == '5':
            cook.add_food()
                
        elif choice == '0':
            break

# 记得在你的 main_menu() 里把之前的 '2' 选项改成调用 ai_interaction_menu()
if __name__ == '__main__':
    ai_interaction_menu()