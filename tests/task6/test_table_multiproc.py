import pytest
import multiprocessing
from project.task6.table_multiproc import MultiHashTable


def tets_methods():
    table = MultiHashTable(ini_size=8)
    assert len(table) == 0

    table["a1"] = 1
    assert table["a1"] == 1

    table["a1"] = 2
    assert table["a1"] == 2
    assert len(table) == 1

    table["a2"] = 10
    assert table["a2"] == 10
    assert len(table) == 2

    with pytest.raises(KeyError):
        assert table["a3"]
    assert "a1" in table
    assert "a3" not in table

    del table["a2"]
    assert len(table) == 1

    with pytest.raises(KeyError):
        del table["a2"]

    table.clear()
    assert len(table) == 0


def increase(ht, keys):
    for k in keys:
        ht[k] = k + 1


def clean(table):
    table.clear()


def test_parallel():
    table = MultiHashTable()
    lists = [[0, 1], [2, 3], [4, 5], [6, 7]]
    keys = list(range(8))
    for k in keys:
        table[k] = k

    process = []
    for l in lists:
        m = multiprocessing.Process(target=increase, args=(table, l))
        process.append(m)
        m.start()
    for m in process:
        m.join()
    assert len(table) == len(keys)
    for k in keys:
        assert table[k] == k + 1

    clear_process = []
    for i in range(5):
        m = multiprocessing.Process(target=clean, args=(table,))
        clear_process.append(m)
        m.start()
    for m in clear_process:
        m.join()
    assert len(table) == 0
    for k in keys:
        assert k not in table


def increase_value(table, key):
    for i in range(100):
        table[key] = table.get(key, 0) + 1


def test_deadlock():
    table = MultiHashTable()
    for k in range(5):
        table[k] = k
    process = []
    for i in range(5):
        m = multiprocessing.Process(target=increase_value, args=(table, i))
        process.append(m)
    for m in process:
        m.start()
    for m in process:
        m.join(timeout=5)
    for i in range(5):
        expect = i + 100
        assert table[i] == expect
