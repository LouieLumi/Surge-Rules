# OtherAI 覆盖与来源

2026-09-17 根据 Mistral 落入通用代理的反馈，补充常用 AI 官网、API、认证与专属资源域名。规则文件为 `rules/OtherAI.list`，继续使用 `👾 人工智能` 策略；要走英国独享，需要在 Surge 中将这个策略组选到对应节点。

本次核对 54 组服务，OtherAI 从 17 条扩展到 105 条，并从后置分类移走 11 条已被它覆盖的规则。逐条来源、迁移及原提交见 [审计快照](other-ai-audit.json)。

同日后续调整新增 19 条 Cloudflare 服务域名条件和 4 条标准 DNS 精确 IP 条件，当前共 128 条。IP 条件包含检测页直接使用的 `1.1.1.1`；Cloudflare 全网的 ASN 13335 兜底已删除，Poe 继续归 OtherAI。该调整及官方来源见 [Cloudflare 分流说明](CLOUDFLARE.md)，上面的 AI 审计文件保留为首次扩展时的历史快照。

## 匹配范围

- 通常使用 `DOMAIN-SUFFIX`，同时覆盖官网根域、API 以及未来新增的子域。共享云上的明确服务地址使用 `DOMAIN` 精确匹配。
- OpenRouter 从仅匹配根域改为后缀匹配；JetBrains AI 从仅匹配 `api.jetbrains.ai` 改为同时覆盖其 AWS/GCP API 子域。
- Cursor 包含其官方网络清单中的 API、Tab、代码索引、登录、CDN、marketplace、云端电脑域名及专用 S3 下载主机。
- DeepSeek、Kimi、Qwen、智谱、MiniMax、豆包、扣子等国内 AI 也进入 OtherAI，优先于 ChinaDomain / ChinaASN 的国内直连兜底。
- Claude、OpenAI、Gemini/Google 继续使用独立规则文件并统一映射到人工智能策略。Apple Intelligence 仍合并在 Apple，但两个 Cloudflare 中继域名改由 OtherAI 的 `cloudflare.com` 后缀覆盖。
- Copilot 仅添加 AI 专用域名/主机；普通 GitHub、Microsoft、Google、AWS、支付及共享登录服务继续按现有分类匹配。
- 平台主域规则可能同时覆盖官网、账单、文档和模型下载；不会自动识别该域名内某个 URL 是否属于 AI。

## 已核对服务

下表为官方网络文档、API 文档、官网或已核对的官方跳转。官网核对只证明服务域名归属，不代表它公开了全部依赖。带 `=` 的地址使用精确主机匹配，其余为域名后缀匹配。

| 服务 | 域名 / 精确主机 | 来源 |
| --- | --- | --- |
| Cursor | `cursor.com`、`cursor.sh`、`cursorapi.com`、`cursor-cdn.com`、`cursorvm.com`、`=anysphere-binaries.s3.us-east-1.amazonaws.com` | [来源 1](https://cursor.com/docs/enterprise/network-configuration) |
| Windsurf / Codeium / Devin | `windsurf.com`、`codeium.com`、`codeiumdata.com`、`devin.ai`、`devinenterprise.com` | [来源 1](https://docs.devin.ai/desktop/troubleshooting/windsurf-common-issues) |
| Augment Code | `augmentcode.com` | [来源 1](https://docs.augmentcode.com/setup-augment/network-configuration) |
| JetBrains AI / Junie | `api.jetbrains.ai`、`=api.app.prod.grazie.aws.intellij.net` | [来源 1](https://www.jetbrains.com/config/JetBrainsAIPlatform.json) |
| GitHub Copilot | `githubcopilot.com`、`=copilot-proxy.githubusercontent.com`、`=copilot-telemetry.githubusercontent.com`、`=origin-tracker.githubusercontent.com`、`=copilot-reports.github.com` | [来源 1](https://docs.github.com/en/copilot/reference/copilot-allowlist-reference) |
| Microsoft Copilot | `=copilot.microsoft.com` | [来源 1](https://copilot.microsoft.com/) |
| Tabnine | `tabnine.com` | [来源 1](https://www.tabnine.com/) · [来源 2](https://docs.tabnine.com/main/welcome/readme/system-requirements.md) |
| TRAE | `trae.ai`、`trae.com.cn`、`trae.cn` | [来源 1](https://www.trae.ai/) · [来源 2](https://www.trae.com.cn/) |
| Cline | `cline.bot` | [来源 1](https://cline.bot/) |
| Roo Code / Roomote | `roocode.com`、`roomote.dev` | [来源 1](https://roocode.com/) |
| Continue | `continue.dev` | [来源 1](https://continue.dev/) |
| Replit | `replit.com` | [来源 1](https://replit.com/) |
| Lovable | `lovable.dev` | [来源 1](https://lovable.dev/) |
| Bolt | `bolt.new` | [来源 1](https://bolt.new/) |
| v0 | `v0.dev`、`v0.app` | [来源 1](https://v0.dev/) · [来源 2](https://v0.app/) |
| Mistral / Le Chat | `mistral.ai` | [来源 1](https://mistral.ai/) · [来源 2](https://docs.mistral.ai/api/endpoint/models) |
| Perplexity | `perplexity.ai`、`pplx.ai` | [来源 1](https://docs.perplexity.ai/) · [来源 2](https://www.perplexity.ai/contact-sales) |
| You.com | `you.com` | [来源 1](https://you.com/) |
| Pi | `pi.ai` | [来源 1](https://pi.ai/) |
| Character.AI | `character.ai` | [来源 1](https://character.ai/) |
| DeepSeek | `deepseek.com` | [来源 1](https://www.deepseek.com/) |
| Kimi / Moonshot | `kimi.com`、`kimi.ai`、`moonshot.ai`、`moonshot.cn` | [来源 1](https://www.kimi.com/) · [来源 2](https://platform.moonshot.ai/docs/guide/start-using-kimi-api) · [来源 3](https://platform.moonshot.cn/) |
| Qwen / 千问 | `qwen.ai`、`qwenlm.ai`、`qianwen.com` | [来源 1](https://qwen.ai/) · [来源 2](https://chat.qwenlm.ai/) · [来源 3](https://www.qianwen.com/) |
| Z.ai / 智谱 | `z.ai`、`bigmodel.cn`、`chatglm.cn` | [来源 1](https://z.ai/) · [来源 2](https://docs.bigmodel.cn/) · [来源 3](https://www.chatglm.cn/) |
| MiniMax | `minimax.io`、`minimaxi.com`、`minimax.cn` | [来源 1](https://www.minimax.io/) · [来源 2](https://platform.minimaxi.com/) |
| 豆包 | `doubao.com` | [来源 1](https://www.doubao.com/) |
| Coze / 扣子 | `coze.com`、`coze.cn` | [来源 1](https://www.coze.com/) · [来源 2](https://www.coze.cn/) |
| Genspark | `genspark.ai` | [来源 1](https://www.genspark.ai/) |
| Manus | `manus.im` | [来源 1](https://manus.im/) |
| Gamma | `gamma.app` | [来源 1](https://gamma.app/) |
| OpenRouter | `openrouter.ai` | [来源 1](https://openrouter.ai/docs/quickstart) |
| Hugging Face | `huggingface.co`、`hf.co`、`hf.space`、`endpoints.huggingface.cloud` | [来源 1](https://huggingface.co/) · [来源 2](https://hf.co/) · [来源 3](https://huggingface.co/docs/hub/spaces-overview) · [来源 4](https://huggingface.co/docs/inference-endpoints/guides/test_endpoint) |
| Replicate | `replicate.com`、`replicate.delivery` | [来源 1](https://replicate.com/) · [来源 2](https://replicate.com/docs/topics/predictions/output-files) |
| Together AI | `together.ai`、`together.xyz` | [来源 1](https://docs.together.ai/docs/quickstart) · [来源 2](https://docs.together.ai/reference/deployments-storage-volumes-get) |
| Cohere | `cohere.com`、`cohere.ai` | [来源 1](https://cohere.com/) · [来源 2](https://docs.cohere.com/docs/compatibility-api) |
| Cerebras | `cerebras.ai` | [来源 1](https://www.cerebras.ai/) |
| Fireworks AI | `fireworks.ai` | [来源 1](https://fireworks.ai/) |
| fal | `fal.ai`、`fal.run` | [来源 1](https://fal.ai/) · [来源 2](https://fal.ai/docs/documentation/model-apis/inference/queue) |
| Ollama | `ollama.com` | [来源 1](https://ollama.com/) |
| LM Studio | `lmstudio.ai` | [来源 1](https://lmstudio.ai/) |
| Midjourney | `midjourney.com` | [来源 1](https://www.midjourney.com/) |
| PixPix | `pixpix.com` | [来源 1](https://www.pixpix.com/) |
| Runway | `runwayml.com`、`runway.com` | [来源 1](https://runwayml.com/) |
| Pika | `pika.art` | [来源 1](https://pika.art/) |
| Ideogram | `ideogram.ai` | [来源 1](https://ideogram.ai/) |
| Leonardo | `leonardo.ai` | [来源 1](https://leonardo.ai/) |
| Recraft | `recraft.ai` | [来源 1](https://www.recraft.ai/) |
| Kling / 可灵 | `klingai.com` | [来源 1](https://app.klingai.com/global/) |
| Hailuo / 海螺 | `hailuoai.com`、`hailuoai.video` | [来源 1](https://hailuoai.com/) · [来源 2](https://www.minimax.io/news/minimax-h3-open-source) |
| Suno | `suno.com`、`suno.ai` | [来源 1](https://suno.com/) |
| Udio | `udio.com` | [来源 1](https://www.udio.com/) |
| ElevenLabs | `elevenlabs.io` | [来源 1](https://elevenlabs.io/) |
| Fish Audio | `fish.audio` | [来源 1](https://fish.audio/) |
| HeyGen | `heygen.com` | [来源 1](https://www.heygen.com/) |

## 验证与后续维护

修改后运行 `python3 scripts/check_rules.py` 和 `python3 -m unittest discover -s tests -v`。规则集是直接维护的最终文件，来源审计是本次快照，不会自动覆盖今后的 GitHub 修改。

本次验证包含 Mistral 官网/API、Cursor 多种后端、截图中的服务、国内 AI 对直连兜底的优先级，以及共享主域没有被误归类。它是静态规则验证，不是每个应用的登录/语音/下载实测，也不证明每条连接的实际出口 IP。

服务会增加新域名；第三方 OAuth、支付、遥测、通用 STUN/TURN、直接 IP 连接或客户端自定义 API 仍可能按其它规则匹配。代理未接管的流量也无法靠域名规则改变。发现遗漏时，在 Surge 请求记录中取得实际目标主机、命中规则和最终策略，再补具体地址；不要用 `.ai`、`ai` 关键词或整段公共云 IP 粗略兜住全部 AI。
