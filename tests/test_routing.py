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
from check_rules import MESH_LINES, TAIL_LINES, check_repository, first_match_domain, load_domain_routes
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
        for hostname in ("generativelanguage.googleapis.com", "notebooklm.google", "notebooklm.google.com", "google.com", "gemini.google.com"):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, "Gemini.list", "🧿 谷歌服务")

    def test_apple_intelligence_precedes_apple(self):
        for hostname in ("apple-relay.apple.com", "gspe1-ssl.ls.apple.com"):
            self.assert_category(hostname, "AppleIntelligence.list", "👾 人工智能")
        self.assert_category("www.apple.com", "Apple.list", "🍎 苹果服务")

    def test_ai_domain_ownership(self):
        for hostname, filename in (("claude.ai", "Claude.list"), ("api.anthropic.com", "Claude.list"),
                                   ("chatgpt.com", "OpenAI.list"), ("chat.com", "OpenAI.list"),
                                   ("ai.com", "OtherAI.list")):
            with self.subTest(hostname=hostname):
                self.assert_category(hostname, filename, "👾 人工智能")

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
        self.assert_category("api.stripe.com", "Proxy.list", "👾 人工智能")

    def test_hostname_normalization(self):
        self.assert_category("YOUTUBEI.GOOGLEAPIS.COM.", "YouTube.list", "📹 油管视频")

    def test_all_published_files_and_protected_configuration(self):
        errors, counts = check_repository(ROOT)
        self.assertEqual(errors, [], "\n".join(errors))
        self.assertEqual(len(counts), 21)

    def test_cloudflare_asn_remains_only_in_configuration_tail(self):
        manifest = json.loads((ROOT / "rulesets.json").read_text(encoding="utf-8"))
        for entry in manifest["rulesets"]:
            self.assertFalse(any(rule.kind == "IP-ASN" and rule.value == "13335"
                                 for rule in load_rules(ROOT / entry["file"])), entry["file"])
        active = [line for line in (ROOT / "Surge-Rules.conf").read_text(encoding="utf-8").splitlines()
                  if line.strip() and not line.lstrip().startswith(("#", ";", "//"))]
        self.assertEqual(tuple(active[-3:]), TAIL_LINES)
        self.assertEqual(sum(line.startswith("IP-ASN,13335,") for line in active), 1)


class CheckerFailureTests(unittest.TestCase):
    """Prove malformed output is detected, including reverse-order overlap."""

    def make_fixture(self, root):
        manifest = {"schema_version": 1, "base_url": "https://example.com/", "rulesets": [
            {"file": "First.list", "policy": "Proxy"}, {"file": "Second.list", "policy": "DIRECT"}]}
        (root / "rulesets.json").write_text(json.dumps(manifest), encoding="utf-8")
        (root / "ApplicationDirect").write_text("PROCESS-NAME,LocalApp\n", encoding="utf-8")
        (root / "ApplicationReject").write_text("PROCESS-NAME,BlockedApp\n", encoding="utf-8")
        (root / "First.list").write_text("DOMAIN-SUFFIX,example.com\n", encoding="utf-8")
        (root / "Second.list").write_text("DOMAIN,unrelated.test\n", encoding="utf-8")
        config = ["[Rule]", "RULE-SET,https://example.com/ApplicationDirect,DIRECT",
                  "RULE-SET,https://example.com/ApplicationReject,REJECT,no-resolve"]
        config += list(MESH_LINES)
        config += ["RULE-SET,https://example.com/First.list,Proxy", "RULE-SET,https://example.com/Second.list,DIRECT"]
        config += list(TAIL_LINES)
        (root / "Surge-Rules.conf").write_text("\n".join(config) + "\n", encoding="utf-8")

    def test_detects_parent_suffix_even_when_it_appears_after_child(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_fixture(root)
            self.assertEqual(check_repository(root)[0], [])
            (root / "First.list").write_text("DOMAIN,api.example.com\nDOMAIN-SUFFIX,example.com\n", encoding="utf-8")
            errors, _ = check_repository(root)
            self.assertTrue(any("First.list: redundant DOMAIN,api.example.com" in error for error in errors))

    def test_detects_cross_category_coverage(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_fixture(root)
            (root / "Second.list").write_text("DOMAIN,api.example.com\n", encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
