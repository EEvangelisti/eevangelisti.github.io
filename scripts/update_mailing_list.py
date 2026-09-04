#!/usr/bin/env python3
"""
Synchronise the public OMGN mailing-list data from Airtable.

The Airtable token is NEVER stored in this file. It must be supplied through
the AIRTABLE_TOKEN environment variable (e.g. a GitHub Actions secret).

Required environment variables:
    AIRTABLE_TOKEN
    AIRTABLE_BASE_ID
    AIRTABLE_TABLE_ID

Output:
    _data/mailing_list.yml

Only the following Airtable fields are exported:
    - "NOM, Prénom"
    - "Institution"
    - "Country"

In particular, email addresses and all other Airtable fields are deliberately
excluded from the generated public file.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


API_ROOT = "https://api.airtable.com/v0"

NAME_FIELD = "LAST NAME, First name"
INSTITUTION_FIELD = "Institute"
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
    """
    Fetch all records from Airtable, following pagination.

    fields[] is used deliberately so that fields such as email addresses are
    not even requested from Airtable by this synchronisation script.
    """
    records = []
    offset = None

    while True:
        params = [
            ("pageSize", "100"),
            ("fields[]", NAME_FIELD),
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


def split_name(raw_name: str) -> tuple[str, str, str]:
    """
    Parse the Airtable field 'NOM, Prénom'.

    Expected form:
        DUPONT, Jean  -> last_name='DUPONT', first_name='Jean'

    If no comma is present, the value is kept intact:
        Cher          -> last_name='Cher', first_name=''

    display_name is included now to make the later transition to a single
    Name column straightforward.
    """
    raw_name = " ".join(str(raw_name or "").split())

    if "," in raw_name:
        last_name, first_name = raw_name.split(",", 1)
        last_name = last_name.strip().upper()
        first_name = first_name.strip()
        display_name = " ".join(part for part in (last_name, first_name) if part)
    else:
        last_name = raw_name
        first_name = ""
        display_name = raw_name

    return last_name, first_name, display_name


def yaml_string(value: str) -> str:
    """
    Return a safely quoted YAML scalar.

    JSON double-quoted strings are valid YAML scalars, so this avoids adding
    a PyYAML dependency to the repository.
    """
    return json.dumps(str(value or ""), ensure_ascii=False)


def normalise_records(records: list[dict]) -> list[dict]:
    public_records = []

    for record in records:
        fields = record.get("fields", {})

        raw_name = fields.get(NAME_FIELD, "")
        institution = fields.get(INSTITUTION_FIELD, "")
        country = fields.get(COUNTRY_FIELD, "")

        last_name, first_name, display_name = split_name(raw_name)

        # Ignore completely empty rows.
        if not any((display_name, institution, country)):
            continue

        public_records.append(
            {
                "last_name": last_name,
                "first_name": first_name,
                "display_name": display_name,
                "affiliation_main": " ".join(str(institution or "").split()),
                "country": " ".join(str(country or "").split()),
                # Compatible with the current Liquid sort in mailing-list.md.
                "sort_name": (last_name or display_name).casefold(),
            }
        )

    public_records.sort(
        key=lambda person: (
            person["sort_name"],
            person["first_name"].casefold(),
            person["affiliation_main"].casefold(),
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
            f"Updated {OUTPUT_FILE} with {len(public_records)} public mailing-list entries."
        )
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
