"""Let the reply model inspect its own provider account balance."""

from __future__ import annotations

import json
from urllib.parse import urlsplit

from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Star

from .balance_api import query_deepseek_balance


class SelfBalance(Star):
    """Reuse the currently selected chat provider and its API key."""

    @filter.llm_tool(name="get_self_balance")
    async def get_self_balance(self, event: AstrMessageEvent) -> str:
        """查询你当前会话所用模型平台账户的真实余额。

        返回当前 API Key 所属账户的总可用余额、赠金余额、充值余额、币种、
        是否可继续调用及 UTC 查询时间。这是模型平台账户余额，所有使用同一
        账户的机器人和程序共享它。当前支持 DeepSeek 官方平台。
        工具会自动读取当前会话所选模型的配置，无需用户提供 API Key。
        只有 ok=true 才查到了真实余额；失败时说明无法查询，不要编造金额，
        也不要把未知余额说成零。金额为查询时的快照，后续调用会改变余额。
        """
        try:
            selected = event.get_extra("selected_provider")
            if isinstance(selected, str) and selected:
                provider = self.context.get_provider_by_id(selected)
            else:
                provider = await self.context.get_using_provider_async(
                    umo=event.unified_msg_origin
                )
            if provider is None:
                return json.dumps({"ok": False, "error": "provider_not_found"})

            base = urlsplit(str(provider.provider_config.get("api_base") or ""))
            if (
                base.scheme != "https"
                or base.hostname != "api.deepseek.com"
                or base.port not in (None, 443)
                or base.username is not None
                or base.password is not None
            ):
                return json.dumps(
                    {
                        "ok": False,
                        "error": "unsupported_platform",
                        "message": "当前仅支持 DeepSeek 官方平台的账户余额查询。",
                    },
                    ensure_ascii=False,
                )

            result = await query_deepseek_balance(
                provider.get_current_key(),
                provider.provider_config.get("proxy") or None,
            )
            result["provider_id"] = provider.meta().id
        except Exception:
            # Provider exceptions may contain credentials or private URLs.
            result = {"ok": False, "error": "provider_configuration_error"}
        return json.dumps(result, ensure_ascii=False)
