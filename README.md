# 自查余额（已合并）

本插件的功能已并入[用量与费用明细](https://github.com/littleApricot/astrbot_plugin_usage_insight)，从 v0.3.0 起统一提供。

## 迁移

先在 AstrBot 插件管理中卸载旧“自查余额”，再从原插件源安装或更新“用量与费用明细”。旧插件没有独立配置和数据库；统计插件已有的记录会保留。卸载旧插件可避免同名工具被重复加载覆盖。

机器人继续使用 `get_self_balance` 工具，复用当前模型的 API Key 查询 DeepSeek 官方账号余额，无需修改原工具名。页面还提供当前 Key 在此 AstrBot 中的用量和费用估算。

账号余额由同账号的所有程序共享；本机 Key 统计只覆盖此 AstrBot 采集的请求。请参阅合并后的[完整使用说明](https://github.com/littleApricot/astrbot_plugin_usage_insight#readme)。
