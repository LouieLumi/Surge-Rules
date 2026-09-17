# Cloudflare 域名分流与普通境外默认出口

2026-09-17 按用户要求，普通境外流量由 Proxy / FINAL 使用星链；AI、Google 和已核对的 Cloudflare 服务域名使用人工智能策略，用户将该策略组选为英国独享。Poe 是 AI 服务，保留在 OtherAI。

## 为什么删除 AS13335

Cloudflare 的代理 IP 由很多客户域名共享。按 AS13335 匹配会把普通工具、商店和下载站也送去英国，无法区分 Cloudflare 自己的服务和使用 Cloudflare 的网站。依据：[Cloudflare 共享 IP 说明](https://developers.cloudflare.com/fundamentals/concepts/cloudflare-ip-addresses/)。

因此删除配置中的 `IP-ASN,13335,...` 整行，也不在任何规则集内加入 Cloudflare 全网 CIDR 作为替代。Cloudflare 服务使用域名规则，另对四个标准 DNS 服务的直接 IP 设置精确主机条件；未命中的请求仍会依次检查其他服务、国内/局域网兜底，最后使用星链。依据：[Surge 匹配顺序](https://manual.nssurge.com/rules/overview.html)。

这不需要给 Wise、Shopify、Product Hunt、npm、unpkg 等网站逐个加例外。它们不会仅因为目标 IP 属于 Cloudflare 就被归入 AI。

## OtherAI 中的 Cloudflare 范围

以下均使用 `DOMAIN-SUFFIX`，同时覆盖根域及子域，共 20 条。将原 Proxy 中 6 条重叠规则移走；Apple 中两条 Cloudflare 中继主机由 `cloudflare.com` 父域覆盖。原 OpenAI 中的专属 CDN 主机继续优先命中 OpenAI，出口仍为人工智能策略。

| 服务 | 域名条件 | 官方依据 |
| --- | --- | --- |
| 官网、API、验证、cdnjs、STUN/TURN | `cloudflare.com` | [产品文档](https://developers.cloudflare.com/) · [TURN 地址](https://developers.cloudflare.com/realtime/turn/) |
| DNS | `cloudflare-dns.com`、`one.one.one.one` | [客户端网络要求](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/deployment/firewall/) · [DoT](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-tls/) |
| 客户端、Gateway、Access、状态 | `cloudflareclient.com`、`cloudflare-gateway.com`、`cloudflareaccess.com`、`cloudflarestatus.com` | [官方全局策略](https://developers.cloudflare.com/cloudflare-one/traffic-policies/global-policies/) |
| Web Analytics | `cloudflareinsights.com` | [采集地址](https://developers.cloudflare.com/web-analytics/data-metrics/data-origin-and-collection/) |
| Workers / Pages | `workers.dev`、`pages.dev` | [域名与迁移说明](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/) |
| R2 API / 公共存储 | `r2.cloudflarestorage.com`、`r2.dev` | [R2 API](https://developers.cloudflare.com/r2/api/) · [公共存储桶](https://developers.cloudflare.com/r2/buckets/public-buckets/) |
| Tunnel | `argotunnel.com`、`cfargotunnel.com`、`trycloudflare.com` | [连接端点](https://developers.cloudflare.com/tunnel/configuration/) · [隧道域名](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/routing-to-tunnel/dns/) · [快速隧道](https://developers.cloudflare.com/tunnel/get-started/) |
| 图片 / 视频 | `imagedelivery.net`、`videodelivery.net`、`cloudflarestream.com` | [Images](https://developers.cloudflare.com/images/optimization/hosted-images/serve-uploaded-images/) · [Stream](https://developers.cloudflare.com/stream/faq/) |
| 直接访问 CDN 服务主机 | `cdn.cloudflare.net` | [CNAME 接入](https://developers.cloudflare.com/dns/zone-setups/partial-setup/) |
| 既有 IPFS 网关兼容规则 | `cloudflare-ipfs.com` | [网关 URL](https://developers.cloudflare.com/web3/how-to/use-ipfs-gateway/) |

`workers.dev`、`pages.dev`、R2、图片和视频服务也承载非 AI 内容；直接访问这些服务域名时，按用户要求统一走英国。客户自己的独立域名则按该域名匹配，不因 CNAME 或 IP 背后使用 Cloudflare 而自动归入本列表。同一个网页的主站可以走星链，加载的 Cloudflare 服务域名资源可以走英国。

这不是 Cloudflare 所有产品和未来域名的永久全集。未列出的直接 IP 连接、客户端自定义的 STUN/TURN 域名或 Surge 未接管的流量，无法仅靠这些条件保证英国出口；发现实际遗漏时应根据目标主机补服务条件。Cloudflare 官方也支持 [自定义 TURN 域名](https://developers.cloudflare.com/realtime/turn/custom-domains/)。

## 直接 IP 的 Cloudflare 出口检测

Net.Coffee 的 [GPT 检测页](https://ip.net.coffee/gpt/)公开脚本 `fetchCfIP()` 访问 `https://1.1.1.1/cdn-cgi/trace`。删除 AS13335 后，这个 IP 字面量没有域名可供 OtherAI 匹配，会落到 FINAL 星链；同时 `cloudflare.com`、Claude 和 WebRTC 仍可正常匹配英国。该检测卡片不能代表所有 Cloudflare 域名的出口。

OtherAI 另加入四个 [Cloudflare 官方标准 DNS 地址](https://developers.cloudflare.com/1.1.1.1/ip-addresses/)：`1.1.1.1/32`、`1.0.0.1/32`、`2606:4700:4700::1111/128`、`2606:4700:4700::1001/128`。每条均带 `no-resolve`，只匹配对应单个已知 IP，不触发普通域名的 DNS 查询，也不覆盖 Cloudflare 客户网站的共享地址段。条件同时适用于到这些地址的 DNS 和 HTTPS 等已被 Surge 接管的连接，不修改设备的 DNS 服务器设置。

## 生效步骤

1. 从本地 Surge 的 `[Rule]` 中删除 `IP-ASN,13335,...` 整行。
2. Proxy 的 RULE-SET 策略设为 `✨ 星链网络`；Claude、OpenAI、OtherAI、Gemini 的策略统一设为 `👾 人工智能`。
3. 保留 `FINAL,✨ 星链网络,dns-failed`，更新 OtherAI、Proxy、Apple 的远程规则集，确认两个策略组选中预期节点。

也可直接使用仓库的 [完整规则片段](../Surge-Rules.conf) 替换现有 `[Rule]` 段；它不包含节点和策略组定义。订阅 `.list` 刷新不会自动改动本地配置中的 ASN 行或策略映射。

本次校验覆盖域名归属、Cloudflare 与普通站点的边界、Google 基础设施策略、Poe 保留为 AI、ASN 规则不得重新出现，以及本地/组网规则保留。静态规则测试和离线语法检查不能证明当前设备每条连接的实际出口。
