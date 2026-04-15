"""
LiteLLM 统一调用接口
"""
import litellm
from typing import List, Dict
from config import get_model_config

class LLMClient:
    """统一的 LLM 调用客户端，支持多个 AI 模型提供商"""

    def __init__(self):
        self.model, self.api_key = get_model_config()
        # 设置 API key 到环境变量（LiteLLM 会自动读取）
        import os
        config_key_env = None
        for provider, config in __import__('config').MODEL_CONFIGS.items():
            if config["model"] == self.model:
                config_key_env = config["api_key_env"]
                break
        if config_key_env:
            os.environ[config_key_env] = self.api_key

    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        调用 LLM 生成响应

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            temperature: 温度参数（0-1）
            max_tokens: 最大 token 数

        Returns:
            str: LLM 生成的响应文本
        """
        try:
            response = litellm.completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ LLM call failed: {e}")
            raise
