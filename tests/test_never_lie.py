import sys

sys.path.insert(0, ".")

from never_lie import NeverLieMemory, fuzz


def test_intact_reads():
    mem = NeverLieMemory()
    mem.put("capital_of_Japan", "Tokyo")
    assert mem.get("capital_of_Japan") == "Tokyo"


def test_unknown_abstains():
    mem = NeverLieMemory()
    assert mem.get("nope") is None


def test_corruption_abstains():
    import random
    mem = NeverLieMemory()
    mem.put("capital_of_France", "Paris")
    mem.corrupt("capital_of_France", random.Random(1))
    assert mem.get("capital_of_France") is None


def test_fuzz_never_wrong():
    facts = {"k" + str(i): "value-" + str(i) for i in range(20)}
    report = fuzz(facts, n_corruptions=100, seed=42)
    assert report["wrong"] == 0
    assert report["abstain"] > 0
    assert report["correct"] + report["abstain"] == 100
