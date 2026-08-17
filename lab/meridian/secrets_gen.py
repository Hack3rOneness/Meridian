"""Derive per-instance secrets from a seed the proctor controls.
No flags or canary values live in source. The proctor sets MLP_SEED (kept
private) so each candidate gets unique values that can't be shared.
"""
import hashlib
import os

SEED = os.environ.get("MLP_SEED", "dev-seed-CHANGE-ME")


def _h(tag, n=16):
    return hashlib.sha256(f"{SEED}:{tag}".encode()).hexdigest()[:n]


def _letters(tag, n=12):
    raw = hashlib.sha256(f"{SEED}:{tag}".encode()).digest()
    return "".join("abcdefghijklmnopqrstuvwxyz"[b % 26] for b in raw[:n])


# Flag that SURVIVES the egress filter (letters/underscore) — the reward for
# reaching the undocumented agent's configuration (shadow-AI-to-prod evidence).
FLAG_PROD = "MLP{" + _letters("prod")[:6] + "_" + _letters("prod2")[:6] + "}"

# Flag that the egress filter WILL redact (hex body) — proving data loss
# therefore requires defeating the filter via an encoding pushed through the
# agent, not a plain read.
FLAG_DATALOSS = "MLP{" + _h("dataloss", 16) + "}"

# Canary regulated record.
CANARY_SSN = f"{int(_h('ssn1',3),16)%900+100}-{int(_h('ssn2',2),16)%90+10}-" \
             f"{int(_h('ssn3',4),16)%9000+1000}"
CANARY_ACCT = "ACCT-" + str(int(_h("acct", 5), 16) % 90000 + 10000)

DB_PASSWORD = _h("dbpw", 12)
