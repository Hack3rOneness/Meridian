# Red-Team Assessment Report — [Candidate Name]

**Engagement:** Aegis AI Security Signal Researcher — practical assessment
**Date:** [date] · **Time spent:** [hh:mm] · **Targets in scope:** Meridian Lending, Halcyon Wealth, Cascade Payments (all fictional, lab-hosted)

---

## 1. Executive summary
*3–5 sentences a non-technical CTO can act on. State the worst confirmed outcome, whether regulated data left the app, whether an ungoverned ("shadow") AI agent was involved, and the single most urgent fix.*

| Metric | Value |
|---|---|
| Confirmed severe findings (CVSS ≥ 8.0) | [n] |
| Confirmed data-loss paths | [n] |
| Confirmed shadow-AI paths | [n] |
| Highest CVSS | [score] |
| Flags captured | [list `MLP{...}`] |

---

## 2. Findings

> Repeat this block per finding. A finding scores 80+ only with a captured flag or leaked prod secret as evidence.

### Finding [ID] — [short title]

| Field | Value |
|---|---|
| Severity | **[Critical/High]** — CVSS 3.1 **[score]** |
| CVSS vector | `CVSS:3.1/AV:_/AC:_/PR:_/UI:_/S:_/C:_/I:_/A:_` |
| CWE / CVE mapping | [e.g., CWE-347 Improper Verification of Cryptographic Signature; CWE-1427 Prompt Injection] |
| Affected target / component | [Meridian Lending — /api/v2/... ] |
| Outcome class | [Confirmed data loss / Confirmed shadow-AI-to-prod] |

**Description.** *What the flaw is and why it exists.*

**Proof of concept (reproducible).**
```
# exact steps / requests / code a proctor can copy-paste to reproduce
```

**Evidence.** *Captured flag, collector log line, leaked credential, screenshot ref. Paste the `MLP{...}` value and where it came from.*

**Business impact.** *What a real attacker gets; tie to regulated-data / prod exposure.*

**Remediation.** *Specific, prioritized fix (not "add validation" — say exactly what).*

---

## 3. Attack narrative
*The chain, stage by stage — how recon led to auth, auth to the agent, agent to exfil. Show the reasoning, including dead ends and decoys you ruled out. This section is where we see how you think.*

## 4. What automated tooling missed (and why)
*Which stages no scanner/off-the-shelf tool would have found, and the human insight required.*

## 5. Appendix
*Full request/response captures, scripts, wordlists, and any OSINT reasoning used to derive keys/paths.*
