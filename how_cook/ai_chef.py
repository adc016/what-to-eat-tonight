import requests
import json
import re

# 1. 新增函数：读取 Key
def get_api_key():
    try:
        # 尝试打开 .env 文件
        with open('.env', 'r') as f:
            for line in f:
                # 找到包含 DEEPSEEK_API_KEY= 的那一行
                if line.startswith('DEEPSEEK_API_KEY='):
                    # 分割并返回 Key，去掉空格和换行符
                    return line.split('=', 1)[1].strip()
        print("❌ 警告：在 .env 文件中未找到 DEEPSEEK_API_KEY。")
        return None
    except FileNotFoundError:
        print("❌ 错误：未找到 .env 配置文件，无法加载 API Key。")
        return None

# 2. 调用 Key
API_URL = "https://api.deepseek.com/chat/completions"
# 将原来的硬编码 API_KEY 替换成函数调用
API_KEY = get_api_key()

def ask_ai(messages):
    # 准备“信封头” (Headers)
    # 告诉服务器：我是来送数据的(json)，这是我的身份证明(Bearer Token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 准备“信件内容” (Payload/Data)
    # 这是所有 AI API 通用的标准格式
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        #创意程度0.7
        "temperature": 0.7
    }

    try:
        #发送请求（POST）
        #requests.post(地址，头部信息，数据内容)
        response = requests.post(API_URL, headers = headers, json = data)

        #是否发送成功(状态码200表示成功)
        if response.status_code == 200:
            #解析回信
            #标准路径
            result = response.json()
            ai_reply = result['choices'][0]['message']['content']
            return ai_reply
        else:
            return f"呼叫失败，错误代码：{response.status_code}，原因：{response.text}"
        
    except Exception as e:
        return f"网络出问题了：{e}"

def clean_json_string(text):
    """清洗AI返回的字符串，提取JSON部分"""
    match = re.search(r'```json(.*?)```',text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_dishes(count = 5, flavor = '家常菜'):
    print(f"AI 正在疯狂翻阅菜谱，为您构思 {count} 道 {flavor}...")

    prompt = f"""
    请推荐 {count} 道 {flavor}。
    【重要】必须严格只返回一个 JSON 格式的字符串列表 (List of strings)。
    不要包含任何其他问候语或解释。
    格式范例：["番茄炒蛋", "红烧肉", "凉拌黄瓜"]
    """

    reply = ask_ai([{"role": "user", "content": prompt}])

    if reply:
        try:
            #清洗并把字符串变成Python列表
            clean_reply = clean_json_string(reply)
            dish_list = json.loads(clean_reply)
            return dish_list
        except json.JSONDecodeError:
            print("AI 没听话，返回的不是标准 JSON，解析失败。")
            print("AI 说：", reply)
            return []
    return []

def get_recipe(dish_name):
    print(f"正在询问{dish_name}的做法...")

    prompt = f"""
    请教我做【{dish_name}】。
    请严格按照以下 JSON 格式返回：
    {{
        "ingredients": ["材料1", "材料2"],
        "steps": ["第一步...", "第二步..."],
        "tips": "注意事项..."
    }}
    不要返回多余的文字。
    """

    reply = ask_ai([{"role": "user", "content": prompt}])

    if reply:
        try:
            clean_reply = clean_json_string(reply)
            recipe_data = json.loads(clean_reply)
            return recipe_data
        except:
            print("解析食谱失败，直接显示原文：")
            return reply 
    return None
