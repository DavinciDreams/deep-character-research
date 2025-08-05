import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
import os
from pathlib import Path

@dataclass
class AIConfig:
    openai_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    lmstudio_base_url: str = None
    lmstudio_model: str = None
    default_provider: str = None
    default_model: str = None
    fallback_enabled: bool = None
    
    def __post_init__(self):
        """Load values from environment variables if not provided"""
        if self.openai_api_key is None:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openrouter_api_key is None:
            self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        # Log masked OpenRouter API key at startup
        if self.openrouter_api_key:
            masked = '*' * (len(self.openrouter_api_key) - 4) + self.openrouter_api_key[-4:]
            logging.info(f"OpenRouter API key loaded: {masked}")
        else:
            logging.warning("OpenRouter API key not set.")
        if self.anthropic_api_key is None:
            self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.lmstudio_base_url is None:
            self.lmstudio_base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234")
        if self.lmstudio_model is None:
            self.lmstudio_model = os.getenv("LMSTUDIO_MODEL", "local-model")
        if self.default_provider is None:
            self.default_provider = os.getenv("DEFAULT_AI_PROVIDER", "openrouter")
        if self.default_model is None:
            self.default_model = os.getenv("DEFAULT_MODEL", "nvidia/llama-3.1-nemotron-ultra-253b-v1:free")
        if self.fallback_enabled is None:
            self.fallback_enabled = os.getenv("FALLBACK_ENABLED", "true").lower() == "true"

class BaseAIProvider:
    def __init__(self, config: AIConfig):
        self.config = config
        self.session = None
        
    async def get_session(self):
        """Get or create HTTP session"""
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def close(self):
        """Close HTTP session safely"""
        if self.session and not self.session.closed:
            try:
                await self.session.close()
            except Exception as e:
                logging.warning(f"Error closing session: {e}")
            finally:
                self.session = None
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test provider connection"""
        return {"status": "error", "message": "Not implemented"}
    
    async def generate_response(self, prompt: str, model: str = None) -> Dict[str, Any]:
        """Generate response from AI provider"""
        return {"content": "Not implemented", "model": model}

class OpenAIProvider(BaseAIProvider):
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self.api_key = config.openai_api_key
        self.base_url = "https://api.openai.com/v1"
        
    async def test_connection(self) -> Dict[str, Any]:
        """Test OpenAI connection"""
        if not self.api_key:
            return {"status": "error", "message": "No API key provided"}
        
        try:
            session = await self.get_session()
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with session.get(f"{self.base_url}/models", headers=headers) as response:
                if response.status == 200:
                    return {"status": "success", "message": "Connected to OpenAI"}
                else:
                    return {"status": "error", "message": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def generate_response(self, prompt: str, model: str = None) -> Dict[str, Any]:
        """Generate response using OpenAI"""
        if not self.api_key:
            raise Exception("No OpenAI API key provided")
        
        model = model or "gpt-3.5-turbo"
        
        try:
            session = await self.get_session()
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            async with session.post(f"{self.base_url}/chat/completions", 
                                   headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    
                    return {
                        "content": content,
                        "model": model,
                        "tokens_used": result.get('usage', {}).get('total_tokens'),
                        "cost": self._calculate_cost(result.get('usage', {}), model)
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API error {response.status}: {error_text}")
                    
        except Exception as e:
            logging.error(f"OpenAI generation error: {e}")
            raise
    
    def _calculate_cost(self, usage: Dict, model: str) -> float:
        """Estimate cost based on usage"""
        if not usage:
            return 0.0
        
        # Rough cost estimates (per 1K tokens)
        costs = {
            "gpt-3.5-turbo": 0.002,
            "gpt-4": 0.03,
            "gpt-4-turbo": 0.01
        }
        
        cost_per_1k = costs.get(model, 0.002)
        total_tokens = usage.get('total_tokens', 0)
        
        return (total_tokens / 1000) * cost_per_1k

class OpenRouterProvider(BaseAIProvider):
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self.api_key = config.openrouter_api_key
        self.base_url = "https://openrouter.ai/api/v1"
        
    async def test_connection(self) -> Dict[str, Any]:
        """Test OpenRouter connection"""
        if not self.api_key:
            return {"status": "error", "message": "No API key provided"}
        
        try:
            session = await self.get_session()
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            # Log headers with masked API key
            masked_key = '*' * (len(self.api_key) - 4) + self.api_key[-4:] if self.api_key else None
            logged_headers = dict(headers)
            if masked_key:
                logged_headers["Authorization"] = f"Bearer {masked_key}"
            logging.info(f"OpenRouter request headers: {logged_headers}")
            
            async with session.get(f"{self.base_url}/models", headers=headers) as response:
                if response.status == 200:
                    return {"status": "success", "message": "Connected to OpenRouter"}
                else:
                    return {"status": "error", "message": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def generate_response(self, prompt: str, model: str = None) -> Dict[str, Any]:
        """Generate response using OpenRouter"""
        if not self.api_key:
            raise Exception("No OpenRouter API key provided")
        
        model = model or self.config.default_model
        
        try:
            session = await self.get_session()
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            # Log headers with masked API key
            masked_key = '*' * (len(self.api_key) - 4) + self.api_key[-4:] if self.api_key else None
            logged_headers = dict(headers)
            if masked_key:
                logged_headers["Authorization"] = f"Bearer {masked_key}"
            logging.info(f"OpenRouter request headers: {logged_headers}")
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            async with session.post(f"{self.base_url}/chat/completions", 
                                   headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    
                    return {
                        "content": content,
                        "model": model,
                        "tokens_used": result.get('usage', {}).get('total_tokens'),
                        "cost": 0.0  # Many OpenRouter models are free
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"OpenRouter API error {response.status}: {error_text}")
                    
        except Exception as e:
            logging.error(f"OpenRouter generation error: {e}")
            raise

class LMStudioProvider(BaseAIProvider):
    def __init__(self, config: AIConfig):
        super().__init__(config)
        self.base_url = config.lmstudio_base_url
        self.model = config.lmstudio_model
        
    async def test_connection(self) -> Dict[str, Any]:
        """Test LM Studio connection"""
        try:
            session = await self.get_session()
            async with session.get(f"{self.base_url}/v1/models") as response:
                if response.status == 200:
                    return {"status": "success", "message": "Connected to LM Studio"}
                else:
                    return {"status": "error", "message": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def generate_response(self, prompt: str, model: str = None) -> Dict[str, Any]:
        """Generate response using LM Studio"""
        model = model or self.model
        
        try:
            session = await self.get_session()
            headers = {"Content-Type": "application/json"}
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            async with session.post(f"{self.base_url}/v1/chat/completions", 
                                   headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    
                    return {
                        "content": content,
                        "model": model,
                        "tokens_used": result.get('usage', {}).get('total_tokens'),
                        "cost": 0.0  # Local inference is free
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"LM Studio API error {response.status}: {error_text}")
                    
        except Exception as e:
            logging.error(f"LM Studio generation error: {e}")
            raise

class AIProviderManager:
    def __init__(self, config: AIConfig):
        self.config = config
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available providers"""
        if self.config.openai_api_key:
            self.providers["openai"] = OpenAIProvider(self.config)
        
        if self.config.openrouter_api_key:
            self.providers["openrouter"] = OpenRouterProvider(self.config)
        
        # LM Studio doesn't require API key
        self.providers["lmstudio"] = LMStudioProvider(self.config)
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    async def test_provider_connection(self, provider_name: str) -> Dict[str, Any]:
        """Test connection to a specific provider"""
        if provider_name not in self.providers:
            return {"status": "error", "message": f"Provider {provider_name} not available"}
        
        provider = self.providers[provider_name]
        return await provider.test_connection()
    
    async def generate_response(self, provider_name: str, prompt: str, 
                              model: str = None) -> Dict[str, Any]:
        """Generate response using specified provider"""
        if provider_name not in self.providers:
            raise Exception(f"Provider {provider_name} not available")
        
        provider = self.providers[provider_name]
        return await provider.generate_response(prompt, model)
    
    async def close_all(self):
        """Close all provider sessions safely"""
        for provider_name, provider in self.providers.items():
            try:
                await provider.close()
                logging.info(f"Closed {provider_name} provider")
            except Exception as e:
                logging.warning(f"Error closing {provider_name} provider: {e}")