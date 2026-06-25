import os
from dotenv import load_dotenv

load_dotenv()

# DeepSeek LLM 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# 高德地图 API 配置
AMAP_API_KEY = os.getenv("AMAP_API_KEY", "")

# TCL 知识库配置
TCL_TOKEN = os.getenv("TCL_TOKEN", "")
TCL_KNOWLEDGE_ID = os.getenv("TCL_KNOWLEDGE_ID", "")

# 模型参数
MODEL_NAME = "deepseek-chat"
TEMPERATURE = 0
MAX_TOKENS = 1024
