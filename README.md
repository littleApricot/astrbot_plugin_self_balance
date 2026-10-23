# 自查余额

给 AstrBot 增加 `get_self_balance` 工具，让机器人查询当前会话所用 DeepSeek 账户的余额。

## 安装和使用

在 AstrBot 插件管理中刷新已添加的 littleApricot 插件源，搜索“自查余额”安装。它与回复判断、群聊表情图库、自维护提示词共用原来的源地址：

```text
https://raw.githubusercontent.com/littleApricot/astrbot_plugin_reply_gate/main/plugins.json
```

也可以通过[仓库地址](https://github.com/littleApricot/astrbot_plugin_self_balance)安装，或从[发布页](https://github.com/littleApricot/astrbot_plugin_self_balance/releases)下载 ZIP 上传。后续在插件管理中检查更新、一键更新即可。

启用后，插件会复用当前模型配置里的 API Key 和代理设置，无需单独配置。

向机器人说“查一下你还有多少余额”即可。当前回复模型需要支持工具调用，并允许使用 `get_self_balance`。

当前支持 DeepSeek 官方平台，模型配置的 API 地址应为 `https://api.deepseek.com` 或 `https://api.deepseek.com/v1`。其他平台会返回 `unsupported_platform`。

## 工具返回

`get_self_balance` 无业务参数，查询对象由当前会话选择的模型决定。如果配置了多个 Key，查询当前正在使用的 Key 所属账户。

| 字段 | 含义 |
| --- | --- |
| `ok` | 是否成功查询；失败时返回 `error`，不返回余额 |
| `platform` | 模型平台，目前为 `DeepSeek` |
| `provider_id` | 可选的模型配置标识 |
| `checked_at` | 查询时间，带时区的 UTC 时间 |
| `is_available` | 官方返回的账户是否有余额可供 API 调用 |
| `balance_infos` | 各币种的余额列表，分别展示，不跨币种相加 |
| `currency` | `balance_infos` 每项中的币种：`CNY` 或 `USD` |
| `total_balance` | 每项中的总可用余额，包含充值余额和赠金 |
| `granted_balance` | 每项中的未过期赠金余额 |
| `topped_up_balance` | 每项中的充值余额 |

金额保留官方返回的十进制字符串。查询失败表示余额未知，不能解释为余额为零。

余额属于模型平台账户；共用账户的机器人和其他程序会共同消耗它。工具返回的是查询时的快照，后续模型调用可能使余额变化。

## 查询方式

插件只向 DeepSeek 官方的 `GET https://api.deepseek.com/user/balance` 发送余额查询，API Key 不会作为工具参数或结果交给模型，也不会写入插件文件。查询过程不调用聊天模型。

已使用机器人现有 Key 验证官方真实余额查询、插件查询函数和 AstrBot 原生工具注册。安装包尚未安装到正在运行的 AstrBot，群聊中的自动工具调用需安装后验证。

[DeepSeek 官方余额接口说明](https://api-docs.deepseek.com/zh-cn/api/get-user-balance/)
