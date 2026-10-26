# Claude / OpenAI 分流维护

核对日期：2026-10-26。入口保持为 `rules/Claude.list` 和 `rules/OpenAI.list`，仍使用 `👾 人工智能` 策略。这次补充按用户提供的两份 Net.Coffee 清单核对，再结合服务商文档和当前域名清单收窄匹配范围。

## 本次调整

- Claude 从实际 4 条扩充到 16 条：补齐短域名、MCP 内容/客户端、指定 CDN、旧认证和内容端点；将已知监控接收地址放到 AI 分类；补充官方 API 入站 IPv4/IPv6 范围。
- OpenAI 从 15 条扩充到 37 条：补齐资源、验证、WorkOS 登录依赖、语音和指定遥测端点，覆盖 ChatGPT、Codex 和 Sora。核心后缀已覆盖 API、登录和 WebSocket 子域，不需要重复列出。
- 删除 `DOMAIN-KEYWORD,openai`，用明确域名替代。包含 openai 字样的第三方域名不再自动进入人工智能策略。
- Azure Web PubSub 使用 `chatgpt-async-webps-prod-*-*.webpubsub.azure.com` 命名模式，避免把整个共享服务都划给 OpenAI。Surge 的通配规则比来源正则稍宽，不能据此证明任意匹配主机的归属。
- 从 Proxy 移走 7 条已由专用分类接管的规则：两个 Datadog intake、crixet 后端、chatgpt.site、Arkose client-api、LiveKit host/turn。Proxy 其余流量保持原策略。
- 规则数量头部按实际内容更新；首次导入报告继续保留历史数据。

## 共享服务的边界

`browser-intake-us5-datadoghq.com` 和 `browser-intake-datadoghq.com` 是独立根域，不能被 `datadoghq.com` 的后缀捕获。两者按后缀匹配，以覆盖 `rum.` 等子域；它们以及 LiveKit host/turn、WorkOS、Stripe JS、Fathom 都可能服务其他客户，相关请求也会随这些具体规则使用 AI 出口。

没有新增 sentry / datadog / sift 关键词，也没有把整个 Sentry、Auth0、Stripe、Intercom、Statsig 或 Azure 网络归入 Claude/OpenAI。只把有依据的 Sentry 项目端点、验证/认证主机和支付脚本提前匹配；其余共享服务沿用现有分类。客服、统计等可选组件不承诺与主服务出口相同，遇到实际异常应按 Surge 请求日志补充具体主机。已有 OtherAI 的 `datadoghq.com` 规则保留。

## IP 与 NTP

Claude 官方区分入站和出站地址：本地客户端访问 API 使用官方入站范围 `160.79.104.0/23`、`2607:6bc0::/48`。没有照搬参考文章的更宽 `/21`、`/32` 或整个 ASN；`/21` 在官方文档中用于 Anthropic 向外发起请求，不能混同本地 API 目的地址。

两条 IP 规则都带 `no-resolve`，匹配已知目的 IP，不为未解析的域名主动触发 DNS。它们只是补充，不能代替域名规则，也不保证覆盖每个 CDN 地址。

没有加入全局 NTP 代理。NTP 同步时间，并不返回用户系统时区；“代理 NTP 即可统一时区或保证避免风控”的说法没有据此采用。规则集也不修改系统时区或 IPv6 开关。

## 应用与验证

1. 在 Surge 中刷新两个 AI 规则集及 Proxy；已有订阅 URL、策略组和推荐顺序均无需改名。仓库配置设置的分类刷新周期为 3600 秒。
2. 确认 `👾 人工智能` 选中了期望的节点。规则只能选策略，不能保证组内节点固定，也不能保证账号可用性。
3. 打开 Claude/ChatGPT，查看 API、登录、MCP/文件、语音请求实际命中的规则和出口。位于这些 RULE-SET 之前的应用直连、拒绝、协议规则仍有更高优先级。
4. 语音需要可用的 UDP 或服务支持的 TCP 回退。如果本地已有更前置的 `PROTOCOL,STUN` 规则，STUN 请求仍由该规则决定；仅更新 GitHub 域名表不会覆盖它。本次没有改动本地 profile。
5. 仓库检查验证语法、去重、顺序、代表域名及 IP 边界，不模拟 Surge 实际 DNS、ASN、UDP、进程或在线服务连通性。官方语音 IP 清单持续变化，本次没有把它静态抄入规则。

## 来源

- 用户参考：[Net.Coffee Claude](https://ip.net.coffee/claude/site.html)、[Net.Coffee ChatGPT](https://ip.net.coffee/gpt/site.html)。用于查漏，不采用其所有风控推断。
- [Claude Code 网络要求](https://code.claude.com/docs/en/network-config)：API、认证、MCP、内容、监控端点；[Claude API 地址](https://platform.claude.com/docs/en/api/ip-addresses)：入站/出站范围。
- [OpenAI 网络建议](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)：资源、WorkOS、指定遥测和支付脚本。允许访问清单不等于“全部必须同一出口”，这里的策略归类是本仓库的选择。
- [v2fly OpenAI 数据](https://github.com/v2fly/domain-list-community/blob/master/data/openai)、[Anthropic 数据](https://github.com/v2fly/domain-list-community/blob/master/data/anthropic)：核对域名、LiveKit 和 Web PubSub 模式；社区归类不是服务商所有权声明。
- [blackmatrix7 Claude 数据](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Surge/Claude/Claude.list)：Fathom 端点。迁入的 Proxy 条目及该来源的衍生内容保留原 GPL-2.0 归属，见 [第三方声明](../THIRD_PARTY_NOTICES.md)。
- [Surge 域名匹配](https://manual.nssurge.com/rules/domain.html)、[匹配顺序与 DNS](https://manual.nssurge.com/rules/overview.html)：后缀、通配、先匹配和 no-resolve 语义。
- [NTPv4 RFC 5905](https://www.rfc-editor.org/rfc/rfc5905.html)：协议及时间戳定义。
