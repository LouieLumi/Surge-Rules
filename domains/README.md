# Surge 域名集合

## 国内、国外与国际站

三份文件均为 Surge 原生 DOMAIN-SET，可分别订阅。前导点匹配域名本身及其子域名，裸主机名只做精确匹配。

| 文件 | 收录范围 |
| --- | --- |
| [domestic.txt](domestic.txt) · [Raw](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/domains/domestic.txt) | 国内服务、港澳银行，以及上游按中国大陆 DNS / CDN 收录的剩余域名 |
| [foreign.txt](foreign.txt) · [Raw](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/domains/foreign.txt) | 有地区证据的海外本地服务和地区专用站点 |
| [international.txt](international.txt) · [Raw](https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/domains/international.txt) | 多个市场共用的官网、下载服务和 CDN，例如 Google 下载、Apple 更新和微软 Office CDN |

2026-11-06 的拆分以原 [direct.txt](direct.txt) 的 110,189 条记录和 [ApplicationDirect](../rules/ApplicationDirect) 的 5 条域名规则为底稿。原订阅地址继续可用。后者的 3 条进程规则只对应用生效，保留在原文件中。

国内集合开头单列港澳银行官网及公开网银。按名册核对香港 147 家持牌银行、17 家有限制牌照银行，以及澳门 32 家银行和分行。地区专用域通常连同子域名收录，银行用全球共用主机提供当地服务时只收录该主机。以 URL 路径区分地区的网站，同一主机上的其他地区页面也会命中。部分批发银行只公布集团网站，登记网址也可能暂时无法解析。[香港金管局银行联系表](https://www.hkma.gov.hk/media/eng/doc/key-functions/banking-stability/banking-policy-and-supervision/addr.xls) · [澳门金融管理局机构名册](https://www.amcm.gov.mo/zh-hant/bank/bank-institutions-list?type=company-parent-bank-leaf-1)

旧集合的上游根据大陆 DNS 或 CDN 的可用性收录域名。可识别的跨国服务和海外地区站按服务范围分出，其余保留在国内集合。这部分表示沿用原直连名单，运营方所在地未经逐一核验。原自定义域名 `anxx.net` 也在这一组。[上游收录口径](https://github.com/felixonmars/dnsmasq-china-list/blob/a8942d3ac6ebd8dcfc582d4e97fbb443a2176cb2/README.md) · [社区域名分类](https://github.com/v2fly/domain-list-community/tree/4af75ecfbd62c077f9f3ae68b0ae21b89fda1c60/data) · [原始集合的许可和归属](../THIRD_PARTY_NOTICES.md)

三份文件使用不同策略时，较具体的国际站条目应排在国内集合前面。例如国际站收录了 `time.amazonaws.cn`，国内集合中原有的 `.cn` 也能匹配它。Surge 采用最先匹配的规则。

## 原直连 DNS 名单

`direct.txt` 是从 [Loyalsoldier/surge-rules](https://github.com/Loyalsoldier/surge-rules) 导入的国内及部分在国内可直连服务的域名名单，保留上游 DOMAIN-SET 格式和全部内容。它不是只包含中国域名的地域数据库，也不会根据策略组的当前选择切换 DNS。

## 在 Surge 中使用

在现有配置的 `[Host]` 段加入：

```ini
DOMAIN-SET:https://raw.githubusercontent.com/LouieLumi/Surge-Rules/main/domains/direct.txt = server:https://223.5.5.5/dns-query
```

这条引用仅为命中的域名指定阿里 DoH。实际直连或代理仍由 `[Rule]` 和策略组决定；不需要把此集合加入 `[Rule]`。

域名前的 `.` 表示匹配该域名及其子域名；没有前导点的条目仅匹配该主机名。不要把 `DOMAIN-SUFFIX,` 或策略名称写入这个文件。

## 来源与维护

- 导入日期：2026-11-05。
- 上游文件：[release/direct.txt](https://github.com/Loyalsoldier/surge-rules/blob/release/direct.txt)。
- 导入数量：110,189 条。
- 上游 Git blob：`ae1fe01c16367218652de73b0c74f19ae2a47113`。
- 导入内容 SHA-256：`1594e76559de7d020f7f3714bd03633358ee06a86781f7851c3fd96a940f7d25`。
- 上游许可：GNU GPL version 3，随附全文见 [GPL-3.0.txt](../LICENSES/GPL-3.0.txt)，来源与贡献者归属见 [第三方声明](../THIRD_PARTY_NOTICES.md)。

此文件现在由本仓库独立维护，不定时覆盖为上游版本。可直接修改并提交到 `main`，Surge 刷新远程域名集合后读取本仓库的内容。需要同步上游时，应先检查差异，保留本仓库的手工修改并更新来源记录。
