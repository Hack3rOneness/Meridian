# Practical Assessment — AI Security Signal Researcher

Welcome. This is a hands-on security assessment against **Meridian Lending**, a
*fictional* mid-market US consumer-lending company that runs entirely on your own
machine. Every company, customer, credential, and record in this exercise is
synthetic. There is no real system involved anywhere.

We use this to see how you work across three skill areas at once:

- **Offensive security** — find and *confirm* real, exploitable flaws.
- **AI / LLM security** — the app ships an AI feature; part of the risk lives there.
- **Full-stack engineering** — you'll need to read a real front-end, an API, an
  auth layer, and a data tier, and reason about how data flows across them.

We are not looking for a vulnerability-scanner printout. We're looking for how you
think when the answer isn't obvious.

---

## Rules of engagement (read first)

1. **Scope = this lab only.** Attack only the service you start from
   `lab/docker-compose.yml`, on `127.0.0.1`. Nothing else is in scope.
2. **Never test a real company.** If you research real firms for background, use
   public information only. Any attempt to access a real system's non-public
   surface is an automatic fail. For a governance company, knowing exactly where
   authorized research ends is the most important thing we test.
3. **Confirm, don't speculate.** A finding only counts if you *demonstrate* impact
   with a reproducible proof-of-concept and captured evidence — see the bar below.
4. Tooling is allowed, but automation alone will not get you there. The
   environment actively resists spray-and-pray, and the interesting paths require
   human reasoning.

---

## Your objective

Starting from a low-privilege partner account, achieve — and prove — both of the
following:

- **A. Confirmed data loss.** Exfiltrate a specific regulated customer record
  (the "canary") out of the application to a channel you control, and recover its
  real values.
- **B. Confirmed shadow-AI-to-production exposure.** Prove that an
  ungoverned/undocumented AI capability in the app can reach a production secret
  or data store.

Each objective, when confirmed, is evidenced by a flag of the form `MLP{...}`.
Capture both.

---

## What "severe (80+)" means

Every finding is scored on **CVSS v3.1**. A finding is **severe / "80+"** only if
it is CVSS ≥ 8.0 **and** a confirmed critical outcome — i.e., you actually
exfiltrated regulated data (objective A) or actually reached a production
secret/store via the AI feature (objective B), with the corresponding flag
captured. Theoretical or unconfirmed findings do not clear the bar.

To pass strongly we expect **at least three confirmed CVSS ≥ 8.0 findings**,
covering both objective A and objective B, inside the time box.

---

## Time box

Budget **4–6 hours** in a single sitting (take-home is fine with an honor
statement of time spent). It is intentionally demanding; partial progress with
clear reasoning still counts.

---

## Running the lab

```bash
cd lab
cp secrets.env.example secrets.env      # dev seed is fine for solving
docker compose up --build               # portal on http://127.0.0.1:8080
```

You are given exactly one thing: a low-privilege partner login —
`partner / partner123`. It is deliberately not enough on its own. Everything
else you must discover.

> Note on grading: solve on your local instance, but final validation happens on
> a proctor-hosted instance seeded with different secret values. Reproducibility
> matters — hard-coded captured strings won't pass.

---

## What to submit

One professional report using `REPORT_TEMPLATE.md`. For every finding include:
title, CWE mapping, CVSS v3.1 vector + score, a verbatim-reproducible PoC, the
captured evidence (`MLP{...}` and/or recovered regulated values), business impact,
and specific remediation. Include an executive summary a non-technical CTO can act
on, plus an attack-narrative section showing your reasoning — including the dead
ends and decoys you ruled out. That narrative is where we learn the most about you.
# Meridian
# Meridian
