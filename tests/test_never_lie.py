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


def test_malformed_slot_abstains():
    mem = NeverLieMemory()
    mem.put("key", "value")
    del mem.slots["key"]["digest"]
    assert mem.get("key") is None

    mem.put("key", "value")
    mem.slots["key"]["payload"] = "not bytes"
    assert mem.get("key") is None


def test_fuzz_never_wrong():
    facts = {"k" + str(i): "value-" + str(i) for i in range(20)}
    report = fuzz(facts, n_corruptions=100, seed=42)
    assert report["wrong"] == 0
    assert report["abstain"] > 0
    assert report["correct"] + report["abstain"] == 100


def test_fuzz_empty_facts_contract():
    assert fuzz({}, n_corruptions=0) == {
        "corruptions": 0,
        "correct": 0,
        "abstain": 0,
        "wrong": 0,
    }
    try:
        fuzz({}, n_corruptions=1)
    except ValueError as error:
        assert str(error) == "cannot corrupt facts when facts is empty"
    else:
        raise AssertionError("positive corruptions on empty facts must fail")
