#!/usr/bin/env python3
"""
Synchronise the public OMGN mailing-list data from Airtable.

Required environment variables:
    AIRTABLE_TOKEN
    AIRTABLE_BASE_ID
    AIRTABLE_TABLE_ID

Output:
    _data/mailing_list.yml

Only these Airtable fields are requested:
    - "Last name"
    - "First name"
    - "Institution"
    - "Country"

Email addresses and all other fields are deliberately excluded.

Duplicate public entries are collapsed by normalized first name + last name.
When duplicate records exist, institution and country are merged so that
the most complete public information is preserved.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
import unicodedata
from pathlib import Path

API_ROOT = "https://api.airtable.com/v0"

LAST_NAME_FIELD = "Last name"
FIRST_NAME_FIELD = "First name"
INSTITUTION_FIELD = "Institution"
COUNTRY_FIELD = "Country"

OUTPUT_FILE = Path("_data/mailing_list.yml")


def get_required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def airtable_get(url: str, token: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except Exception as exc:
        raise RuntimeError(f"Airtable request failed: {exc}") from exc


def fetch_records(token: str, base_id: str, table_id: str) -> list[dict]:
    records = []
    offset = None

    while True:
        params = [
            ("pageSize", "100"),
            ("fields[]", LAST_NAME_FIELD),
            ("fields[]", FIRST_NAME_FIELD),
            ("fields[]", INSTITUTION_FIELD),
            ("fields[]", COUNTRY_FIELD),
        ]

        if offset:
            params.append(("offset", offset))

        query = urllib.parse.urlencode(params)
        table = urllib.parse.quote(table_id, safe="")
        url = f"{API_ROOT}/{base_id}/{table}?{query}"

        payload = airtable_get(url, token)
        records.extend(payload.get("records", []))

        offset = payload.get("offset")
        if not offset:
            break

    return records


def clean_text(value) -> str:
    return " ".join(str(value or "").split())


def normalize_for_comparison(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", clean_text(value))
    without_marks = "".join(
        ch for ch in normalized if not unicodedata.combining(ch)
    )
    return without_marks.casefold()


def yaml_string(value: str) -> str:
    return json.dumps(str(value or ""), ensure_ascii=False)


def choose_more_complete(old: str, new: str) -> str:
    old = clean_text(old)
    new = clean_text(new)

    if not old:
        return new
    if not new:
        return old
    if old == new:
        return old

    return new if len(new) > len(old) else old


def normalise_records(records: list[dict]) -> list[dict]:
    unique = {}

    for record in records:
        fields = record.get("fields", {})

        last_name = clean_text(fields.get(LAST_NAME_FIELD, "")).upper()
        first_name = clean_text(fields.get(FIRST_NAME_FIELD, ""))
        institution = clean_text(fields.get(INSTITUTION_FIELD, ""))
        country = clean_text(fields.get(COUNTRY_FIELD, ""))

        if not any((last_name, first_name, institution, country)):
            continue

        display_name = (
            f"{last_name}, {first_name}"
            if last_name and first_name
            else last_name or first_name
        )

        key = (
            normalize_for_comparison(last_name),
            normalize_for_comparison(first_name),
        )

        if not any(key):
            key = ("__airtable_record__", record.get("id", ""))

        current = {
            "last_name": last_name,
            "first_name": first_name,
            "display_name": display_name,
            "affiliation_main": institution,
            "country": country,
            "sort_name": normalize_for_comparison(last_name or first_name),
        }

        if key not in unique:
            unique[key] = current
            continue

        existing = unique[key]
        existing["affiliation_main"] = choose_more_complete(
            existing["affiliation_main"],
            current["affiliation_main"],
        )
        existing["country"] = choose_more_complete(
            existing["country"],
            current["country"],
        )

    public_records = list(unique.values())

    public_records.sort(
        key=lambda person: (
            person["sort_name"],
            normalize_for_comparison(person["first_name"]),
            normalize_for_comparison(person["affiliation_main"]),
        )
    )

    return public_records


def write_yaml(records: list[dict], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# This file is generated automatically from Airtable.",
        "# Do not edit it manually.",
        "",
    ]

    for person in records:
        lines.extend(
            [
                f"- last_name: {yaml_string(person['last_name'])}",
                f"  first_name: {yaml_string(person['first_name'])}",
                f"  display_name: {yaml_string(person['display_name'])}",
                f"  affiliation_main: {yaml_string(person['affiliation_main'])}",
                f"  country: {yaml_string(person['country'])}",
                f"  sort_name: {yaml_string(person['sort_name'])}",
            ]
        )

    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    try:
        token = get_required_env("AIRTABLE_TOKEN")
        base_id = get_required_env("AIRTABLE_BASE_ID")
        table_id = get_required_env("AIRTABLE_TABLE_ID")

        records = fetch_records(token, base_id, table_id)
        public_records = normalise_records(records)
        write_yaml(public_records, OUTPUT_FILE)

        print(
            f"Updated {OUTPUT_FILE}: "
            f"{len(records)} Airtable records -> "
            f"{len(public_records)} unique public entries."
        )
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
