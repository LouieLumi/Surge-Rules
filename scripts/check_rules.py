#!/usr/bin/env python3
"""Validate published rule sets, deduplication and the subscription order.

The domain routing helper is a static check of DOMAIN, DOMAIN-SUFFIX and
DOMAIN-KEYWORD only. It is not a Surge traffic test and cannot simulate DNS,
IP/ASN databases, user agents, processes, TLS SNI or routing policies.
"""

import argparse
import ipaddress
import json
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple, Union

from rulelib import Rule, RuleIndex, load_rules


ROOT = Path(__file__).resolve().parents[1]
LOCAL_FILES = ("ApplicationDirect", "ApplicationReject")
MESH_LINES = (
    "AND,((NOT,((SUBNET,ROUTER:192.168.3.1))), (IP-CIDR,192.168.3.0/24,no-resolve)),🍀 望京组网",
    "AND,((NOT,((SUBNET,ROUTER:192.168.5.2))), (IP-CIDR,192.168.5.0/24,no-resolve)),🍀 望京组网",
    "AND,((NOT,((SUBNET,ROUTER:192.168.0.1))), (IP-CIDR,192.168.0.0/24,no-resolve)),🍀 望京组网",
    "AND,((NOT,((SUBNET,ROUTER:192.168.22.3))), (IP-CIDR,192.168.22.0/24,no-resolve)),🍀 辽宁组网",
    "AND,((NOT,((SUBNET,ROUTER:192.168.31.1))), (IP-CIDR,192.168.31.0/24,no-resolve)),🍀 北京组网",
)
TAIL_LINES = (
    "GEOIP,CN,DIRECT",
    'IP-ASN,13335,"👾 人工智能"',
    "FINAL,✨ 星链网络,dns-failed",
)


def _manifest(root: Path) -> dict:
    manifest = json.loads((root / "rulesets.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported rulesets.json schema_version")
    base_url = manifest.get("base_url")
    if not isinstance(base_url, str) or not base_url.startswith("https://") or not base_url.endswith("/"):
        raise ValueError("rulesets.json base_url must be an HTTPS directory URL")
    entries = manifest.get("rulesets")
    if not isinstance(entries, list) or not entries:
        raise ValueError("rulesets.json rulesets must be a nonempty list")
    names = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("rulesets.json contains a non-object entry")
        name, policy = entry.get("file"), entry.get("policy")
        if not isinstance(name, str) or Path(name).name != name or not name.endswith(".list"):
            raise ValueError("invalid rule-set filename: {!r}".format(name))
        if name in names:
            raise ValueError("duplicate rulesets.json file: " + name)
        names.add(name)
        if not isinstance(policy, str) or not policy.strip():
            raise ValueError("missing rule-set policy: " + name)
    return manifest


def _broad_first(rule: Rule) -> tuple:
    """Order only the proved inclusion families from parents to children."""
    if rule.kind == "DOMAIN-SUFFIX":
        return (0, len(rule.value.split(".")), rule.value, rule.options)
    if rule.kind == "DOMAIN":
        return (1, 0, rule.value, rule.options)
    if rule.kind in {"IP-CIDR", "IP-CIDR6"}:
        network = ipaddress.ip_network(rule.value)
        return (2, network.version, network.prefixlen, int(network.network_address), rule.options)
    return (3, rule.kind, rule.value, rule.options)


def _reference(line: str) -> Tuple[str, ...]:
    fields = [field.strip() for field in line.split(",")]
    if len(fields) < 3 or fields[0] != "RULE-SET":
        raise ValueError("invalid RULE-SET reference: " + line)
    # These controlled subscription URLs and policies contain no commas.
    if fields[2].startswith(("'", '"')):
        if len(fields[2]) < 2 or fields[2][-1] != fields[2][0]:
            raise ValueError("unbalanced policy quotes: " + line)
        fields[2] = fields[2][1:-1]
    return tuple(fields)


def _check_config(root: Path, manifest: dict, errors: List[str]) -> None:
    path = root / "Surge-Rules.conf"
    try:
        original = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        errors.append("Surge-Rules.conf: " + str(exc))
        return
    active = []
    for line in original:
        if not line.strip() or line.lstrip().startswith(("#", ";", "//")):
            continue
        if line.strip() == "[Rule]":
            continue
        active.append(line)
    base = manifest["base_url"]
    expected_references = [
        ("RULE-SET", base + "ApplicationDirect", "DIRECT"),
        ("RULE-SET", base + "ApplicationReject", "REJECT", "no-resolve"),
    ] + [("RULE-SET", base + entry["file"], entry["policy"]) for entry in manifest["rulesets"]]
    actual_references = []
    for line in active:
        if line.strip().startswith("RULE-SET,"):
            try:
                reference = _reference(line.strip())
                if len(actual_references) >= 2 and len(reference) > 3:
                    if len(reference) == 4 and re.fullmatch(r"update-interval=-?[0-9]+", reference[3]):
                        reference = reference[:3]
                    else:
                        errors.append("Surge-Rules.conf: unexpected category RULE-SET option: " + line)
                actual_references.append(reference)
            except ValueError as exc:
                errors.append("Surge-Rules.conf: " + str(exc))
    if actual_references != expected_references:
        errors.append("Surge-Rules.conf: RULE-SET paths, policies, options or order differ from rulesets.json")
    expected_length = len(expected_references) + len(MESH_LINES) + len(TAIL_LINES)
    if len(active) != expected_length:
        errors.append("Surge-Rules.conf: expected {} active rules, found {}".format(expected_length, len(active)))
    if tuple(active[2:7]) != MESH_LINES:
        errors.append("Surge-Rules.conf: the five original mesh rules changed or moved")
    if tuple(active[-3:]) != TAIL_LINES:
        errors.append("Surge-Rules.conf: GEOIP / ASN13335 / FINAL tail changed or moved")
    # Comparing the complete rule shape catches a misplaced fallback or an
    # additional rule even when the subsequence of RULE-SET lines is correct.
    expected_shape = ["RULE-SET"] * 2 + list(MESH_LINES) + ["RULE-SET"] * len(manifest["rulesets"]) + list(TAIL_LINES)
    actual_shape = ["RULE-SET" if line.strip().startswith("RULE-SET,") else line for line in active]
    if actual_shape != expected_shape:
        errors.append("Surge-Rules.conf: active rule layout differs from the protected subscription layout")


def check_repository(root: Union[str, Path] = ROOT) -> Tuple[List[str], Dict[str, int]]:
    """Return (errors, per-file rule counts), without modifying any file."""
    root = Path(root)
    errors: List[str] = []
    counts: Dict[str, int] = {}
    try:
        manifest = _manifest(root)
    except (OSError, ValueError) as exc:
        return ["rulesets.json: " + str(exc)], counts

    loaded: Dict[str, List[Rule]] = {}
    for name in list(LOCAL_FILES) + [entry["file"] for entry in manifest["rulesets"]]:
        try:
            rules = load_rules(root / name)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
            continue
        counts[name], loaded[name] = len(rules), rules
        if not rules:
            errors.append(name + ": empty rule set")
        for rule in rules:
            if rule.kind == "IP-ASN" and rule.value == "13335":
                errors.append(name + ": ASN13335 must remain only in the protected configuration tail")

    previous = RuleIndex()
    for entry in manifest["rulesets"]:
        name = entry["file"]
        if name not in loaded:
            continue
        rules = loaded[name]
        within = RuleIndex()
        for rule in sorted(rules, key=_broad_first):
            covered = within.covering(rule)
            if covered is not None:
                errors.append("{}: redundant {} covered by {}".format(name, rule.render(), covered[0].render()))
            within.add(rule, name)
        for rule in rules:
            covered = previous.covering(rule)
            if covered is not None:
                errors.append("{}: {} already covered by {} in preceding {}".format(
                    name, rule.render(), covered[0].render(), covered[1]))
        for rule in rules:
            previous.add(rule, name)
    # The two original local override lists are parsed, but deliberately not
    # deduplicated or included in the generated categories' ownership index.
    _check_config(root, manifest, errors)
    return errors, counts


DomainRoutes = List[Tuple[str, str, List[Rule]]]


def load_domain_routes(root: Union[str, Path] = ROOT) -> DomainRoutes:
    """Load the configured category order for static hostname-only checks."""
    root = Path(root)
    manifest = _manifest(root)
    entries = [("ApplicationDirect", "DIRECT"), ("ApplicationReject", "REJECT")]
    entries += [(entry["file"], entry["policy"]) for entry in manifest["rulesets"]]
    return [(name, policy, [rule for rule in load_rules(root / name)
                           if rule.kind in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"}])
            for name, policy in entries]


def first_match_domain(hostname: str, root: Union[str, Path] = ROOT,
                       routes: Optional[DomainRoutes] = None) -> Optional[Tuple[str, str]]:
    """Return (rule-set filename, policy) for a hostname's first static match.

    A None result means none of these three domain rule types matched. It
    does not assert that actual Surge traffic would reach FINAL.
    """
    host = hostname.lower().rstrip(".")
    if not host or any(char.isspace() for char in host):
        raise ValueError("expected a nonempty hostname without whitespace")
    if routes is None:
        routes = load_domain_routes(root)
    for name, policy, rules in routes:
        for rule in rules:
            if rule.kind == "DOMAIN" and host == rule.value:
                return name, policy
            if rule.kind == "DOMAIN-SUFFIX" and (host == rule.value or host.endswith("." + rule.value)):
                return name, policy
            if rule.kind == "DOMAIN-KEYWORD" and rule.value in host:
                return name, policy
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (defaults to the script's repository)")
    args = parser.parse_args()
    errors, counts = check_repository(args.root)
    if errors:
        for error in errors:
            print("ERROR: " + error)
        print("FAILED: {} validation errors".format(len(errors)))
        return 1
    print("OK: {} rule sets, {} rules; syntax, conservative deduplication and subscription order passed".format(
        len(counts), sum(counts.values())))
    print("Static validation only; no live Surge traffic was tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
