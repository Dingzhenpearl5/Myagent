# 企业综合信息查询 Agent

基于 LangChain / LangGraph Tool Calling Agent 和 Streamlit 的企业信息查询助手，面向“赛道一：智能体（Agent）构建”演示场景。

## 功能亮点

- 企业内部制度问答：检索 `data/internal_docs/` 下的本地 Markdown / TXT / PDF / Word 文档，并返回来源。
- 多工具查询：支持天气查询、高德 API 城市天气和 A 股股票查询。
- 稳定降级：股票主行情源不可用时自动切换备用数据源。
- 演示友好：内置考勤、报销、信息安全与 AI 使用规范等虚构示例文档。
- 本地可运行：通过 Streamlit 提供聊天式 Demo，适合评委直接体验。

## 示例问题

- `怎么打卡？`
- `报销多久到账？`
- `可以使用 AI 工具处理客户资料吗？`
- `你可以查什么内部资料呢？`
- `北京今天的天气怎么样？`
- `查询 000001 当前股价`

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY、AMAP_API_KEY

# 启动 Demo
streamlit run app.py
```

Windows PowerShell 可使用：

```powershell
Copy-Item .env.example .env
streamlit run app.py
```

## 本地知识库

内部资料默认读取 `data/internal_docs/`，支持 `.md`、`.txt`、`.pdf` 和 `.docx` 文件。新增制度文档后无需改代码，重启或刷新应用即可检索。

当前示例资料包括：

- `员工手册.md`
- `考勤与打卡制度.md`
- `报销流程说明.md`
- `信息安全与AI使用规范.md`

## 测试

```bash
python -m pytest tests/test_agent.py tests/test_rag.py -q
python -m pytest tests/test_stock.py -q
```

## 项目结构

```text
├── app.py                  # Streamlit 入口
├── agent/agent_factory.py  # Agent 创建与调用入口
├── config/settings.py      # 环境变量配置
├── data/internal_docs/     # 本地内部知识库
├── services/               # 天气、股票、RAG 等服务封装
├── tools/                  # LangChain 工具定义
├── ui/                     # Streamlit 页面组件
└── tests/                  # 回归测试
```

## 参赛说明

本项目展示了一个可运行、可演示的企业信息查询 Agent：用户可以在聊天界面提出自然语言问题，系统根据问题类型调用天气、股票或本地知识库能力。内部资料类问题会直接返回本地检索结果和来源，减少模型幻觉和“资料存在但回答查不到”的风险。
