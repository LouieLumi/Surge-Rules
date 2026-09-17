# 分类与匹配设计

Surge 按配置从上到下匹配，先命中的规则决定策略。本仓库把可独立选择出口的服务放入专用分类，再保留通用服务、代理和国内直连兜底。分类文件自身只提供匹配条件，使用哪个策略由 `[Rule]` 中的 `RULE-SET` 行决定。

本次基于用户现有规则和下载的上游快照整理。`rulesets.json` 记录 18 个分类、推荐顺序及现有策略；`Surge-Rules.conf` 提供可复制的 `[Rule]` 片段，不包含节点、DNS 或策略组定义。

## 分类迁移

| 内容 | 整理结果 |
| --- | --- |
| `ApplicationDirect`、`ApplicationReject` 与五条异地组网规则 | 规则内容保留，两个应用文件迁入 `rules/`，仍放在全部分类前 |
| Apple Intelligence | 合并到 `rules/Apple.list`；Cloudflare 中继域名随后按统一基础设施策略改由 OtherAI 覆盖，其余走 `🍎 苹果服务` |
| 苹果服务 | `Apple.list` 接收 Apple 上游规则，以及旧 `GlobalMedia.list` 的 Apple TV / Apple Music 章节 |
| Claude、OpenAI、其他 AI | 保留独立分类；`chat.com` 归 `OpenAI.list`，`ai.com` 归 `OtherAI.list` |
| Gemini / Google | 合并 Google 上游与原 Gemini 规则，继续使用 `Gemini.list` 路径，当前与其它 AI 一起使用 `👾 人工智能` 策略 |
| 微软服务 | 独立 `Microsoft.list`，位于专用 AI、游戏和媒体分类之后 |
| Telegram | 独立 `Telegram.list`，保留域名、进程及 Telegram ASN/IP 条件 |
| 游戏平台 | Epic、Sony、Steam、Nintendo 合并为 `Games.list` |
| YouTube、Netflix、Disney | 各自的上游规则与旧 `GlobalMedia.list` 中对应章节合并，使用原有各自策略 |
| Bilibili | 国内、国际版都归 `BiliBili.list`，使用 `📽 哔哩哔哩` |
| 其他国外媒体 | `GlobalMedia.list` 保留移出专用分类后的其他国外媒体 |
| 其他国内媒体 | `ChinaMedia.list` 保留其他国内媒体，并接收 `snssdk.com`；Bilibili 已在专类中处理 |
| Proxy、LAN、China ASN、国内补全 | 分别为 `Proxy.list`、`LAN.list`、`ChinaASN.list`、`ChinaDomain.list` |

`GlobalMedia.list` 排在 `ChinaMedia.list` 前，让 `inter.iqiyi.com`、`intl.iqiyi.com` 等国际爱奇艺具体子域先匹配国外媒体，再由国内媒体的 `iqiyi.com` 父域接住其余请求。这个顺序用于保留国际版例外，不把共享的国内域名一并转为国外媒体：`snssdk.com` 明确保留在 `ChinaMedia.list`。

YouTube 必须先于 Google 大类；游戏平台和专用 AI 必须先于 Microsoft 大类。Apple 与 Apple Intelligence 现在共用一个文件和策略。更具体的域名放前、更宽的服务范围放后，是这些顺序的共同原因。

上游 YouTube 清单同时包含 `gvt1.com`、`gvt2.com` 等 Google 共享 CDN。本次沿用该清单的归属，它们也可能承载地图或其他 Google 下载，不能理解成只匹配视频。Microsoft 清单中的 `edgesuite.net`、`optimizely.com` 等宽泛条目同理；Netflix、Disney 等明确的子域会先按前置专用规则匹配。

## AI 共享服务与 IP 行为

原 Claude / OpenAI 列表中的共享云服务、认证、支付与遥测域名移入 `Proxy.list`，避免把它们全部归为某一家 AI 厂商。仍留在专用 AI 分类中的服务专属域名按各自策略匹配。最初整理时 Proxy 沿用了原有人工智能策略；按后续“普通境外默认星链”的要求，当前 `Proxy.list` 与 FINAL 均使用 `✨ 星链网络`。

`DOMAIN-SUFFIX,cloudflare.com` 已从 Proxy 移到 OtherAI，覆盖 Cloudflare 官网、API、验证、cdnjs、STUN/TURN。随后补充 DNS、Access、Workers、Pages、R2、Tunnel、图片与视频等已核对的服务域名，合计 20 条 Cloudflare 域名条件；这属于用户指定的基础设施出口，并不表示这些服务全是 AI。Apple 中的 `apple-relay.cloudflare.com` 与 `cp4.cloudflare.com` 两条前置例外已删除，由 OtherAI 的父域统一覆盖。其它 AI 专用主机仍优先，例如 OpenAI 自己的 Cloudflare CDN 主机继续命中 OpenAI，出口同样是人工智能策略。

普通站点即使由 Cloudflare CDN 托管，也按请求域名本身分流，不再被 AS13335 捕获。没有增加 Wise、Shopify、npm 等站点的个别例外；调整的是通用默认策略。Twilio 和通用 LiveKit 仍由 Proxy 匹配，明确的 ChatGPT LiveKit 主机则由 OpenAI 匹配。详情和边界见 [Cloudflare 分流说明](CLOUDFLARE.md)。

随后根据 Mistral 落入 Proxy 的反馈，对 54 组常用 AI 服务核对官网和网络/API 文档，OtherAI 从 17 条扩展到 105 条，并将 Proxy 中 11 条 AI 域名移入该类。Cursor 的 API、CDN、云端电脑域名、OpenRouter 和 JetBrains API 的子域覆盖得到补充；国内 AI 也优先于国内直连兜底。明细见 [OtherAI 覆盖与来源](OTHER_AI.md)；本次未调整专用 Claude、OpenAI、Gemini、Apple 分类或任何 IP/ASN 规则。

原 OpenAI 文件里的 `AS20473`、`24.199.123.28/32`、`64.23.132.171/32` 一并移入 `Proxy.list`。其中两个旧 IP 的现时用途未经验证，保留为兼容兜底，不声明它们是 OpenAI 专用地址。对这三条 IP/ASN 条件增加 `no-resolve`，避免匹配兜底时主动为每个未匹配域名触发 DNS；它们仍可匹配已知目标 IP。

除上述三条外，原有 IP 规则选项保持不变。特别是 `ChinaASN.list` 延续 `ChinaASN_Resolve.list` 的解析语义，**可能触发 DNS 查询**，没有为了去重统一增加 `no-resolve`。

当前末尾为：

```ini
GEOIP,CN,DIRECT
FINAL,✨ 星链网络,dns-failed
```

原来位于 GEOIP 后、FINAL 前的 AS13335 规则已按后续要求删除，不再用整个共享 CDN 网络判断人工智能归属。规则校验会拒绝在任何规则文件重新引入 AS13335；配置片段也不再允许这条兜底。

语义依据：[Surge 匹配顺序与 DNS](https://manual.nssurge.com/rules/overview.html)、[规则集格式与刷新参数](https://manual.nssurge.com/rules/ruleset.html)。AS20473 的基础设施归属见 [Vultr 官方说明](https://docs.vultr.com/support/products/network/what-is-vultrs-asn)；`chat.com` 与 `ai.com` 的归属按本次整理时的站点内容/跳转核对。

## 去重边界

去重只处理能明确证明覆盖的情况：完全相同的规则、域名后缀包含关系，以及规则参数相同的 CIDR 包含关系。相同参数是保留 IP 解析语义的前提，例如不会把带 `no-resolve` 与不带该参数的规则当作完全等价。

跨分类排除以后，部分后置列表只包含未被前置分类覆盖的剩余规则。更前的具体子域与更后的父域后缀会有意共存，例如国际爱奇艺与国内媒体。删除后面的父域会漏掉其余子域，删除前面的具体子域则会改变策略归属。

保留现有 Google 相关关键词和 `DOMAIN-KEYWORD,openai` 的宽匹配行为。这类关键词不要求是服务的官方域名，仍可能命中含相同文字的其他域名；本次未将其静默改窄。也不根据 ASN、GEOIP 或关键词推断并删除另一条域名/IP 规则，因为这些条件的覆盖关系并非仅靠静态文本就能可靠确定。

因此，这些分类要按 `Surge-Rules.conf` 的推荐组合和顺序使用，不能把任意一个去重后的列表理解为对应上游的完整独立版本。

## 后续维护

`.list` 就是实际订阅文件，直接修改并提交到 `main` 即可，不需要重新运行导入或生成步骤。`rulesets.json` 与 `Surge-Rules.conf` 用于记录推荐分类和调用方式；调整文件名称、策略映射或顺序时，需要同步维护它们，并更新实际使用中的 Surge 配置。

本地检查命令：

```sh
python3 scripts/check_rules.py
python3 -m unittest discover -s tests -v
```

[来源清单](SOURCES.md) 与 [导入报告](import-report.json) 记录本次上游与整理情况；它们是本次导入的快照，不会因为之后手动修改规则而自动刷新。各上游及用户原有内容的许可分别保留，见 [第三方声明](../THIRD_PARTY_NOTICES.md)。

## 2026-09-17 后续调整

首次目录调整将所有规则集迁入 `rules/`，目录内只放规则文件。订阅基址更新为 `https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/`。`AppleIntelligence.list` 已合并，不再单独订阅。之后又扩充 OtherAI，并完成上文的 Cloudflare 域名迁移和 AS13335 删除。五条异地组网及两个本地应用规则的内容保持不变；历史导入报告继续记录首次整理时的名称与数量。
