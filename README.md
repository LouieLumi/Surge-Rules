# Surge-Rules

按服务分类、按顺序匹配的 Surge 规则集。`main` 分支是正式订阅入口；所有规则文件统一放在 `rules/`，后续可直接在 GitHub 修改对应文件。

## 使用

打开 [Surge-Rules.conf：Raw 规则片段](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Surge-Rules.conf)，将其中规则复制到现有配置的 `[Rule]` 段。**这只是 `[Rule]` 片段，不是完整配置，不能用它替换整个 profile**；节点、策略组、DNS 等继续使用现有配置，已有 `[Rule]` 标题时不要重复添加。

片段保留 `ApplicationDirect`、`ApplicationReject`、五条异地组网规则，以及末尾的 `GEOIP,CN,DIRECT`、`IP-ASN,13335,"👾 人工智能"` 和 `FINAL,✨ 星链网络,dns-failed`。所有策略组名称都必须在你的配置中原样存在，包括 emoji 和空格。

18 个分类订阅都设为 `update-interval=3600`。提交到 GitHub 后，Surge 会在后续规则集更新时读取；需要立即生效可手动刷新远程规则集。`ApplicationDirect`、`ApplicationReject` 的规则内容和策略未变，仅更新到 `rules/` 路径，未额外指定刷新间隔。

规则集地址已从根目录迁移到 `/main/rules/`，请使用上面的新片段一次性更新订阅地址；旧地址不再维护。

## 分类与顺序

以下顺序与推荐片段一致。Apple Intelligence 已合并进 `rules/Apple.list`，统一走 `🍎 苹果服务`；YouTube、游戏平台、AI 等专用分类在 Google、Microsoft 大类前，防止被大范围规则提前匹配。

| 顺序 | 分类 | 文件与订阅 | 现有策略 |
| --- | --- | --- | --- |
| 1 | 苹果服务（含 Apple Intelligence） | [Apple.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Apple.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Apple.list) | 🍎 苹果服务 |
| 2 | Claude | [Claude.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Claude.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Claude.list) | 👾 人工智能 |
| 3 | OpenAI / ChatGPT / Sora | [OpenAI.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/OpenAI.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/OpenAI.list) | 👾 人工智能 |
| 4 | 其他人工智能 | [OtherAI.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/OtherAI.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/OtherAI.list) | 👾 人工智能 |
| 5 | 电报信息 | [Telegram.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Telegram.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Telegram.list) | 📲 电报信息 |
| 6 | 游戏平台（Epic / Sony / Steam / Nintendo） | [Games.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Games.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Games.list) | 🎮 游戏平台 |
| 7 | YouTube / YouTube Music | [YouTube.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/YouTube.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/YouTube.list) | 📹 油管视频 |
| 8 | 奈飞视频 | [Netflix.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Netflix.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Netflix.list) | 🎥 奈飞视频 |
| 9 | 迪士尼 | [Disney.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Disney.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Disney.list) | 🎬 迪士尼+ |
| 10 | 哔哩哔哩（含国际版） | [BiliBili.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/BiliBili.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/BiliBili.list) | 📽 哔哩哔哩 |
| 11 | 其他国外媒体 | [GlobalMedia.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/GlobalMedia.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/GlobalMedia.list) | 🍿 国外媒体 |
| 12 | 其他国内媒体 | [ChinaMedia.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/ChinaMedia.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/ChinaMedia.list) | 🍔 国内媒体 |
| 13 | Gemini / Google | [Gemini.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Gemini.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Gemini.list) | 🧿 谷歌服务 |
| 14 | 微软服务 | [Microsoft.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Microsoft.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Microsoft.list) | Ⓜ️ 微软服务 |
| 15 | 通用代理兜底 | [Proxy.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/Proxy.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/Proxy.list) | 👾 人工智能 |
| 16 | 局域网兜底 | [LAN.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/LAN.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/LAN.list) | DIRECT |
| 17 | 中国 ASN 直连兜底 | [ChinaASN.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/ChinaASN.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/ChinaASN.list) | DIRECT |
| 18 | 国内域名 / 应用补全 | [ChinaDomain.list](https://github.com/LouieLumi/Surge-Rules/blob/main/rules/ChinaDomain.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/rules/ChinaDomain.list) | DIRECT |

`Proxy.list` 是通用代理兜底，沿用原配置的 `👾 人工智能` 策略，并不表示其中所有服务都是 AI。

## 目录与直连兜底

`rules/` 只存放规则集：18 个分类文件、`ApplicationDirect`、`ApplicationReject`，以及保留的 `NetInfrastructure.list`。后者未加入推荐订阅，内容保持不变。配置片段 `Surge-Rules.conf`、README、`rulesets.json`、`docs/`、`scripts/`、`tests/` 和 `LICENSES/` 都放在规则目录外。

| 规则 | 作用 | 例子 / 匹配依据 |
| --- | --- | --- |
| `LAN.list` | 局域网和特殊用途地址直连 | 私网 IP、路由器域名、`.local` 等；不会因为它存在就自动建立异地组网 |
| `ChinaDomain.list` | 国内域名和应用特征补全直连 | `.cn`、支付宝/淘宝/百度等关键词、部分 User-Agent 和少量固定 IP |
| `ChinaASN.list` | 根据目标 IP 所属的中国 ASN 直连 | ASN 是运营商或网络组织的编号；该规则可能先解析域名，不等同于判断网站使用中文 |

三者都走 `DIRECT`，分别从本地网络、域名/应用、网络归属三个角度补漏；只有前面服务规则未命中时，才按配置顺序进入这些兜底。`GEOIP,CN,DIRECT` 再按 IP 地理数据库补全；`ASN 13335` 与 Final 保留原有顺序。

## 以后怎么改

1. 打开 `rules/` 中对应的规则文件，在 GitHub 编辑并提交到 `main`。文件只写规则条件，不写策略名，例如 `DOMAIN-SUFFIX,example.com`。
2. 分类文件直接就是订阅内容，修改后**无需重新生成**。修改策略映射或顺序时，还需要调整自己 Surge 配置的 `[Rule]` 段；仓库 `.conf` 是供复制的参考片段。
3. 本地修改后运行校验：

```sh
python3 scripts/check_rules.py
python3 -m unittest discover -s tests -v
```

每次向 GitHub 提交时，Actions 也会运行同样的校验，检查语法、重复规则、配置顺序和典型域名归属；它只检查，不会重写你的规则。请留意提交旁的检查结果。

这些文件是按分类与优先级整理后的规则集，不是各上游的完整独立副本。请按推荐组合订阅；单独摘取某一分类可能缺少已移往前置分类的规则。

详见 [设计说明](docs/DESIGN.md)、[来源清单](docs/SOURCES.md)、[导入报告](docs/import-report.json) 和 [第三方声明](THIRD_PARTY_NOTICES.md)。
