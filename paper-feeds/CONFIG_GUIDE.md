# 配置指南 (Configuration Guide)

本项目使用 `config.toml` 进行配置管理。你可以通过修改此文件来自定义各种行为。

## 配置文件位置

`config.toml` 位于项目根目录。

## 配置项说明

### 1. 通用设置 (`[general]`)

```toml
[general]
# 保留论文的天数（也是缓存 summary 的时间）
days_back = 7

# 数据存储路径
data_dir = "data"
papers_file = "papers.json"
failed_file = "failed.json"
```

**说明：**
- `days_back`: 超过这个天数的论文会被自动删除，同时也决定了从 arXiv/IACR 抓取多少天内的论文
- 修改为 30 可以保留一个月的论文记录

### 2. arXiv 抓取设置 (`[fetchers.arxiv]`)

```toml
[fetchers.arxiv]
# 要抓取的 arXiv 分类
categories = ["cs.CR", "cs.AI", "cs.LG", "cs.CL"]

# 请求间隔（秒）- arXiv 建议 3 秒以上
delay = 3.0

# 每个分类最多抓取的论文数
max_results = 500

# 每次请求返回的论文数
batch_size = 100
```

**常用 arXiv 分类：**
- `cs.CR` - Cryptography and Security（密码学与安全）
- `cs.AI` - Artificial Intelligence（人工智能）
- `cs.LG` - Machine Learning（机器学习）
- `cs.CL` - Computation and Language（NLP）
- `cs.CV` - Computer Vision（计算机视觉）
- `stat.ML` - Machine Learning (Statistics)

### 3. IACR 抓取设置 (`[fetchers.iacr]`)

```toml
[fetchers.iacr]
# 请求间隔（秒）
delay = 2.0
```

### 4. AI 摘要生成设置 (`[summarizer]`)

```toml
[summarizer]
# 使用的模型
model = "qwen-plus"

# 最大生成 token 数
max_tokens = 500

# 温度参数（0-1，越高越随机）
temperature = 0.7

# API 请求超时（秒）
timeout = 60

# API 调用间隔（秒）
rate_limit_delay = 1.0

# 失败重试次数
max_retries = 3

# 重试间隔（秒）
retry_delay = 5.0
```

**可用模型：**
- `qwen-turbo` - 最快，适合简单任务
- `qwen-plus` - 平衡性能和质量（默认）
- `qwen-max` - 最强性能，但更慢更贵

### 5. 双语摘要支持 🆕

**重要更新：** 系统现在自动生成**中英文双语摘要**！

- ✅ UI 默认显示**中文摘要**
- ✅ 可通过下拉菜单切换到**英文摘要**
- ✅ 双语摘要都支持 Markdown 格式
- ✅ 数据文件中包含 `summary_zh` 和 `summary_en` 两个字段

**双语 Prompt 修改：**

双语 prompt 在 `scripts/summarizer.py` 的 `_create_bilingual_prompt()` 方法中定义，以确保稳定的格式解析。如需修改双语摘要的风格，请直接编辑该文件。

### 6. 自定义 Prompt (`[summarizer.prompt_template]`)

**注意：** `config.toml` 中的 `prompt_template` 现在主要用于向后兼容。实际使用的是双语 prompt。

**默认双语 Prompt（在代码中）：**
- 中文摘要：详细解读论文的背景、方法、主要发现和创新点
- 英文摘要：简洁概括论文的核心贡献和关键结果（3-5句话）
- 严格遵循 `[中文摘要]` 和 `[English Summary]` 标记分隔

**单语 Prompt 配置（备用）：**
```toml
prompt_template = """你是一位精通各领域前沿研究的学术文献解读专家，面对一篇给定的论文，请你高效阅读并迅速提取出其核心内容。要求在解读过程中，先对文献的背景、研究目的和问题进行简明概述，再详细梳理研究方法、关键数据、主要发现及结论，同时对新颖概念进行通俗易懂的解释，帮助读者理解论文的逻辑与创新点；最后，请对文献的优缺点进行客观评价，并指出可能的后续研究方向。整体报告结构清晰、逻辑严谨。

Title: {title}

Abstract: {abstract}

Provide a concise summary:"""
```

**简洁英文版：**
```toml
prompt_template = """Please summarize this research paper in 3-5 sentences. Focus on the main contribution, methods, and key results.

Title: {title}

Abstract: {abstract}

Provide a concise summary:"""
```

### 7. 关键词过滤 (`[keywords]`)

```toml
[keywords]
# 关键词文件路径
file = "keywords.txt"
```

**关键词语法：**
- 每行一个 OR 条件
- 同一行多个词为 AND 条件
- `#` 开头为注释

**示例 (keywords.txt)：**
```
# 匹配包含 "llm" 或 "gpt" 的论文
llm
gpt

# 匹配同时包含 "neural" 和 "backdoor" 的论文
neural backdoor

# 匹配联邦学习相关论文
federated learning
```

## 常见使用场景

### 场景 1：保留更长时间的论文

修改 `config.toml`：
```toml
[general]
days_back = 30  # 改为 30 天
```

### 场景 2：只关注密码学论文

修改 `config.toml`：
```toml
[fetchers.arxiv]
categories = ["cs.CR"]  # 只保留密码学分类
```

### 场景 3：使用更快的模型

修改 `config.toml`：
```toml
[summarizer]
model = "qwen-turbo"  # 使用更快的模型
rate_limit_delay = 0.5  # 减少延迟
```

### 场景 4：生成简短摘要

修改 `config.toml`：
```toml
[summarizer]
max_tokens = 200  # 限制输出长度
prompt_template = """Summarize this paper in 1-2 sentences focusing only on the main contribution.

Title: {title}

Abstract: {abstract}

Summary:"""
```

### 场景 5：中文输出

修改 `config.toml`：
```toml
[summarizer]
prompt_template = """请用2-3句中文总结这篇论文的核心贡献。

标题: {title}

摘要: {abstract}

总结："""
```

## 验证配置

修改配置后，可以本地测试：

```bash
pip install -r requirements.txt
export DASHSCOPE_API_KEY="your-key"
python scripts/main.py
```

查看 `data/papers.json` 确认效果。

## 注意事项

1. **API 配额限制**：减少 `rate_limit_delay` 可能导致超出 API 限制
2. **arXiv 限制**：`delay` 不要小于 3 秒，否则可能被封禁
3. **缓存时间**：修改 `days_back` 不会影响已有数据，只影响新抓取的论文
4. **Prompt 长度**：过长的 prompt 会消耗更多 tokens
