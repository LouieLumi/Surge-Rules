# Surge-Rules

按服务分类、按顺序匹配的 Surge 规则集。`main` 分支是正式订阅入口；后续可直接在 GitHub 修改对应 `.list` 文件。

## 使用

打开 [Surge-Rules.conf：Raw 规则片段](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Surge-Rules.conf)，将其中规则复制到现有配置的 `[Rule]` 段。**这只是 `[Rule]` 片段，不是完整配置，不能用它替换整个 profile**；节点、策略组、DNS 等继续使用现有配置，已有 `[Rule]` 标题时不要重复添加。

片段保留 `ApplicationDirect`、`ApplicationReject`、五条异地组网规则，以及末尾的 `GEOIP,CN,DIRECT`、`IP-ASN,13335,"👾 人工智能"` 和 `FINAL,✨ 星链网络,dns-failed`。所有策略组名称都必须在你的配置中原样存在，包括 emoji 和空格。

19 个分类订阅都设为 `update-interval=3600`。提交到 GitHub 后，Surge 会在后续规则集更新时读取；需要立即生效可手动刷新远程规则集。`ApplicationDirect`、`ApplicationReject` 沿用原订阅行，未额外指定刷新间隔。

## 分类与顺序

以下顺序与推荐片段一致。Apple Intelligence 在苹果服务前；YouTube、游戏平台、AI 等专用分类在 Google、Microsoft 大类前，防止被大范围规则提前匹配。

| 顺序 | 分类 | 文件与订阅 | 现有策略 |
| --- | --- | --- | --- |
| 1 | Apple Intelligence | [AppleIntelligence.list](https://github.com/LouieLumi/Surge-Rules/blob/main/AppleIntelligence.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/AppleIntelligence.list) | 👾 人工智能 |
| 2 | 苹果服务 | [Apple.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Apple.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Apple.list) | 🍎 苹果服务 |
| 3 | Claude | [Claude.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Claude.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Claude.list) | 👾 人工智能 |
| 4 | OpenAI / ChatGPT / Sora | [OpenAI.list](https://github.com/LouieLumi/Surge-Rules/blob/main/OpenAI.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/OpenAI.list) | 👾 人工智能 |
| 5 | 其他人工智能 | [OtherAI.list](https://github.com/LouieLumi/Surge-Rules/blob/main/OtherAI.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/OtherAI.list) | 👾 人工智能 |
| 6 | 电报信息 | [Telegram.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Telegram.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Telegram.list) | 📲 电报信息 |
| 7 | 游戏平台（Epic / Sony / Steam / Nintendo） | [Games.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Games.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Games.list) | 🎮 游戏平台 |
| 8 | YouTube / YouTube Music | [YouTube.list](https://github.com/LouieLumi/Surge-Rules/blob/main/YouTube.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/YouTube.list) | 📹 油管视频 |
| 9 | 奈飞视频 | [Netflix.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Netflix.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Netflix.list) | 🎥 奈飞视频 |
| 10 | 迪士尼 | [Disney.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Disney.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Disney.list) | 🎬 迪士尼+ |
| 11 | 哔哩哔哩（含国际版） | [BiliBili.list](https://github.com/LouieLumi/Surge-Rules/blob/main/BiliBili.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/BiliBili.list) | 📽 哔哩哔哩 |
| 12 | 其他国外媒体 | [GlobalMedia.list](https://github.com/LouieLumi/Surge-Rules/blob/main/GlobalMedia.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/GlobalMedia.list) | 🍿 国外媒体 |
| 13 | 其他国内媒体 | [ChinaMedia.list](https://github.com/LouieLumi/Surge-Rules/blob/main/ChinaMedia.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/ChinaMedia.list) | 🍔 国内媒体 |
| 14 | Gemini / Google | [Gemini.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Gemini.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Gemini.list) | 🧿 谷歌服务 |
| 15 | 微软服务 | [Microsoft.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Microsoft.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Microsoft.list) | Ⓜ️ 微软服务 |
| 16 | 通用代理兜底 | [Proxy.list](https://github.com/LouieLumi/Surge-Rules/blob/main/Proxy.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/Proxy.list) | 👾 人工智能 |
| 17 | 局域网兜底 | [LAN.list](https://github.com/LouieLumi/Surge-Rules/blob/main/LAN.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/LAN.list) | DIRECT |
| 18 | 中国 ASN 直连兜底 | [ChinaASN.list](https://github.com/LouieLumi/Surge-Rules/blob/main/ChinaASN.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/ChinaASN.list) | DIRECT |
| 19 | 国内域名 / 应用补全 | [ChinaDomain.list](https://github.com/LouieLumi/Surge-Rules/blob/main/ChinaDomain.list) · [Raw 订阅](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/ChinaDomain.list) | DIRECT |

`Proxy.list` 是通用代理兜底，沿用原配置的 `👾 人工智能` 策略，并不表示其中所有服务都是 AI。

## 以后怎么改

1. 打开表中的 `.list` 文件，在 GitHub 编辑并提交到 `main`。文件只写规则条件，不写策略名，例如 `DOMAIN-SUFFIX,example.com`。
2. 分类文件直接就是订阅内容，修改后**无需重新生成**。修改策略映射或顺序时，还需要调整自己 Surge 配置的 `[Rule]` 段；仓库 `.conf` 是供复制的参考片段。
3. 本地修改后运行校验：

```sh
python3 scripts/check_rules.py
python3 -m unittest discover -s tests -v
```

每次向 GitHub 提交时，Actions 也会运行同样的校验，检查语法、重复规则、配置顺序和典型域名归属；它只检查，不会重写你的规则。请留意提交旁的检查结果。

这些文件是按分类与优先级整理后的规则集，不是各上游的完整独立副本。请按推荐组合订阅；单独摘取某一分类可能缺少已移往前置分类的规则。

详见 [设计说明](docs/DESIGN.md)、[来源清单](docs/SOURCES.md)、[导入报告](docs/import-report.json) 和 [第三方声明](THIRD_PARTY_NOTICES.md)。
