"""Static routing regressions for known overlap and category-ownership cases.

These tests do not execute Surge or infer IP, DNS, ASN or process behavior.
"""

from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_rules import LOCAL_FILES, MESH_LINES, TAIL_LINES, check_repository, first_match_domain, load_domain_routes
from rulelib import load_rules


class PublishedRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes = load_domain_routes(ROOT)

    def assert_category(self, hostname, filename, policy):
        self.assertEqual(first_match_domain(hostname, routes=self.routes), (filename, policy), hostname)

    def test_youtube_precedes_broad_google(self):
        for hostname in ("googlevideo.com", "r1.googlevideo.com", "youtubei.googleapis.com", "video.google.com"):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, "YouTube.list", "📹 油管视频")

    def test_gemini_and_general_google(self):
        for hostname in ("generativelanguage.googleapis.com", "notebooklm.google", "notebooklm.google.com",
                         "google.com", "gemini.google.com", "accounts.google.com", "www.gstatic.com",
                         "storage.googleapis.com", "stun.l.google.com", "server.1e100.net"):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, "Gemini.list", "👾 人工智能")

    def test_apple_intelligence_remains_merged_except_cloudflare_services(self):
        for hostname in ("apple-relay.apple.com", "gspe1-ssl.ls.apple.com",
                         "7h15.ru1353t.1s.m4d3.by.5ukk4w.skk.moe",
                         "apple-relay.fastly-edge.com", "www.apple.com"):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, "Apple.list", "🍎 苹果服务")
        self.assertNotIn("AppleIntelligence.list", [name for name, _, _ in self.routes])

    def test_ai_domain_ownership(self):
        for hostname, filename in (("claude.ai", "Claude.list"), ("api.anthropic.com", "Claude.list"),
                                   ("chatgpt.com", "OpenAI.list"), ("chat.com", "OpenAI.list"),
                                   ("ai.com", "OtherAI.list"), ("poe.com", "OtherAI.list"),
                                   ("api.poe.com", "OtherAI.list")):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, filename, "👾 人工智能")

    def test_other_ai_frontends_and_backend_hosts_do_not_fall_through(self):
        # Regressions for the Mistral screenshot and vendor-documented API,
        # auth, nested cloud-computer and asset hosts beyond their homepages.
        for hostname in ("mistral.ai", "chat.mistral.ai", "api.mistral.ai",
                         "pixpix.com", "www.midjourney.com", "marketplace.cursorapi.com",
                         "cursor-cdn.com", "computer.region.cursorvm.com", "agent.api5.cursor.sh",
                         "anysphere-binaries.s3.us-east-1.amazonaws.com",
                         "aws.api.jetbrains.ai", "api.openrouter.ai", "api.githubcopilot.com",
                         "copilot-proxy.githubusercontent.com", "server.codeiumdata.com",
                         "chat.deepseek.com", "api.moonshot.cn", "chat.qwen.ai",
                         "queue.fal.run", "files.replicate.delivery"):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, "OtherAI.list", "👾 人工智能")

    def test_other_ai_does_not_capture_shared_hosts_or_lookalike_domains(self):
        # A service-specific endpoint must not pull the whole shared cloud,
        # source hosting, authentication, or general WebRTC provider into AI.
        for hostname in ("github.com", "api.github.com", "www.microsoft.com",
                         "storage.googleapis.com", "other-bucket.s3.us-east-1.amazonaws.com",
                         "api.stripe.com", "global.turn.twilio.com", "example.turn.livekit.cloud",
                         "notmistral.ai", "api.mistral.ai.example.org"):
            with self.subTest(hostname=hostname):
                match = first_match_domain(hostname, routes=self.routes)
                self.assertTrue(match is None or match[0] != "OtherAI.list", (hostname, match))

    def test_domestic_and_international_media(self):
        for hostname in ("iq.com", "intl.iqiyi.com"):
            self.assert_category(hostname, "GlobalMedia.list", "🍿 国外媒体")
        for hostname in ("www.iqiyi.com", "snssdk.com"):
            self.assert_category(hostname, "ChinaMedia.list", "🍔 国内媒体")
        for hostname in ("bilibili.tv", "www.bilibili.com"):
            self.assert_category(hostname, "BiliBili.list", "📽 哔哩哔哩")

    def test_service_specific_shared_infrastructure(self):
        self.assert_category("cdn.optimizely.com", "Disney.list", "🎬 迪士尼+")
        self.assert_category("netflix.com.edgesuite.net", "Netflix.list", "🎥 奈飞视频")
        self.assert_category("api.stripe.com", "Proxy.list", "✨ 星链网络")

    def test_cloudflare_services_follow_ai_without_routing_all_customers_by_asn(self):
        for hostname in ("cloudflare.com", "api.cloudflare.com", "challenges.cloudflare.com",
                         "cdnjs.cloudflare.com", "stun.cloudflare.com", "turn.cloudflare.com",
                         "apple-relay.cloudflare.com", "cp4.cloudflare.com",
                         "cloudflare-dns.com", "one.one.one.one", "cloudflare-ipfs.com",
                         "www.cloudflarestatus.com", "static.cloudflareinsights.com",
                         "zero-trust-client.cloudflareclient.com", "account.cloudflare-gateway.com",
                         "team.cloudflareaccess.com", "demo.workers.dev", "demo.pages.dev",
                         "account.r2.cloudflarestorage.com", "pub-example.r2.dev",
                         "region1.v2.argotunnel.com", "example.cfargotunnel.com", "demo.trycloudflare.com",
                         "imagedelivery.net", "customer.videodelivery.net", "customer.cloudflarestream.com",
                         "example.com.cdn.cloudflare.net"):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, "OtherAI.list", "👾 人工智能")

    def test_general_overseas_sites_use_proxy_or_continue_to_non_ai_fallbacks(self):
        # No per-site exceptions are needed: known proxy domains use Starlink;
        # unlisted domains continue to IP/domestic checks and FINAL, never a
        # Cloudflare ASN -> AI rule. This helper does not simulate those checks.
        for hostname in ("coinbase.com", "www.okx.com", "binance.com", "zoom.us",
                         "1password.com", "notion.so", "godaddy.com", "gitlab.com", "crunchyroll.com"):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, "Proxy.list", "✨ 星链网络")
        for hostname in ("wise.com", "shopify.com", "producthunt.com", "registry.npmjs.org",
                         "kali.download", "unpkg.com", "nodejs.org", "crypto.com",
                         "a-new-overseas-service.example", "notcloudflare.com", "cloudflare.com.example"):
            with self.subTest(hostname=hostname):
                self.assertIsNone(first_match_domain(hostname, routes=self.routes), hostname)

    def test_hostname_normalization(self):
        self.assert_category("YOUTUBEI.GOOGLEAPIS.COM.", "YouTube.list", "📹 油管视频")

    def test_all_published_files_and_protected_configuration(self):
        errors, counts = check_repository(ROOT)
        self.assertEqual(errors, [], "\n".join(errors))
        manifest = json.loads((ROOT / "rulesets.json").read_text(encoding="utf-8"))
        expected = set(LOCAL_FILES) | {entry["file"] for entry in manifest["rulesets"]}
        expected.update(manifest.get("auxiliary_rulesets", []))
        self.assertEqual(set(counts), expected)

    def test_cloudflare_asn_is_removed_and_default_policy_is_starlink(self):
        manifest = json.loads((ROOT / "rulesets.json").read_text(encoding="utf-8"))
        for entry in manifest["rulesets"]:
            self.assertFalse(any(rule.kind == "IP-ASN" and rule.value == "13335"
                                 for rule in load_rules(ROOT / "rules" / entry["file"])), entry["file"])
        active = [line for line in (ROOT / "Surge-Rules.conf").read_text(encoding="utf-8").splitlines()
                  if line.strip() and not line.lstrip().startswith(("#", ";", "//"))]
        self.assertEqual(tuple(active[-len(TAIL_LINES):]), TAIL_LINES)
        self.assertFalse(any(line.startswith("IP-ASN,13335,") for line in active))
        self.assertEqual(active[-1], "FINAL,✨ 星链网络,dns-failed")


class CheckerFailureTests(unittest.TestCase):
    """Prove malformed output is detected, including reverse-order overlap."""

    def make_fixture(self, root):
        manifest = {"schema_version": 1, "rules_directory": "rules",
                    "base_url": "https://example.com/rules/", "rulesets": [
            {"file": "First.list", "policy": "Proxy"}, {"file": "Second.list", "policy": "DIRECT"}]}
        (root / "rulesets.json").write_text(json.dumps(manifest), encoding="utf-8")
        (root / "rules").mkdir()
        (root / "rules/ApplicationDirect").write_text("PROCESS-NAME,LocalApp\n", encoding="utf-8")
        (root / "rules/ApplicationReject").write_text("PROCESS-NAME,BlockedApp\n", encoding="utf-8")
        (root / "rules/First.list").write_text("DOMAIN-SUFFIX,example.com\n", encoding="utf-8")
        (root / "rules/Second.list").write_text("DOMAIN,unrelated.test\n", encoding="utf-8")
        config = ["[Rule]", "RULE-SET,https://example.com/rules/ApplicationDirect,DIRECT",
                  "RULE-SET,https://example.com/rules/ApplicationReject,REJECT,no-resolve"]
        config += list(MESH_LINES)
        config += ["RULE-SET,https://example.com/rules/First.list,Proxy", "RULE-SET,https://example.com/rules/Second.list,DIRECT"]
        config += list(TAIL_LINES)
        (root / "Surge-Rules.conf").write_text("\n".join(config) + "\n", encoding="utf-8")

    def test_detects_parent_suffix_even_when_it_appears_after_child(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_fixture(root)
            self.assertEqual(check_repository(root)[0], [])
            (root / "rules/First.list").write_text("DOMAIN,api.example.com\nDOMAIN-SUFFIX,example.com\n", encoding="utf-8")
            errors, _ = check_repository(root)
            self.assertTrue(any("First.list: redundant DOMAIN,api.example.com" in error for error in errors))

    def test_detects_cross_category_coverage(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_fixture(root)
            (root / "rules/Second.list").write_text("DOMAIN,api.example.com\n", encoding="utf-8")
            errors, _ = check_repository(root)
            self.assertTrue(any("preceding First.list" in error for error in errors))

    def test_detects_changed_mesh_and_missing_reject_no_resolve(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_fixture(root)
            path = root / "Surge-Rules.conf"
            text = path.read_text(encoding="utf-8").replace("REJECT,no-resolve", "REJECT")
            text = text.replace("ROUTER:192.168.3.1", "ROUTER:192.168.3.2")
            path.write_text(text, encoding="utf-8")
            errors, _ = check_repository(root)
            self.assertTrue(any("RULE-SET paths" in error for error in errors))
            self.assertTrue(any("mesh rules changed" in error for error in errors))

    def test_rejects_reintroduced_cloudflare_asn_catchall(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_fixture(root)
            path = root / "rules/First.list"
            path.write_text(path.read_text() + "IP-ASN,13335,no-resolve\n", encoding="utf-8")
            self.assertTrue(any("broad ASN13335 routing is disabled" in error
                                for error in check_repository(root)[0]))
            path.write_text("DOMAIN-SUFFIX,example.com\n", encoding="utf-8")
            config = root / "Surge-Rules.conf"
            config.write_text(config.read_text().replace("FINAL,", 'IP-ASN,13335,"AI"\nFINAL,'), encoding="utf-8")
            self.assertTrue(any("tail changed or moved" in error for error in check_repository(root)[0]))

    def test_rejects_documentation_in_rules_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_fixture(root)
            (root / "rules/README.md").write_text("Documentation belongs outside rules.\n", encoding="utf-8")
            errors, _ = check_repository(root)
            self.assertTrue(any("unexpected non-rule entry: README.md" in error for error in errors))

    def test_detects_rule_file_moved_back_to_root(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_fixture(root)
            (root / "rules/First.list").rename(root / "First.list")
            errors, counts = check_repository(root)
            self.assertTrue(any("rule file must be inside rules/: First.list" in error for error in errors))
            self.assertNotIn("First.list", counts)


if __name__ == "__main__":
    unittest.main()
