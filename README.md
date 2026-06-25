# 企业综合信息查询 Agent

基于 LangChain Tool Calling Agent 的智能问答系统。

## MVP 功能

- 天气查询（高德 API）
- A 股股票查询（AkShare）
- 内部资料查询（占位，待扩展）

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY、AMAP_API_KEY

# 启动
streamlit run app.py
```

## 项目结构

```
├── app.py                  # 入口
├── config/settings.py      # 配置
├── agent/agent_factory.py  # Agent 工厂
├── tools/                  # LangChain 工具
├── services/               # 外部 API 封装
├── ui/                     # Streamlit 组件
└── tests/                  # 测试
```
