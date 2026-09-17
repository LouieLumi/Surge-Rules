# 第三方来源与许可

本仓库的分类规则根据各文件标注的来源分别整理。此文档和 `LICENSES/` 中的文本仅记录对应上游的许可，**不对本仓库所有文件作统一授权，也不对 LouieLumi 原有文件重新授权**。原作者及贡献者的权利和原有声明继续保留。

本次整理日期：2026-09-17。修改包括分类、去重、格式规范化及按优先级排除已被前置分类覆盖的规则；具体变更以 Git 历史、各规则文件头及来源清单为准。整理后的文件是本仓库维护的版本，不代表上游原作者审核或认可了这些修改。

## 许可对应关系

| 上游 | 本仓库对应内容 | 上游许可及随附全文 |
| --- | --- | --- |
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | 来源注明为该仓库的 Apple、Microsoft、Google、游戏、媒体及 Proxy/Lan/ChinaASN 等衍生规则；以各文件实际来源为准 | 上游根 LICENSE 为 GNU GPL version 2；对应衍生内容保留该许可，见 [GPL-2.0.txt](LICENSES/GPL-2.0.txt) |
| [SukkaW/Surge](https://github.com/SukkaW/Surge) / [Sukka Ruleset](https://ruleset.skk.moe) | 独立文件 `AppleIntelligence.list` | 上游文件头与根 LICENSE 为 GNU AGPL version 3；见 [AGPL-3.0.txt](LICENSES/AGPL-3.0.txt) |
| [VirgilClyne/GetSomeFries](https://github.com/VirgilClyne/GetSomeFries) | 独立文件 `Telegram.list`，源自 `ruleset/ASN.Telegram.list` | 上游根 LICENSE 为 GNU GPL version 3；见 [GPL-3.0.txt](LICENSES/GPL-3.0.txt) |
| [Blankwonder/surge-list](https://github.com/Blankwonder/surge-list) | `ChinaDomain.list` 中由 `cn.list` 整理的域名、USER-AGENT 和 IP 规则 | 核验时上游仓库及 `cn.list` 未声明许可证。本仓库仅记录来源，不为这部分内容添加或推定 GPL、AGPL 等授权 |

`AppleIntelligence.list`、`Telegram.list` 与 blackmatrix7 的衍生规则分别存放，并分别标注来源许可。各许可全文中的无担保条款仍然适用于其对应内容。

## 上游声明与进一步来源

- blackmatrix7 的 [README](https://github.com/blackmatrix7/ios_rule_script/blob/master/README.md) 包含项目特别声明，并说明其规则汇总自其他公开项目。各分类目录中的 README 进一步列出数据来源，应结合对应文件的来源记录查阅，例如 [Apple](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Surge/Apple/README.md)、[Google](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Surge/Google/README.md) 和 [ChinaASN](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Surge/ChinaASN/README.md)。本仓库不将这些汇总内容声明为 blackmatrix7 或 LouieLumi 原创。
- Sukka 的 [README](https://github.com/SukkaW/Surge/blob/master/README.md) 说明许可范围；[Apple Intelligence 原文件](https://ruleset.skk.moe/List/non_ip/apple_intelligence.conf) 的作者、主页与 AGPL 声明是本仓库该分类的直接来源。
- Telegram 来源的 [原文件](https://github.com/VirgilClyne/GetSomeFries/blob/main/ruleset/ASN.Telegram.list) 标明作者 VirgilClyne，并链接至其 [ASN 使用说明](https://github.com/VirgilClyne/GetSomeFries/wiki/%F0%9F%8C%90-ASN)。
- China 补全来源为 Blankwonder 的 [cn.list](https://github.com/Blankwonder/surge-list/blob/master/cn.list)。其缺少明确许可声明的状态已在上表单独记录。

原有 `ApplicationDirect`、`ApplicationReject` 及其他本仓库既有文件的权属或许可状态，不因本文档新增而改变。规则若同时保留其他来源的内容，其原有来源声明仍然适用。

## 许可证原文来源

以下文件于上述整理日期直接下载，未修改其正文：

- `LICENSES/GPL-2.0.txt`：[blackmatrix7 根 LICENSE](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/LICENSE)
- `LICENSES/GPL-3.0.txt`：[GetSomeFries 根 LICENSE](https://raw.githubusercontent.com/VirgilClyne/GetSomeFries/main/LICENSE)
- `LICENSES/AGPL-3.0.txt`：[SukkaW/Surge 根 LICENSE](https://raw.githubusercontent.com/SukkaW/Surge/master/LICENSE)
