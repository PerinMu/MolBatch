from __future__ import annotations


def parse_chain_string(chain_string: str) -> list[str]:
    cleaned = (
        chain_string.replace(",", " ")
        .replace(";", " ")
        .replace("+", " ")
        .strip()
    )
    if not cleaned:
        raise ValueError("Empty chain string")
    if " " in cleaned:
        chains = [part.strip() for part in cleaned.split() if part.strip()]
    else:
        chains = list(cleaned)
    if not chains:
        raise ValueError("No chains parsed")
    return chains


def merge_unique_chain_strings(*chain_strings: str) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for chain_string in chain_strings:
        if not chain_string:
            continue
        for chain in parse_chain_string(chain_string):
            if chain not in seen:
                seen.add(chain)
                merged.append(chain)
    return merged
