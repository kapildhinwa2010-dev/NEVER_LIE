# 🛡️ NEVER-LIE

[![CI](https://github.com/kapildhinwa2010-dev/NEVER_LIE/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/NEVER_LIE/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/NEVER_LIE/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/NEVER_LIE/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 A memory that would rather abstain than answer wrong

Most memory systems optimize for accuracy. NEVER-LIE optimizes for a **guarantee**:

> 🚫 **Zero wrong answers.** Under random corruption, every read is either
> exactly correct, or an explicit abstention. Never a confident lie.

## 🔍 How it works

- 📥 Every stored fact carries a SHA-256 integrity digest
- 📤 Reads verify the digest: match → fact, mismatch → abstain (None)
- 🧪 A fuzzer corrupts random bits; the property test asserts wrong == 0

## 🤔 Why this matters

"Honest uncertainty" is the rarest property in AI. A system that says
"I don't know" under damage is safer than one that says something wrong
with full confidence - and this is a **testable property**, not a vibe.

## 💻 Usage

    python never_lie.py

Library:

    from never_lie import NeverLieMemory, fuzz

    mem = NeverLieMemory()
    mem.put("capital_of_Japan", "Tokyo")
    print(mem.get("capital_of_Japan"))

    report = fuzz({"k": "v"}, n_corruptions=100)

## 🧪 Tests

    pytest -q

<details>
<summary>🔬 Honest limitations</summary>

- This is **corruption detection**, not cryptographic security: an adversary
  who can rewrite both a fact and its digest can still lie. Use an HMAC in
  adversarial settings.
- Abstention is not recovery: the fact is lost, not repaired (parity-based
  repair is future work).

</details>

## ⚖️ License

MIT - see [LICENSE](LICENSE).
