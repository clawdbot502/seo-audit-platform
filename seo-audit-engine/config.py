"""
配置文件：管理多模型支持和环境变量
"""
import os
from typing import Dict, Tuple

MODEL_CONFIGS = {
    "openai": {
        "model": "gpt-4-turbo-preview",
        "api_key_env": "OPENAI_API_KEY"
    },
    "anthropic": {
        "model": "claude-3-opus-20240229",
        "api_key_env": "ANTHROPIC_API_KEY"
    },
    "google": {
        "model": "gemini/gemini-pro",
        "api_key_env": "GOOGLE_API_KEY"
    },
    "deepseek": {
        "model": "deepseek/deepseek-chat",
        "api_key_env": "DEEPSEEK_API_KEY"
    },
    "kimi": {
        "model": "openai/K2.6-code-preview",
        "api_key_env": "KIMI_API_KEY",
        "base_url": "https://api.kimi.com/coding/"
    }
}

def get_model_config() -> Tuple[str, str]:
    """
    获取当前配置的模型和 API key

    Returns:
        Tuple[str, str]: (model_name, api_key)

    Raises:
        ValueError: 如果提供商未知或 API key 缺失
    """
    provider = os.getenv("MODEL_PROVIDER", "openai")

    if provider not in MODEL_CONFIGS:
        raise ValueError(
            f"Unknown provider: {provider}. "
            f"Available: {', '.join(MODEL_CONFIGS.keys())}"
        )

    config = MODEL_CONFIGS[provider]

    # 优先使用通用 API_KEY，其次使用特定的 API key
    api_key = os.getenv("API_KEY") or os.getenv(config["api_key_env"])

    if not api_key:
        raise ValueError(f"Missing API key: API_KEY or {config['api_key_env']}")

    # 如果配置中有 base_url，设置环境变量供 litellm 使用
    if "base_url" in config:
        base_url = os.getenv("BASE_URL") or config["base_url"]
        os.environ["OPENAI_API_BASE"] = base_url
        print(f"✓ Using model: {config['model']} (provider: {provider}, base_url: {base_url})")
    else:
        print(f"✓ Using model: {config['model']} (provider: {provider})")

    return config["model"], api_key
