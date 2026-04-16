"""
配置文件：支持多个 AI 模型提供商
支持灵活模式（MODEL_NAME + API_KEY + BASE_URL）和兼容模式
"""
import os
from typing import Tuple, List

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
        "model": "K2.6-code-preview",
        "api_key_env": "KIMI_API_KEY",
        "base_url": "https://api.kimi.com/coding/"
    }
}


def _parse_fallback_models(fallback_str: str | None) -> List[str]:
    """解析逗号分隔的 fallback 模型列表"""
    if not fallback_str:
        return []
    return [m.strip() for m in fallback_str.split(",") if m.strip()]


def get_model_config() -> Tuple[str, str, str, List[str]]:
    """
    获取当前配置的模型、API key、Base URL 和 fallback 模型列表

    支持两种配置模式：
    1. 灵活模式（推荐）：MODEL_NAME + API_KEY + BASE_URL（可选）+ FALLBACK_MODELS（可选）
    2. 兼容模式：MODEL_PROVIDER + API_KEY + BASE_URL

    Returns:
        Tuple[str, str, str, List[str]]: (model_name, api_key, base_url, fallback_models)

    Raises:
        ValueError: 如果配置缺失或无效
    """
    # ===== 模式 1：灵活模式（优先） =====
    model = os.getenv("MODEL_NAME") or os.getenv("AUDIT_MODEL")
    api_key = os.getenv("API_KEY") or os.getenv("AUDIT_API_KEY")
    base_url = os.getenv("BASE_URL") or os.getenv("AUDIT_BASE_URL")
    fallback_models = _parse_fallback_models(
        os.getenv("FALLBACK_MODELS") or os.getenv("AUDIT_FALLBACK_MODELS")
    )

    if model and api_key:
        print(f"✓ Using model: {model} (base_url: {base_url or 'default'}, fallbacks: {len(fallback_models)})")
        return model, api_key, base_url or "", fallback_models

    # ===== 模式 2：兼容模式 =====
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

    # 获取 base_url（如果有）
    base_url = os.getenv("BASE_URL") or os.getenv(f"{provider.upper()}_BASE_URL") or config.get("base_url", "")

    fallback_models = _parse_fallback_models(
        os.getenv("FALLBACK_MODELS") or os.getenv("AUDIT_FALLBACK_MODELS")
    )

    if base_url:
        print(f"✓ Using model: {config['model']} (provider: {provider}, base_url: {base_url}, fallbacks: {len(fallback_models)})")
    else:
        print(f"✓ Using model: {config['model']} (provider: {provider}, fallbacks: {len(fallback_models)})")

    return config["model"], api_key, base_url, fallback_models
