# -*- coding: utf-8 -*-

import boost_histogram as bh


def test_weighted_sum():
    a = bh.accumulators.WeightedSum(1.5, 2.5)

    assert repr(a) == "WeightedSum(value=1.5, variance=2.5)"

    assert a == bh.accumulators.WeightedSum(1.5, 2.5)

    assert a.value == 1.5
    assert a.variance == 2.5

    a += 1.5

    assert a.value == 3.0
    assert a.variance == 4.75

    vals = [1, 2, 3]
    vari = [4, 5, 6]

    a = bh.accumulators.WeightedSum()
    for val, var in zip(vals, vari):
        a += bh.accumulators.WeightedSum(val, variance=var)

    assert a.value == 6
    assert a.variance == 15

    a2 = bh.accumulators.WeightedSum().fill(vals, variance=vari)
    assert a == a2

    assert a == bh.accumulators.WeightedSum(6, 15)


def test_sum():
    vals = [1, 2, 3]
    a = bh.accumulators.Sum()
    for val in vals:
        a += val

    assert a.value == 6

    a2 = bh.accumulators.Sum().fill(vals)
    assert a == a2

    assert a == bh.accumulators.Sum(6)

    assert repr(a) == "Sum(6 + 0)"


def test_weighted_mean():
    vals = [4, 1]
    weights = [1, 2]
    a = bh.accumulators.WeightedMean()
    for v, w in zip(vals, weights):
        a(v, weight=w)

    assert a.sum_of_weights == 3.0
    assert a.variance == 4.5
    assert a.value == 2.0

    a2 = bh.accumulators.WeightedMean().fill(vals, weight=weights)
    assert a == a2

    assert a == bh.accumulators.WeightedMean(3, 5, 2, 4.5)
    assert (
        repr(a)
        == "WeightedMean(sum_of_weights=3, sum_of_weights_squared=5, value=2, variance=4.5)"
    )


def test_mean():
    vals = [1, 2, 3]
    a = bh.accumulators.Mean()
    for val in vals:
        a(val)

    assert a.count == 3
    assert a.value == 2
    assert a.variance == 1

    a2 = bh.accumulators.Mean().fill([1, 2, 3])
    assert a == a2

    assert a == bh.accumulators.Mean(3, 2, 1)

    assert repr(a) == "Mean(count=3, value=2, variance=1)"


def test_weight_collector():
    ws = [1, 2, 3]
    a = bh.accumulators.WeightCollector()
    for w in ws:
        a += w

    assert len(a) == 3
    assert list(a) == [1, 2, 3]
    assert a.view().sum() == 6
    assert a[0] == 1
    a[0] = 9
    a.view()[1:] *= 2

    assert repr(a) == "WeightCollector([9, 4, 6])"

    ws = [4, 5, 6, 7, 8, 9, 10, 11]
    a.fill(ws)

    assert len(a) == 11
    assert repr(a) == "WeightCollector([9, 4, 6, 4, 5, 6, 7, 8, 9, 10, 11])"

    a2 = bh.accumulators.WeightCollector().fill(range(1001))
    assert repr(a2) == "WeightCollector([0, 1, 2, 3, 4, ..., 996, 997, 998, 999, 1000])"
