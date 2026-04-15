"""
LiteLLM 统一调用接口
"""
import litellm
from typing import List, Dict
from config import get_model_config

class LLMClient:
    """统一的 LLM 调用客户端，支持多个 AI 模型提供商"""

    def __init__(self):
        self.model, self.api_key, self.base_url = get_model_config()

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
            # 构建调用参数
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "api_key": self.api_key,
                # 对于自定义 base_url，使用 custom_llm_provider
                "custom_llm_provider": "openai" if self.base_url else None
            }
            
            # 如果有 base_url，添加到参数中
            if self.base_url:
                params["api_base"] = self.base_url
            
            response = litellm.completion(**params)
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ LLM call failed: {e}")
            raise
