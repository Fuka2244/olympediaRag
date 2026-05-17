import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# ====== 1. 本地模型路径 ======
model_path = "F:\Models\sqlcoder"   # 改成你的路径

# ====== 2. 4-bit 量化配置 ======
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",      # 推荐 nf4
    bnb_4bit_compute_dtype=torch.float16
)

# ====== 3. 加载 tokenizer ======
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# ====== 4. 加载模型（4bit） ======
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=bnb_config,
    device_map="cuda",
    trust_remote_code=True
)
print("✓ 模型加载完成\n")
# ====== 5. Prompt ======
prompt = """### Task
Generate a SQL query to answer the following question:
"Which Ethiopian men have won the Olympic marathon?"

### Database Schema
The query will run on a database with the following schema:
CREATE TABLE athletes (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(100),
    gender VARCHAR(10)
);

CREATE TABLE results (
    athlete_id INT,
    event_id INT,
    medal VARCHAR(20)
);

CREATE TABLE events (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    year INT
);

### note
- 'Ethiopian' corresponds to country = 'Ethiopia'
- 'men' corresponds to gender = 'M'
- 'Olympic marathon' refers to event name = 'Marathon'
- 'won' means medal = 'Gold'

### SQL
SELECT"""

# ====== 6. 编码 ======
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# ====== 7. 推理 ======
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=False,
        temperature=0.0
    )

# ====== 8. 解码 ======
result = tokenizer.decode(outputs[0], skip_special_tokens=True)

# ====== 9. 提取 SQL ======
sql = result[len(prompt):].strip()

print("===== Generated SQL =====")
print(sql)