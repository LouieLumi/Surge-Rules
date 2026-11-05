# DNS 域名集合

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
