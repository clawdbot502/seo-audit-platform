"""
LiteLLM 统一调用接口
"""
import litellm
from typing import List, Dict
from config import get_model_config

class LLMClient:
    """统一的 LLM 调用客户端，支持多个 AI 模型提供商和自定义 Base URL"""

    def __init__(self):
        self.model, self.api_key, self.base_url, self.fallback_models = get_model_config()

    def _call_model(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """内部方法：调用指定模型"""
        kwargs = {
            "model": model,
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
        if self.base_url:
            kwargs["api_base"] = self.base_url

        response = litellm.completion(**kwargs)
        return response.choices[0].message.content

    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        调用 LLM 生成响应，支持 fallback 模型自动切换

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            temperature: 温度参数（0-1）
            max_tokens: 最大 token 数

        Returns:
            str: LLM 生成的响应文本
        """
        # 尝试主模型
        try:
            return self._call_model(
                self.model, system_prompt, user_prompt, temperature, max_tokens
            )
        except Exception as e:
            print(f"❌ LLM call failed with primary model {self.model}: {e}")

            # 尝试 fallback 模型
            if self.fallback_models:
                for fallback_model in self.fallback_models:
                    print(f"🔄 Trying fallback model: {fallback_model}")
                    try:
                        return self._call_model(
                            fallback_model, system_prompt, user_prompt, temperature, max_tokens
                        )
                    except Exception as fb_error:
                        print(f"❌ Fallback model {fallback_model} failed: {fb_error}")
                        continue

            raise Exception(f"All models failed. Primary error: {e}")
