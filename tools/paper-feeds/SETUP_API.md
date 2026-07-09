# API密钥设置指南

本项目默认使用**阿里云DashScope（通义千问）**进行论文摘要生成。
AI 摘要也可以关闭，或通过配置替换为 DashScope-compatible 的 LLM endpoint。

## 获取API密钥

1. 访问 https://dashscope.console.aliyun.com/
2. 注册/登录阿里云账号
3. 进入控制台
4. 创建API-KEY
5. 复制生成的API密钥

## 在GitHub中设置密钥

1. 进入你的GitHub仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加密钥:
   - Name: `PAPER_FEEDS_LLM_API_KEY`
   - Value: 你的DashScope API密钥
5. 点击 **Add secret**

旧名称 `DASHSCOPE_API_KEY` 和 `MODELSCOPE_API_KEY` 仍然兼容。
如果只想抓论文、不调用 LLM，可以在 **Settings → Secrets and variables → Actions → Variables**
中添加：

- Name: `PAPER_FEEDS_AI_SUMMARY_ENABLED`
- Value: `false`

如果要改 LLM endpoint，可以添加 Repository Variable：

- Name: `PAPER_FEEDS_LLM_API_URL`
- Value: 你的 DashScope-compatible endpoint URL

## 免费额度

DashScope提供免费试用额度:
- qwen-plus模型: 每天有一定的免费调用次数
- 具体额度请查看官方文档

## 本地测试

如果你想在本地测试:

```bash
export PAPER_FEEDS_LLM_API_KEY="your-api-key-here"
python tools/paper-feeds/scripts/main.py
```

关闭 AI 摘要：

```bash
export PAPER_FEEDS_AI_SUMMARY_ENABLED=false
python tools/paper-feeds/scripts/main.py
```

自定义 endpoint：

```bash
export PAPER_FEEDS_LLM_API_URL="https://example.com/api/v1/services/aigc/text-generation/generation"
export PAPER_FEEDS_LLM_API_KEY="your-api-key-here"
python tools/paper-feeds/scripts/main.py
```

## 故障排除

如果遇到401错误:
- 检查API密钥是否正确
- 确认在GitHub Secrets中名称为 `PAPER_FEEDS_LLM_API_KEY`
- 检查是否有足够的API调用额度

如果遇到403错误:
- 你的账号可能需要实名认证
- 检查API调用配额
