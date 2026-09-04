#!/usr/bin/env python3
"""Validate the public ISPD-Opt author-generated subset and its checksums."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
CSV = ROOT / "ISPD_Opt_Author_Generated_Email_Subset_v1.0.csv"
EXPECTED_CSV_SHA256 = "af7c858690f8e6286d9618e96abc98ecb96815a2a2cbe4738faa0706c8ab190e"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


errors: list[str] = []
if sha256(CSV) != EXPECTED_CSV_SHA256:
    errors.append("Release CSV SHA-256 mismatch")

frame = pd.read_csv(CSV, low_memory=False)
if frame.shape != (1800, 32):
    errors.append(f"Unexpected CSV shape: {frame.shape}")
if frame["class_label"].value_counts().to_dict() != {"GL": 900, "GP": 900}:
    errors.append("Generated class distribution mismatch")
if frame["generator"].value_counts().to_dict() != {
    "chatgpt": 800,
    "claude": 800,
    "gemini": 200,
}:
    errors.append("Generator distribution mismatch")
if not frame["authorship"].eq("ai").all():
    errors.append("Non-AI authorship row detected")
if frame["record_id"].duplicated().any():
    errors.append("Duplicate record_id detected")
if frame["text"].duplicated().any():
    errors.append("Duplicate exact text detected")
calculated = frame["text"].astype(str).map(
    lambda value: hashlib.sha256(value.encode("utf-8")).hexdigest()
)
if not calculated.eq(frame["text_sha256"].astype(str)).all():
    errors.append("Stored text hash mismatch")

checksum_file = ROOT / "SHA256SUMS.txt"
for line in checksum_file.read_text(encoding="utf-8").splitlines():
    expected, name = line.split("  ", 1)
    target = ROOT / name
    if not target.exists():
        errors.append(f"Missing checksum target: {name}")
    elif sha256(target) != expected:
        errors.append(f"Checksum mismatch: {name}")

if errors:
    print("RELEASE VALIDATION: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("RELEASE VALIDATION: PASS")
print("Validated 1,800 exact author-generated records; no human-source rows included.")
