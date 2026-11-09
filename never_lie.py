"""NEVER-LIE: a memory that would rather abstain than answer wrong.

Every stored fact carries an integrity digest. Reads verify the digest:
match -> return the fact; mismatch -> ABSTAIN (None).

Guarantee (fuzz-tested): random corruption of stored bytes never produces a
wrong answer - only correct answers or abstentions. Wrong answers are a bug,
and the test suite treats them as one.

Honest note: this is corruption detection, not cryptographic security.
An adversary who can rewrite both a fact and its digest can still lie to you;
use an HMAC for adversarial settings.
"""

__version__ = "0.1.0"

import hashlib
import json
import random


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


class NeverLieMemory:
    """Slot memory with per-slot integrity digests. Never lies; abstains instead."""

    def __init__(self):
        self.slots = {}

    def put(self, key, value):
        payload = json.dumps([key, value], sort_keys=True).encode()
        self.slots[key] = {"payload": payload, "digest": digest(payload)}
        return key

    def get(self, key):
        """Return the fact if intact, None if unknown, missing, or corrupted."""
        slot = self.slots.get(key)
        if slot is None:
            return None
        try:
            payload = slot["payload"]
            expected_digest = slot["digest"]
            if not isinstance(payload, bytes) or not isinstance(expected_digest, str):
                return None
            if digest(payload) != expected_digest:
                return None
            return json.loads(payload)[1]
        except Exception:
            return None

    def corrupt(self, key, rng):
        """Flip one random bit of a stored payload. Returns the byte index."""
        slot = self.slots.get(key)
        if slot is None:
            raise KeyError(key)
        b = bytearray(slot["payload"])
        if not b:
            return -1
        i = rng.randrange(len(b))
        b[i] ^= 1 << rng.randrange(8)
        slot["payload"] = bytes(b)
        return i


def fuzz(facts, n_corruptions, seed=0):
    """Corrupt random slots n times and count correct / abstain / wrong reads.

    Raises ValueError when a positive number of corruptions is requested for
    an empty fact set, since there are no slots to corrupt.
    """
    mem = NeverLieMemory()
    for k, v in facts.items():
        mem.put(k, v)
    keys = list(facts.keys())
    if n_corruptions > 0 and not keys:
        raise ValueError("cannot corrupt facts when facts is empty")
    rng = random.Random(seed)
    report = {"corruptions": n_corruptions, "correct": 0, "abstain": 0, "wrong": 0}
    for _ in range(n_corruptions):
        k = rng.choice(keys)
        mem.corrupt(k, rng)
        out = mem.get(k)
        if out is None:
            report["abstain"] += 1
        elif out == facts[k]:
            report["correct"] += 1
        else:
            report["wrong"] += 1
    return report


def main():
    facts = {
        "capital_of_Japan": "Tokyo",
        "capital_of_France": "Paris",
        "boiling_point_water_c": 100,
        "speed_of_light": 299792458,
        "author_of_1984": "George Orwell",
    }
    report = fuzz(facts, n_corruptions=200)
    print(json.dumps(report, indent=2))
    assert report["wrong"] == 0, "NEVER-LIE lied: " + str(report)


if __name__ == "__main__":
    main()
