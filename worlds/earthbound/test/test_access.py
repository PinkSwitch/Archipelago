from . import EarthBoundTestBase


class TestPSIShuffle(EarthBoundTestBase):
    options = {
        "PSIShuffle": 1
    }


class TestExtendedPSIShuffle(EarthBoundTestBase):
    options = {
        "PSIShuffle": 2
    }


class TestBossShuffle(EarthBoundTestBase):
    options = {
        "BossShuffle": 1
    }


class TestBossShuffleWithDD(EarthBoundTestBase):
    options = {
        "BossShuffle": 1,
        "DecoupleDiamondDog": 1
    }


class TestBossShuffleGiygas(EarthBoundTestBase):
    options = {
        "BossShuffle": 1,
        "ShuffleGiygas": 1
    }


class TestBossShuffleFull(EarthBoundTestBase):
    options = {
        "BossShuffle": 1,
        "ShuffleGiygas": 1,
        "DecoupleDiamondDog": 1
    }
