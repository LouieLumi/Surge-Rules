"""Conservative parsing and coverage checks for the project's Surge rule sets.

This is intentionally not a full Surge profile parser. Policy columns, FINAL,
logical rules and unknown options fail closed rather than being silently lost.
Coverage proves complete inclusion; it does not guess from keywords or live
DNS/ASN data. All code uses only the Python 3.9 standard library.
"""

from dataclasses import dataclass
import ipaddress
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple, Union


DOMAIN_KINDS = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-WILDCARD"}
IP_KINDS = {"IP-CIDR", "IP-CIDR6"}
SUPPORTED_KINDS = DOMAIN_KINDS | IP_KINDS | {
    "IP-ASN", "GEOIP", "USER-AGENT", "PROCESS-NAME", "URL-REGEX"
}
SUPPORTED_OPTIONS = {"no-resolve", "extended-matching"}


@dataclass(frozen=True)
class Rule:
    kind: str
    value: str
    options: Tuple[str, ...] = ()

    def render(self) -> str:
        """Return a policy-free rule; quote values only when syntax requires it."""
        value = self.value
        if ("," in value or value != value.strip() or
                value.startswith(("'", '"')) or re.search(r"\s(?://|#|;)", value)):
            quote = "'" if '"' in value and "'" not in value else '"'
            value = quote + value.replace(quote, quote + quote) + quote
        return ",".join((self.kind, value) + self.options)


def _fields(line: str) -> List[str]:
    """Split quoted fields and remove only whitespace-introduced comments.

    Backslashes are preserved, notably in URL regular expressions. Quoted
    commas and comment markers remain data. Both Surge quote styles work.
    """
    result: List[str] = []
    field: List[str] = []
    quote: Optional[str] = None
    was_quoted = False
    closed = False
    i = 0
    while i < len(line):
        char = line[i]
        if quote is not None:
            if char == quote:
                # A backslash-escaped quote is expression data, not a delimiter.
                slashes = 0
                for previous in reversed(field):
                    if previous != "\\":
                        break
                    slashes += 1
                if slashes % 2:
                    field.append(char)
                elif i + 1 < len(line) and line[i + 1] == quote:
                    field.append(char)
                    i += 1
                else:
                    quote = None
                    closed = True
            else:
                field.append(char)
        else:
            comment = char in "#;" or line.startswith("//", i)
            if comment and (i == 0 or line[i - 1].isspace()):
                break
            if char == ",":
                result.append("".join(field) if was_quoted else "".join(field).strip())
                field, was_quoted, closed = [], False, False
            elif closed:
                if not char.isspace():
                    raise ValueError("unexpected text after a quoted field")
            elif char in "\"'" and not "".join(field).strip():
                field, was_quoted, quote = [], True, char
            else:
                field.append(char)
        i += 1
    if quote is not None:
        raise ValueError("unterminated quoted field")
    result.append("".join(field) if was_quoted else "".join(field).strip())
    return result


def parse_line(line: str) -> Optional[Rule]:
    """Parse one external RULE-SET entry, returning None for blank/comments.

    Only the source rule types and known policy-free options are accepted.
    Hostnames/keywords are case-insensitive; UA, process and regex values are
    not transformed. Options retain their order for conservative equality.
    """
    line = line.strip().lstrip("\ufeff")
    if not line or line.startswith(("#", "//", ";")):
        return None
    if "\n" in line or "\r" in line:
        raise ValueError("expected one rule per line")
    fields = _fields(line)
    if len(fields) < 2:
        raise ValueError("rule requires a type and a value")
    kind, value = fields[0].upper(), fields[1]
    if kind not in SUPPORTED_KINDS:
        raise ValueError("unsupported rule type: " + kind)
    if not value:
        raise ValueError("rule value is empty")
    options = tuple(fields[2:])
    if any(option not in SUPPORTED_OPTIONS for option in options):
        raise ValueError("unknown rule-set option or unexpected policy column")
    if len(options) != len(set(options)):
        raise ValueError("duplicate rule-set option")
    if "no-resolve" in options and kind not in IP_KINDS | {"IP-ASN", "GEOIP"}:
        raise ValueError("no-resolve requires an IP rule")
    if "extended-matching" in options and kind not in DOMAIN_KINDS | {"URL-REGEX"}:
        raise ValueError("extended-matching requires a domain or URL rule")
    if kind in DOMAIN_KINDS:
        if any(char.isspace() for char in value) or "," in value:
            raise ValueError("invalid domain rule value")
        value = value.lower()
        if kind in {"DOMAIN", "DOMAIN-SUFFIX"}:
            value = value.rstrip(".")
            if not value or value.startswith(".") or ".." in value:
                raise ValueError("invalid hostname")
    elif kind in IP_KINDS:
        try:
            network = ipaddress.ip_network(value, strict=False)
        except ValueError as exc:
            raise ValueError("invalid IP network: " + value) from exc
        expected = 4 if kind == "IP-CIDR" else 6
        if network.version != expected:
            raise ValueError("IP network family does not match rule type")
        value = str(network)
    elif kind == "IP-ASN":
        number = value[2:] if value.upper().startswith("AS") else value
        if not number.isascii() or not number.isdecimal() or not 0 <= int(number) <= 4294967295:
            raise ValueError("invalid ASN: " + value)
        value = str(int(number))
    elif kind == "GEOIP":
        if not re.fullmatch(r"[a-zA-Z]{2}", value):
            raise ValueError("invalid GEOIP country code")
        value = value.upper()
    return Rule(kind, value, options)


def load_rules(path: Union[str, Path]) -> List[Rule]:
    """Read UTF-8 rules and annotate parse failures with filename and line."""
    path = Path(path)
    rules: List[Rule] = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        try:
            rule = parse_line(line)
        except ValueError as exc:
            raise ValueError("{}:{}: {}".format(path, number, exc)) from exc
        if rule is not None:
            rules.append(rule)
    return rules


Entry = Tuple[int, Rule, str]


class RuleIndex:
    """Index canonical Rules and identify the earliest complete covering rule.

    Domain queries inspect only their label ancestors, never all stored
    domains. CIDR queries inspect at most 33/129 network prefix ancestors.
    Owner is an opaque category name returned unchanged to callers.
    """

    def __init__(self) -> None:
        self._sequence = 0
        self._exact: Dict[Rule, Entry] = {}
        self._suffixes: Dict[Tuple[str, Tuple[str, ...]], Entry] = {}
        self._networks: Dict[Tuple[int, int, int, Tuple[str, ...]], Entry] = {}

    def add(self, rule: Rule, owner: str) -> None:
        entry = (self._sequence, rule, owner)
        self._sequence += 1
        self._exact.setdefault(rule, entry)
        if rule.kind == "DOMAIN-SUFFIX":
            self._suffixes.setdefault((rule.value, rule.options), entry)
        elif rule.kind in IP_KINDS:
            network = ipaddress.ip_network(rule.value, strict=False)
            key = (network.version, network.prefixlen, int(network.network_address), rule.options)
            self._networks.setdefault(key, entry)

    def covering(self, rule: Rule) -> Optional[Tuple[Rule, str]]:
        """Return (covering_rule, owner), or None if inclusion is unproved."""
        candidates: List[Entry] = []
        exact = self._exact.get(rule)
        if exact is not None:
            candidates.append(exact)
        if rule.kind in {"DOMAIN", "DOMAIN-SUFFIX"}:
            labels = rule.value.split(".")
            for i in range(len(labels)):
                suffix = self._suffixes.get((".".join(labels[i:]), rule.options))
                if suffix is not None:
                    candidates.append(suffix)
        elif rule.kind in IP_KINDS:
            network = ipaddress.ip_network(rule.value, strict=False)
            address, width = int(network.network_address), network.max_prefixlen
            for prefix in range(network.prefixlen, -1, -1):
                shift = width - prefix
                ancestor = (address >> shift) << shift
                entry = self._networks.get((network.version, prefix, ancestor, rule.options))
                if entry is not None:
                    candidates.append(entry)
        if not candidates:
            return None
        _, covering_rule, owner = min(candidates, key=lambda entry: entry[0])
        return covering_rule, owner
