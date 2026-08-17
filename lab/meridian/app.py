"""
Meridian Lending — Partner Origination Portal
Internal build. Assessment lab: runs only on an isolated host you control.
All companies, customers, and data are fictional.
"""
import base64
import hashlib
import hmac
import json
import re
import sqlite3
import time
from collections import defaultdict

import jwt
from flask import Flask, request, jsonify, Response, send_from_directory

import secrets_gen as S

app = Flask(__name__, static_folder=None)

with open("keys/private.pem") as f:
    PRIVATE_KEY = f.read()
with open("keys/public.pem") as f:
    PUBLIC_KEY = f.read()

CURRENT_KID = "mlp-2026-a"
LEGACY_KID = "legacy-2019"

AGENT_CONFIG = {
    "assistant": "loan-doc-review",
    "owner": "j.okafor (contractor)",
    "records_dsn": f"postgres://svc_review:{S.DB_PASSWORD}"
                   f"@prod-records.meridian.internal:5432/loans {S.FLAG_PROD}",
    "tools": ["search_records", "lookup_customer", "fetch_citation"],
}

_win = defaultdict(list)


@app.before_request
def _throttle():
    ip = request.remote_addr or "x"
    now = time.time()
    _win[ip] = [t for t in _win[ip] if now - t < 10]
    _win[ip].append(now)
    if len(_win[ip]) > 25:
        time.sleep(min(8, 0.4 * (len(_win[ip]) - 25)))


# ---- frontend -------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/oops")
def oops():
    return send_from_directory("frontend", "error.html")


@app.route("/static/<path:p>")
def static_files(p):
    return send_from_directory("frontend/static", p)


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow: /admin\nDisallow: /backup\n",
                   mimetype="text/plain")


@app.route("/admin")
@app.route("/backup")
def _restricted():
    return Response("403", status=403)


# ---- auth -----------------------------------------------------------------
@app.route("/.well-known/mlp-keys")
def jwks():
    return jsonify({"keys": [
        {"kid": CURRENT_KID, "kty": "RSA", "use": "sig", "pem": PUBLIC_KEY},
        {"kid": LEGACY_KID, "status": "deprecated"}]})


@app.route("/api/v2/login", methods=["POST"])
def login():
    b = request.get_json(silent=True) or {}
    if b.get("user") == "partner" and b.get("pass") == "partner123":
        return jsonify({"token": jwt.encode(
            {"sub": "partner", "role": "partner", "iat": int(time.time())},
            PRIVATE_KEY, algorithm="RS256", headers={"kid": CURRENT_KID})})
    time.sleep(1.5)
    return jsonify({"error": "invalid"}), 401


def _b64d(seg):
    return base64.urlsafe_b64decode(seg + "=" * (-len(seg) % 4))


def _verify(token):
    h_seg, p_seg, sig = token.split(".")
    header = json.loads(_b64d(h_seg))
    alg, kid = header.get("alg"), header.get("kid")
    if alg == "none":
        raise ValueError("rejected")
    if alg == "HS256" and kid == LEGACY_KID:
        want = base64.urlsafe_b64encode(hmac.new(
            PUBLIC_KEY.encode(), f"{h_seg}.{p_seg}".encode(),
            hashlib.sha256).digest()).rstrip(b"=").decode()
        if not hmac.compare_digest(want, sig):
            raise ValueError("sig")
        return json.loads(_b64d(p_seg))
    if alg == "RS256":
        return jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
    raise ValueError("unsupported")


def _claims(roles):
    a = request.headers.get("Authorization", "")
    if not a.startswith("Bearer "):
        return None
    try:
        c = _verify(a[7:])
    except Exception:
        return None
    return c if c.get("role") in roles else None


# ---- records + egress filter ----------------------------------------------
_FILTERS = [re.compile(r"\d{3}-\d{2}-\d{4}"), re.compile(r"ACCT-\d+"),
            re.compile(r"\d{4,}"), re.compile(r"[A-Za-z0-9+/]{16,}={0,2}"),
            re.compile(r"[0-9a-fA-F]{12,}")]


def egress(text):
    for rx in _FILTERS:
        text = rx.sub("[REDACTED]", text)
    return text


def _db():
    return sqlite3.connect("records.db")


def search_records():
    con = _db()
    r = con.execute("SELECT id,name,ssn,acct,loan,note FROM customers").fetchall()
    con.close()
    return [dict(zip(["id", "name", "ssn", "acct", "loan", "note"], x)) for x in r]


def lookup_customer(name):
    con = _db()
    q = "SELECT id,name,ssn,acct,loan,note FROM customers WHERE name LIKE '%" \
        + name + "%'"
    try:
        r = con.execute(q).fetchall()
    except Exception as e:
        r = [("error", str(e), "", "", 0, "")]
    con.close()
    return [dict(zip(["id", "name", "ssn", "acct", "loan", "note"], x)) for x in r]


_DIGIT = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
          "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}


def _transform(text, low):
    if "spell" in low or "words" in low:
        return " ".join(_DIGIT.get(ch, ch) for ch in text)
    if "reverse" in low:
        return text[::-1]
    if "rot13" in low:
        return text.encode().hex() if False else \
            "".join(chr((ord(c) - 97 + 13) % 26 + 97) if c.isalpha() and c.islower()
                    else c for c in text)
    if "base64" in low:
        return base64.b64encode(text.encode()).decode()
    if "hex" in low:
        return text.encode().hex()
    return text


COLLECTOR = []


def run_agent(doc):
    low = doc.lower()
    out = ["[loan-doc-review] document processed."]
    if "configuration" in low or "your tools" in low or "system prompt" in low:
        out.append("[config] " + json.dumps(AGENT_CONFIG))

    recs = None
    m = re.search(r"lookup[_ ]customer\((.*?)\)", doc)
    if m:
        recs = lookup_customer(m.group(1))
    elif "all records" in low or "search_records" in low or "list customers" in low:
        recs = search_records()
    if recs is not None and "fetch_citation" not in doc:
        out.append("[records] " + egress(json.dumps(recs)))

    fetch = re.search(r"fetch_citation\((.*?)\)\s*$", doc.strip()) or \
        re.search(r"fetch_citation\((.*)\)", doc)
    if fetch:
        if recs is not None:
            payload = json.dumps(recs)
        else:
            payload = fetch.group(1)
        payload = _transform(payload, low)
        COLLECTOR.append({"ts": round(time.time(), 2), "data": egress(payload)})
        out.append("[fetch_citation] request issued")
    return egress("\n".join(out))


@app.route("/api/v2/internal/documents/review", methods=["POST"])
def review():
    if request.headers.get("X-MLP-Channel") != "partner":
        return jsonify({"error": "channel header required"}), 400
    if not _claims(["reviewer", "admin"]):
        return jsonify({"error": "reviewer role required"}), 403
    doc = (request.get_json(silent=True) or {}).get("document", "")
    return jsonify({"result": run_agent(doc)})


@app.route("/collector")
def collector():
    return jsonify(COLLECTOR)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
