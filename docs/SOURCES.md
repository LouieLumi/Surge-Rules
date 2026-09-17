# 来源快照与整理统计

这些文件在 2026-09-17 抓取后已整理为本仓库独立维护的规则；不会定时重新抓取上游覆盖你的手工修改。

下载时间、原始头部、完整 SHA-256：见 [sources.json](sources.json)。逐条迁移及删除依据：见 [import-report.json](import-report.json)。许可见 [第三方说明](../THIRD_PARTY_NOTICES.md)。

## 原始来源

| 来源 | 抓取规则数 | 原始 URL |
| --- | ---: | --- |
| ApplicationDirect | 2 | [原始规则](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/1c578ec604fbb7304d3c3a011eb3420dec52157b/ApplicationDirect) |
| ApplicationReject | 7 | [原始规则](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/1c578ec604fbb7304d3c3a011eb3420dec52157b/ApplicationReject) |
| Apple | 1616 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Apple/Apple_All_No_Resolve.list) |
| AppleIntelligence | 6 | [原始规则](https://ruleset.skk.moe/List/non_ip/apple_intelligence.conf) |
| Claude | 10 | [原始规则](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/1c578ec604fbb7304d3c3a011eb3420dec52157b/Claude.list) |
| OpenAI | 39 | [原始规则](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/1c578ec604fbb7304d3c3a011eb3420dec52157b/OpenAI.list) |
| Gemini | 28 | [原始规则](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/1c578ec604fbb7304d3c3a011eb3420dec52157b/Gemini.list) |
| OtherAI | 17 | [原始规则](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/1c578ec604fbb7304d3c3a011eb3420dec52157b/OtherAI.list) |
| GlobalMedia | 430 | [原始规则](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/1c578ec604fbb7304d3c3a011eb3420dec52157b/GlobalMedia.list) |
| Microsoft | 673 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Microsoft/Microsoft.list) |
| Telegram | 20 | [原始规则](https://raw.githubusercontent.com/VirgilClyne/GetSomeFries/main/ruleset/ASN.Telegram.list) |
| Epic | 15 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Epic/Epic.list) |
| Sony | 116 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Sony/Sony.list) |
| Steam | 54 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Steam/Steam.list) |
| Nintendo | 126 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Nintendo/Nintendo.list) |
| YouTube | 190 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/YouTube/YouTube.list) |
| Netflix | 1158 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Netflix/Netflix.list) |
| Disney | 175 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Disney/Disney.list) |
| BiliBili | 133 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/BiliBili/BiliBili.list) |
| ChinaMedia | 446 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/ChinaMedia/ChinaMedia.list) |
| Proxy | 6924 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Proxy/Proxy_All_No_Resolve.list) |
| LAN | 140 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Lan/Lan.list) |
| ChinaASN | 1009 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/ChinaASN/ChinaASN_Resolve.list) |
| ChinaDomain | 13 | [原始规则](https://raw.githubusercontent.com/Blankwonder/surge-list/master/cn.list) |
| Google | 703 | [原始规则](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Google/Google.list) |

Google 是为“Gemini & Google”补充的同一 blackmatrix7 上游清单；其余均来自你提供的订阅。ApplicationDirect、ApplicationReject 下载用于核对，保持仓库文件不变。NetInfrastructure.list 未被加入订阅、未修改。

当前规则已迁入 `rules/`，Apple Intelligence 已并入 Apple，现为 18 个分类。下面的表和导入报告保留首次整理时的历史统计，文件链接固定到当时提交。

## 首次分类去重统计（历史快照）

迁移先于去重。下表输入是完成归类后、去重前的行数；不会把未使用的本地应用规则算作删除。

| 分类文件 | 去重前 | 保留 | 去除重复/被完整覆盖 |
| --- | ---: | ---: | ---: |
| [AppleIntelligence.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/AppleIntelligence.list) | 6 | 6 | 0 |
| [Apple.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Apple.list) | 1622 | 1616 | 6 |
| [Claude.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Claude.list) | 7 | 3 | 4 |
| [OpenAI.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/OpenAI.list) | 18 | 15 | 3 |
| [OtherAI.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/OtherAI.list) | 17 | 16 | 1 |
| [Telegram.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Telegram.list) | 20 | 20 | 0 |
| [Games.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Games.list) | 311 | 311 | 0 |
| [YouTube.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/YouTube.list) | 213 | 190 | 23 |
| [Netflix.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Netflix.list) | 1184 | 1158 | 26 |
| [Disney.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Disney.list) | 189 | 177 | 12 |
| [BiliBili.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/BiliBili.list) | 144 | 136 | 8 |
| [GlobalMedia.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/GlobalMedia.list) | 355 | 349 | 6 |
| [ChinaMedia.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/ChinaMedia.list) | 441 | 310 | 131 |
| [Gemini.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Gemini.list) | 731 | 698 | 33 |
| [Microsoft.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Microsoft.list) | 673 | 671 | 2 |
| [Proxy.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/Proxy.list) | 6948 | 6675 | 273 |
| [LAN.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/LAN.list) | 140 | 138 | 2 |
| [ChinaASN.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/ChinaASN.list) | 1009 | 1009 | 0 |
| [ChinaDomain.list](https://github.com/LouieLumi/Surge-Rules/blob/deefd8d9433bb7ad4e744345a5b25a18949143b0/ChinaDomain.list) | 13 | 13 | 0 |

**合计：14041 → 13511 条，去除 530 条重复或被完整覆盖的规则。**

该表是此次导入快照，不是实时计数。此后 GitHub 手工维护以各 `.list` 文件实际内容为准。
