"""Regression tests for safe, policy-preserving rule-set deduplication."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from rulelib import Rule, RuleIndex, load_rules, parse_line


class ParsingTests(unittest.TestCase):
    def test_comments_and_telegram_asn_annotation(self):
        for line in ("", "  ", "# title", " // source", "; comment", "\ufeff# BOM"):
            self.assertIsNone(parse_line(line))
        self.assertEqual(parse_line("IP-ASN,AS044907,no-resolve // Telegram Messenger Inc"),
                         Rule("IP-ASN", "44907", ("no-resolve",)))

    def test_domain_and_ip_normalization(self):
        self.assertEqual(parse_line("domain-suffix,EXAMPLE.Com."), Rule("DOMAIN-SUFFIX", "example.com"))
        self.assertEqual(parse_line("IP-CIDR,192.0.2.123/24,no-resolve").value, "192.0.2.0/24")
        self.assertEqual(parse_line("IP-CIDR6,2001:0DB8::1234/32").value, "2001:db8::/32")

    def test_case_and_internal_spaces_are_preserved_for_opaque_values(self):
        for kind, value in (("USER-AGENT", "My App*"), ("PROCESS-NAME", "My Browser"),
                            ("URL-REGEX", r"https://Example\.com/a#fragment;v=2")):
            rule = parse_line(kind + "," + value)
            self.assertEqual(rule.value, value)
            self.assertEqual(parse_line(rule.render()), rule)

    def test_quoted_regex_commas_and_comment_markers(self):
        rule = parse_line(r'URL-REGEX,"https://Example\.com/a{1,3}/ # data",extended-matching # comment')
        self.assertEqual(rule.value, r"https://Example\.com/a{1,3}/ # data")
        self.assertEqual(parse_line(rule.render()), rule)
        self.assertEqual(parse_line("USER-AGENT,'My App; // # Test*'"), Rule("USER-AGENT", "My App; // # Test*"))

    def test_non_whitespace_comment_markers_are_data(self):
        self.assertEqual(parse_line("URL-REGEX,https://example.com/#test;value").value,
                         "https://example.com/#test;value")
        self.assertEqual(parse_line("DOMAIN,example.com ; comment").value, "example.com")

    def test_invalid_entries_fail_instead_of_being_silently_discarded(self):
        for line in ("DOMAIN", "DOMAIN,", "DOMAIN,example.com,DIRECT", "FINAL,DIRECT",
                     "DOMAIN,example.com,pre-matching", "DOMAIN,example.com,no-resolve",
                     "IP-CIDR,2001:db8::/32", "IP-CIDR6,192.0.2.0/24", "IP-ASN,nope",
                     "IP-CIDR,999.0.0.0/24", 'URL-REGEX,"unclosed', "DOMAIN,has space.com",
                     "DOMAIN,a.example.com,extended-matching,extended-matching"):
            with self.subTest(line=line), self.assertRaises(ValueError):
                parse_line(line)

    def test_load_rules_reports_bad_line_number(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "source.list"
            path.write_text("# comment\nDOMAIN,example.com\nFINAL,DIRECT\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"source\.list:3:"):
                load_rules(path)


class CoverageTests(unittest.TestCase):
    def test_suffix_covers_root_and_children_with_label_boundaries(self):
        index = RuleIndex()
        parent = parse_line("DOMAIN-SUFFIX,example.com")
        index.add(parent, "Apple")
        for value in ("example.com", "api.example.com", "deep.api.example.com"):
            self.assertEqual(index.covering(Rule("DOMAIN", value)), (parent, "Apple"))
            self.assertEqual(index.covering(Rule("DOMAIN-SUFFIX", value)), (parent, "Apple"))
        for value in ("badexample.com", "example.com.evil.net", "com"):
            self.assertIsNone(index.covering(Rule("DOMAIN", value)))

    def test_preceding_exact_domain_does_not_cover_later_parent_suffix(self):
        index = RuleIndex()
        index.add(Rule("DOMAIN", "api.example.com"), "AI")
        self.assertIsNone(index.covering(Rule("DOMAIN-SUFFIX", "example.com")))
        self.assertIsNone(index.covering(Rule("DOMAIN-SUFFIX", "api.example.com")))
        self.assertIsNone(index.covering(Rule("DOMAIN", "other.example.com")))

    def test_options_are_part_of_coverage(self):
        index = RuleIndex()
        index.add(Rule("IP-CIDR", "192.0.2.0/24", ("no-resolve",)), "Proxy")
        self.assertIsNone(index.covering(Rule("IP-CIDR", "192.0.2.1/32")))
        self.assertIsNotNone(index.covering(Rule("IP-CIDR", "192.0.2.1/32", ("no-resolve",))))
        index.add(Rule("DOMAIN-SUFFIX", "example.com"), "Apple")
        self.assertIsNone(index.covering(Rule("DOMAIN", "api.example.com", ("extended-matching",))))

    def test_ipv4_ipv6_inclusion_and_family_separation(self):
        index = RuleIndex()
        index.add(Rule("IP-CIDR", "0.0.0.0/0"), "IPv4")
        self.assertIsNone(index.covering(Rule("IP-CIDR6", "::ffff:c000:0201/128")))
        index.add(Rule("IP-CIDR6", "2001:db8::/32"), "IPv6")
        self.assertEqual(index.covering(Rule("IP-CIDR6", "2001:db8:1::/48"))[1], "IPv6")
        self.assertIsNone(index.covering(Rule("IP-CIDR6", "2001:db9::/32")))
        self.assertIsNone(index.covering(Rule("IP-CIDR6", "2001::/16")))

    def test_shared_asn_or_keyword_never_proves_other_rule_coverage(self):
        index = RuleIndex()
        keyword = Rule("DOMAIN-KEYWORD", "google")
        index.add(keyword, "Google")
        index.add(Rule("IP-ASN", "13335"), "Cloudflare")
        self.assertEqual(index.covering(keyword), (keyword, "Google"))
        self.assertIsNone(index.covering(Rule("DOMAIN-SUFFIX", "google.com")))
        self.assertIsNone(index.covering(Rule("DOMAIN-KEYWORD", "googlevideo")))
        self.assertIsNone(index.covering(Rule("IP-CIDR", "1.1.1.0/24")))

    def test_ua_process_and_regex_only_match_exact_values(self):
        index = RuleIndex()
        for kind in ("USER-AGENT", "PROCESS-NAME", "URL-REGEX"):
            broad = Rule(kind, "App*")
            index.add(broad, kind)
            self.assertEqual(index.covering(broad), (broad, kind))
            self.assertIsNone(index.covering(Rule(kind, "AppSpecial")))
            self.assertIsNone(index.covering(Rule(kind, "app*")))

    def test_owner_is_earliest_actual_cover_not_most_specific(self):
        index = RuleIndex()
        first = Rule("DOMAIN-SUFFIX", "example.com")
        index.add(first, "first")
        index.add(Rule("DOMAIN", "api.example.com"), "second")
        index.add(first, "third")
        self.assertEqual(index.covering(Rule("DOMAIN", "api.example.com")), (first, "first"))
        network = Rule("IP-CIDR", "192.0.2.0/24")
        index.add(network, "network-first")
        index.add(Rule("IP-CIDR", "192.0.2.0/25"), "network-second")
        self.assertEqual(index.covering(Rule("IP-CIDR", "192.0.2.1/32")), (network, "network-first"))

    def test_many_domains_still_resolve_correct_ancestor(self):
        index = RuleIndex()
        for number in range(10000):
            index.add(Rule("DOMAIN-SUFFIX", "service{}.example".format(number)), str(number))
        self.assertEqual(index.covering(Rule("DOMAIN", "api.service9876.example"))[1], "9876")
        self.assertIsNone(index.covering(Rule("DOMAIN", "api.unknown.example")))


if __name__ == "__main__":
    unittest.main()
