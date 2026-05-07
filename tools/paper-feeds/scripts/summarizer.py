"""
AI-powered bilingual paper summarizer using DashScope API for Paper Feeds.

Copyright (C) 2024-2026 Paper Pulse Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import requests
import time
from typing import Dict, Optional
import sys
import os

# Import progress utilities if available
try:
    from progress import ProgressBar

    HAS_PROGRESS = True
except ImportError:
    HAS_PROGRESS = False


class ModelScopeSummarizer:
    """Summarizes paper abstracts using DashScope API (Qwen/通义千问)."""

    # DashScope API (阿里云通义千问)
    API_URL = (
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    )
    DEFAULT_MODEL = "qwen-plus"  # Free tier available
    DEFAULT_MAX_TOKENS = 500
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_TIMEOUT = 60
    DEFAULT_RATE_LIMIT_DELAY = 1.0
    DEFAULT_PROMPT_TEMPLATE = """Please summarize this research paper in 3-5 sentences. Focus on the main contribution, methods, and key results.

Title: {title}

Abstract: {abstract}

Provide a concise summary:"""

    def __init__(
        self,
        api_key: str,
        model: str = None,
        max_retries: int = 3,
        retry_delay: float = 5.0,
        max_tokens: int = None,
        temperature: float = None,
        timeout: int = None,
        rate_limit_delay: float = None,
        prompt_template: str = None,
    ):
        """
        Initialize DashScope summarizer.

        Args:
            api_key: DashScope API key (from https://dashscope.console.aliyun.com/)
            model: Model name to use (default: qwen-plus)
            max_retries: Maximum number of retry attempts for failed requests
            retry_delay: Delay between retries in seconds
            max_tokens: Maximum tokens for response
            temperature: Sampling temperature
            timeout: Request timeout in seconds
            rate_limit_delay: Delay between API calls
            prompt_template: Custom prompt template with {title} and {abstract} placeholders
        """
        self.api_key = api_key
        self.model = model or self.DEFAULT_MODEL
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS
        self.temperature = temperature or self.DEFAULT_TEMPERATURE
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.rate_limit_delay = rate_limit_delay or self.DEFAULT_RATE_LIMIT_DELAY
        self.prompt_template = prompt_template or self.DEFAULT_PROMPT_TEMPLATE
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def summarize(self, paper: Dict) -> tuple[Optional[str], Optional[str]]:
        """
        Generate bilingual (Chinese and English) summaries for a paper.

        Args:
            paper: Paper dictionary containing title and abstract

        Returns:
            Tuple of (chinese_summary, english_summary), or (None, None) if summarization fails
        """
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")

        if not abstract:
            return None, None

        # Create prompt for bilingual summarization
        prompt = self._create_bilingual_prompt(title, abstract)

        # Try to generate summary with retries
        for attempt in range(self.max_retries):
            try:
                summary, input_tokens, output_tokens = self._call_api(prompt)
                if summary:
                    # Accumulate token usage
                    self.total_input_tokens += input_tokens
                    self.total_output_tokens += output_tokens
                    # Parse bilingual response
                    zh_summary, en_summary = self._parse_bilingual_summary(summary)
                    return zh_summary, en_summary
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        return None, None

    def _create_bilingual_prompt(self, title: str, abstract: str) -> str:
        """Create a prompt for bilingual summarization."""
        return f"""请对这篇研究论文生成中英文双语摘要。**重要：你有 {self.max_tokens} tokens 的输出限制，请合理分配给中英文两部分。**

论文标题: {title}

论文摘要: {abstract}

请按照以下格式输出（严格遵守格式，以便程序解析）：

[中文摘要]
<这里写中文摘要，约占 60-70% 篇幅，可使用Markdown格式>

[English Summary]
<这里写英文摘要，约占 30-40% 篇幅，可使用Markdown格式>

**字数分配建议（基于 {self.max_tokens} tokens 限制）：**
- 中文摘要：约 400-600 字，包含背景、方法、主要发现和创新点
- 英文摘要：约 150-250 词，简洁概括核心贡献和关键结果（3-5 sentences）

**格式要求：**
1. 必须包含且仅包含两个部分：[中文摘要] 和 [English Summary]
2. 两个标记必须完整出现，用于程序解析
3. 可以使用 Markdown 格式（## 标题、**加粗**、列表等）
4. 确保在 token 限制内完成两个摘要，不要截断"""

    def _parse_bilingual_summary(self, text: str) -> tuple[str, str]:
        """Parse bilingual summary response into Chinese and English parts."""
        import re

        # Try to find Chinese and English sections
        zh_match = re.search(
            r"\[中文摘要\]\s*\n(.*?)\n\[English Summary\]", text, re.DOTALL
        )
        en_match = re.search(r"\[English Summary\]\s*\n(.*?)$", text, re.DOTALL)

        zh_summary = zh_match.group(1).strip() if zh_match else ""
        en_summary = en_match.group(1).strip() if en_match else ""

        # Fallback: if parsing fails, split by markers or use whole text
        if not zh_summary and not en_summary:
            # Try alternative parsing
            parts = re.split(r"\[(?:中文摘要|English Summary)\]", text)
            if len(parts) >= 3:
                zh_summary = parts[1].strip()
                en_summary = parts[2].strip()
            else:
                # If all parsing fails, use the original text for both
                zh_summary = text.strip()
                en_summary = text.strip()

        return zh_summary, en_summary

    def _create_prompt(self, title: str, abstract: str) -> str:
        """Create a prompt for the summarization model."""
        return self.prompt_template.format(title=title, abstract=abstract)

    def _call_api(self, prompt: str) -> tuple:
        """
        Call DashScope API to generate summary.

        Returns:
            Tuple of (summary_text, input_tokens, output_tokens)
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "input": {"messages": [{"role": "user", "content": prompt}]},
            "parameters": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "result_format": "message",
            },
        }

        try:
            response = requests.post(
                self.API_URL,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

            result = response.json()

            # Extract summary from DashScope response format
            content = None
            if "output" in result and "choices" in result["output"]:
                choices = result["output"]["choices"]
                if choices and len(choices) > 0:
                    message = choices[0].get("message", {})
                    content = message.get("content", "").strip()

            # Extract token usage information
            input_tokens = 0
            output_tokens = 0
            if "usage" in result:
                usage = result["usage"]
                input_tokens = usage.get("input_tokens", 0)
                output_tokens = usage.get("output_tokens", 0)

            return (content, input_tokens, output_tokens)

        except requests.RequestException as e:
            raise

    def batch_summarize(self, papers: list, delay: float = None) -> tuple:
        """
        Summarize multiple papers with rate limiting and progress display.

        Args:
            papers: List of paper dictionaries
            delay: Delay between API calls to avoid rate limiting

        Returns:
            Tuple of (successful_papers, failed_papers)
        """
        if delay is None:
            delay = self.rate_limit_delay

        successful = []
        failed = []
        total = len(papers)

        # Create progress bar if available
        if HAS_PROGRESS:
            progress = ProgressBar(total, "Summarizing papers")
        else:
            progress = None

        for i, paper in enumerate(papers, 1):
            # Update progress bar or print simple progress
            if progress:
                progress.update(1)
            else:
                print(f"[{i}/{total}] Summarizing: {paper['title'][:60]}...")

            zh_summary, en_summary = self.summarize(paper)

            if zh_summary and en_summary:
                paper["summary_zh"] = zh_summary
                paper["summary_en"] = en_summary
                paper["summary"] = (
                    zh_summary  # Default to Chinese for backward compatibility
                )
                paper["summary_status"] = "success"
                successful.append(paper)
            else:
                abstract = paper.get("abstract", "")
                if abstract:
                    paper["summary"] = abstract
                    paper["summary_zh"] = abstract
                    paper["summary_en"] = abstract
                else:
                    paper["summary"] = "Summary not available"
                    paper["summary_zh"] = "摘要不可用"
                    paper["summary_en"] = "Summary not available"
                paper["summary_status"] = "failed"
                failed.append(paper)

            # Rate limiting
            if i < total:
                time.sleep(delay)

        # Finish progress bar
        if progress:
            progress.finish()

        print(
            f"\n✓ Summarization complete: {len(successful)} successful, {len(failed)} failed"
        )
        return successful, failed

    def get_usage_stats(self) -> dict:
        """
        Get token usage statistics.

        Returns:
            Dictionary with input_tokens, output_tokens, and total_tokens
        """
        return {
            'input_tokens': self.total_input_tokens,
            'output_tokens': self.total_output_tokens,
            'total_tokens': self.total_input_tokens + self.total_output_tokens
        }
