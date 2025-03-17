from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import time
from datetime import datetime
import io

# 设置模拟模式（不需要加载大型模型）
SIMULATION_MODE = False

app = Flask(__name__)

# 全局变量，用于存储模型和分词器
model = None
tokenizer = None

# 问题列表
QUESTIONS = [
    {
        "id": 1,
        "text": "你最喜欢的学科是什么？为什么它吸引你？",
        "placeholder": "例如：数学、科学、艺术、历史等"
    },
    {
        "id": 2,
        "text": "在课外，你有什么爱好或活动让你感到充实？",
        "placeholder": "例如：体育、音乐、志愿服务、编程等"
    },
    {
        "id": 3,
        "text": "你认为自己的三个主要优势是什么？",
        "placeholder": "例如：创造力、分析能力、沟通能力等"
    },
    {
        "id": 4,
        "text": "你希望在大学里学习什么专业？为什么？",
        "placeholder": "分享你的想法和原因"
    },
    {
        "id": 5,
        "text": "十年后，你希望自己在做什么？",
        "placeholder": "描述你理想的职业或生活状态"
    },
    {
        "id": 6,
        "text": "你认为AI时代最重要的技能是什么？",
        "placeholder": "思考未来社会需要什么样的能力"
    },
    {
        "id": 7,
        "text": "你如何看待个人品牌的重要性？",
        "placeholder": "分享你对个人形象和影响力的看法"
    },
    {
        "id": 8,
        "text": "有没有特定的社会问题或挑战是你希望解决的？",
        "placeholder": "例如：环境、教育、健康等领域的问题"
    }
]

def load_model():
    """加载Llama 3模型和分词器，或在模拟模式下返回True"""
    global model, tokenizer
    
    # 如果在模拟模式下，直接返回成功
    if SIMULATION_MODE:
        print("运行在模拟模式，跳过模型加载")
        return True
    
    # 以下代码在非模拟模式下执行
    # 需要导入必要的库
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
    if model is None or tokenizer is None:
        print("正在加载模型，这可能需要几分钟...")
        
        # 使用Meta的Llama 3模型
        model_name = "meta-llama/Llama-3-8B-Chinese"
        
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
            )
            print("模型加载完成！")
        except Exception as e:
            print(f"模型加载失败: {e}")
            # 使用备用模型
            try:
                model_name = "THUDM/chatglm3-6b"
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    device_map="auto",
                )
                print("备用模型加载完成！")
            except Exception as e:
                print(f"备用模型加载也失败了: {e}")
                return False
    
    return True

def generate_report(answers):
    """使用Llama 3生成个性化报告或在模拟模式下返回示例报告"""
    if not load_model():
        return "模型加载失败，无法生成报告。请稍后再试。"
    
    # 构建提示
    prompt = "你是一位专业的教育顾问和职业规划专家。根据以下高中生的回答，分析他/她应该建立什么样的个人品牌，以在AI时代取得成功。请提供详细的分析和具体的建议。\n\n"
    
    for q in QUESTIONS:
        question_id = q["id"]
        question_text = q["text"]
        answer = answers.get(str(question_id), "未回答")
        prompt += f"问题：{question_text}\n回答：{answer}\n\n"
    
    prompt += "请提供一份全面的个人品牌分析报告，包括以下部分：\n"
    prompt += "1. 个人特质分析\n"
    prompt += "2. 核心优势和独特卖点\n"
    prompt += "3. 潜在职业方向\n"
    prompt += "4. 建立个人品牌的具体步骤\n"
    prompt += "5. 在AI时代脱颖而出的策略\n\n"
    prompt += "所有内容必须用中文输出，并针对高中生的实际情况给出实用建议。"
    
    # 如果在模拟模式下，返回示例报告
    if SIMULATION_MODE:
        # 从答案中获取一些信息来个性化模拟报告
        interests = answers.get("1", "科学和技术")
        hobbies = answers.get("2", "编程和阅读")
        strengths = answers.get("3", "创新思维")
        major = answers.get("4", "计算机科学")
        future = answers.get("5", "技术领域的领导者")
        
        return f"""一、个人特质分析

根据你的回答，我们可以看出你是一个对{interests}充满热情的学生。你展现出了强烈的好奇心和学习欲望，这在AI时代是非常宝贵的特质。你喜欢{hobbies}的习惯也表明你善于自主学习和探索新知识。

你对未来的规划显示出了清晰的目标感，希望在{major}领域深造，并在十年后成为{future}。这种长远的视野和明确的方向感是你的重要特质。

二、核心优势和独特卖点

1. 你对{interests}的深入兴趣使你在这一领域具有独特视角
2. 你展现出的{strengths}能力是你的核心竞争力
3. 你的自我驱动力和学习能力将帮助你在快速变化的环境中保持领先

三、潜在职业方向

考虑到你的兴趣和优势，以下职业方向可能适合你：

- 人工智能研究员或工程师
- 数据科学家
- 产品经理（科技领域）
- 创新顾问
- 教育科技专家

四、建立个人品牌的具体步骤

1. 创建专业社交媒体账号，分享你在{interests}领域的见解和学习心得
2. 参与相关比赛、黑客马拉松或开源项目，展示你的实际能力
3. 建立个人博客或网站，深入探讨你感兴趣的话题
4. 寻找实习或志愿者机会，积累实际经验
5. 与行业专业人士建立联系，主动寻求指导

五、在AI时代脱颖而出的策略

在AI工具变得普遍的时代，以下策略将帮助你脱颖而出：

1. 培养人类独有的能力：创造力、批判性思维、情感智能和跨学科思维
2. 学会与AI协作，而不是与之竞争
3. 持续学习新技能，保持知识更新
4. 发展“T型”技能组合：在一个领域深入专精，同时具备广泛的跨领域知识
5. 建立强大的人际网络和协作能力

记住，真正的个人品牌来自于真实性和一致性。找到你真正热爱的事物，并在此基础上构建你的专业形象。"""
    
    # 如果不是模拟模式，使用实际模型生成
    # 需要导入必要的库
    import torch
    
    # 生成回答
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_length=4096,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 提取生成的报告部分（去除原始提示）
    report = response[len(prompt):].strip()
    
    # 如果报告为空，返回错误信息
    if not report:
        return "生成报告时出现错误，请重试。"
    
    return report

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html', questions=QUESTIONS)

@app.route('/generate', methods=['POST'])
def generate():
    """处理表单提交并生成报告"""
    try:
        # 获取表单数据
        data = request.json
        answers = data.get('answers', {})
        student_name = data.get('name', '同学')
        
        # 生成报告
        report = generate_report(answers)
        
        # 创建响应
        response = {
            'success': True,
            'report': report,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 尝试预加载模型
    try:
        load_model()
    except Exception as e:
        print(f"预加载模型失败: {e}")
        print("应用将在第一次请求时加载模型")
    
    # Get port from environment variable (Render sets this) or default to 5001
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
