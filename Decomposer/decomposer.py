import json
import os
import dashscope
from dashscope import Generation

def load_conf():
    with open('config.json', 'r', encoding='utf-8') as f:
        conf = json.load(f)
    
    api_key = os.getenv('DASH_SCOPE_API_KEY')
    if api_key:
        conf['api_key'] = api_key
    elif not conf.get('api_key') or conf['api_key'] == 'sk-':
        raise ValueError('API Key未设置，请在环境变量中设置DASH_SCOPE_API_KEY或在config.json中配置')
    
    return conf

def load_prompts():
    with open('prompts.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def build_promp(conf, prom, query):
    msgs = [{"role": "system", "content": prom['sys_prompt']}]
    for ex in prom['examples']:
        msgs.append({"role": "user", "content": ex['user']})
        msgs.append({"role": "assistant", "content": ex['assist']})
    user_cont = f"{prom['instr']}\n\n{prom['out_fmt']}\n\n用户问题: {query}"
    msgs.append({"role": "user", "content": user_cont})
    return msgs

def call_qwen(conf, msgs):
    dashscope.api_key = conf['api_key']
    resp = Generation.call(
        model=conf['model'],
        messages=msgs,
        temperature=conf['temp']
    )
    if resp.status_code == 200:
        return resp.output.text
    else:
        raise Exception(f"API错误: {resp.message}")

def parse_resp(text):
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    return json.loads(text.strip())

def valid_subqs(data, max_q):
    subqs = data.get('sub_questions', [])
    if len(subqs) > max_q:
        data['sub_questions'] = subqs[:max_q]
    return data

def decomposer(query):
    conf = load_conf()
    prom = load_prompts()
    msgs = build_promp(conf, prom, query)
    raw_out = call_qwen(conf, msgs)
    data = parse_resp(raw_out)
    
    data = valid_subqs(data, conf['max_subq'])
    
    result = {
        'original_question': data.get('original_question', query),
        'sub_questions': data.get('sub_questions', []),
        'combination': data.get('combination', {})
    }
    
    return result

def main():
    print("=" * 50)
    print("问题分解器 (奥林匹克QA)")
    print("=" * 50)
    test_qs = [
        "Usain Bolt在哪些奥运会上获得了100米金牌？",
        "对比尤塞恩·博尔特和卡尔·刘易斯的奥运生涯，谁的奥运金牌总数更多？",
        "2020年东京奥运会男子100米冠军是谁？他的决赛成绩是多少？",
        "中国在2020年东京奥运会和2016年里约奥运会分别获得了多少枚金牌？"
    ]
    for i, q in enumerate(test_qs, 1):
        print(f"\n[测试 {i}]")
        print(f"原始问题: {q}")
        try:
            res = decomposer(q)
            print(f"组合类型: {res.get('combination', {}).get('type', '未指定')}")
            print(f"组合描述: {res.get('combination', {}).get('description', '无')}")
            if res.get('combination', {}).get('dependencies'):
                print(f"依赖关系: 子问题{res['combination']['dependencies']}")
            print("子问题列表:")
            for j, sq in enumerate(res['sub_questions'], 1):
                print(f"  {j}. {sq}")
        except Exception as e:
            print(f"错误: {e}")
        print("-" * 50)
    while True:
        print("\n输入问题 (q退出):")
        uq = input().strip()
        if uq.lower() == 'q':
            break
        if not uq:
            continue
        try:
            res = decomposer(uq)
            print(f"\n组合类型: {res.get('combination', {}).get('type', '未指定')}")
            print(f"组合描述: {res.get('combination', {}).get('description', '无')}")
            if res.get('combination', {}).get('dependencies'):
                print(f"依赖关系: 依赖子问题索引 {res['combination']['dependencies']}")
            print("子问题列表:")
            for j, sq in enumerate(res['sub_questions'], 1):
                print(f"  {j}. {sq}")
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    main()