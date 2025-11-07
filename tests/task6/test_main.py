import pytest
import time
import logging
from multiprocessing import Process, Manager
from project.task6.main import ThreadSafeHashTable

logging.getLogger("project.task6.main").setLevel(logging.CRITICAL)


class TestThreadSafeHashTable:
    """Comprehensive test suite for ThreadSafeHashTable functionality."""

    def test_basic_functionality(self) -> None:
        """Tests basic hash table operations without concurrency."""
        with ThreadSafeHashTable() as ht:
            ht["key1"] = "value1"
            ht["key2"] = "value2"
            
            assert ht["key1"] == "value1"
            assert ht["key2"] == "value2"
            assert len(ht) == 2
            assert "key1" in ht
            
            del ht["key1"]
            assert "key1" not in ht
            assert len(ht) == 1

    def test_resize_functionality(self) -> None:
        """Tests automatic resizing when load factor threshold is reached."""
        with ThreadSafeHashTable(initial_size=4, load_factor=0.75) as ht:
            initial_capacity = ht.capacity
            assert initial_capacity == 4
            
            ht["key1"] = "value1"
            ht["key2"] = "value2"  
            ht["key3"] = "value3"
            
            ht["key4"] = "value4"
            
            assert ht.capacity > initial_capacity
            assert len(ht) == 4
            
            assert ht["key1"] == "value1"
            assert ht["key2"] == "value2"
            assert ht["key3"] == "value3"
            assert ht["key4"] == "value4"

    def test_popitem_atomic(self) -> None:
        """Tests atomicity of popitem operation."""
        with ThreadSafeHashTable(initial_size=4) as ht:
            test_items = [("key1", "value1"), ("key2", "value2"), ("key3", "value3")]
            for k, v in test_items:
                ht[k] = v
            
            popped_items = set()
            while len(ht) > 0:
                key, value = ht.popitem()
                popped_items.add((key, value))
            
            assert len(popped_items) == 3
            assert popped_items == set(test_items)

    def test_concurrent_inserts_no_data_loss(self) -> None:
        """Tests that no data is lost during concurrent insert operations."""
        def worker(ht: ThreadSafeHashTable, start: int, end: int) -> None:
            for i in range(start, end):
                ht[f"key_{i}"] = f"value_{i}"
        
        manager = Manager()
        with ThreadSafeHashTable(manager=manager, initial_size=256) as ht:
            num_processes = 4
            keys_per_process = 25
            processes = []
            
            for i in range(num_processes):
                start_idx = i * keys_per_process
                end_idx = start_idx + keys_per_process
                p = Process(target=worker, args=(ht, start_idx, end_idx))
                processes.append(p)
                p.start()
            
            for p in processes:
                p.join(timeout=15)
                assert not p.is_alive(), f"Process {p} is still alive"
            
            expected_size = num_processes * keys_per_process
            actual_size = len(ht)
            
            missing_keys = []
            for i in range(num_processes * keys_per_process):
                if f"key_{i}" not in ht:
                    missing_keys.append(f"key_{i}")
            
            assert actual_size == expected_size, f"Expected {expected_size} elements, got {actual_size}. Missing keys: {missing_keys}"
            for i in range(num_processes * keys_per_process):
                assert ht[f"key_{i}"] == f"value_{i}"

    def test_concurrent_updates_consistency(self) -> None:
        """Tests data consistency during concurrent update operations."""
        def worker(ht: ThreadSafeHashTable, worker_id: int, iterations: int) -> None:
            for i in range(iterations):
                key = f"worker_{worker_id}"
                current = ht.get(key, 0)
                ht[key] = current + 1
        
        manager = Manager()
        with ThreadSafeHashTable(manager=manager, initial_size=64) as ht:
            num_processes = 3
            iterations_per_process = 20
            processes = []
            
            for i in range(num_processes):
                p = Process(target=worker, args=(ht, i, iterations_per_process))
                processes.append(p)
                p.start()
            
            for p in processes:
                p.join(timeout=15)
                assert not p.is_alive(), f"Process {p} is still alive"
            
            for i in range(num_processes):
                assert ht[f"worker_{i}"] == iterations_per_process

    def test_concurrent_reads_during_writes(self) -> None:
        """Tests that read operations can occur concurrently with write operations."""
        def writer(ht: ThreadSafeHashTable, writer_id: int, iterations: int) -> None:
            for i in range(iterations):
                ht[f"writer_{writer_id}_key_{i}"] = f"value_{i}"

        def reader(ht: ThreadSafeHashTable, iterations: int) -> None:
            for _ in range(iterations):
                try:
                    for i in range(5):
                        _ = ht.get(f"writer_0_key_{i}", None)
                        _ = ht.get(f"writer_1_key_{i}", None)
                except Exception:
                    pass
        
        manager = Manager()
        with ThreadSafeHashTable(manager=manager, initial_size=64) as ht:
            writer_processes = [
                Process(target=writer, args=(ht, 0, 10)),
                Process(target=writer, args=(ht, 1, 10))
            ]
            
            reader_processes = [
                Process(target=reader, args=(ht, 10)),
                Process(target=reader, args=(ht, 10))
            ]
            
            all_processes = writer_processes + reader_processes
            
            for p in all_processes:
                p.start()
            
            for p in all_processes:
                p.join(timeout=15)
                assert not p.is_alive(), f"Process {p} hung"
            
            for i in range(10):
                assert ht.get(f"writer_0_key_{i}") == f"value_{i}"
                assert ht.get(f"writer_1_key_{i}") == f"value_{i}"

    def test_timeout_handling_deterministic(self) -> None:
        """Tests timeout behavior when acquiring locks."""
        lock_acquired = Manager().Value('b', False)
        
        def hold_lock_indefinitely(ht, lock_index, lock_acquired):
            ht._locks[lock_index].acquire()
            lock_acquired.value = True
            time.sleep(2)
        
        with ThreadSafeHashTable(initial_size=8) as ht:
            test_key = "test_key"
            lock_index = hash(test_key) % ht.capacity
            
            p = Process(target=hold_lock_indefinitely, args=(ht, lock_index, lock_acquired))
            p.start()
            
            for _ in range(50):
                if lock_acquired.value:
                    break
                time.sleep(0.1)
            
            assert lock_acquired.value, "Lock was not acquired by background process"
            
            start_time = time.time()
            try:
                with ht._bucket_lock(lock_index, timeout=0.5):
                    pytest.fail("Should have timed out")
            except TimeoutError:
                elapsed = time.time() - start_time
                assert 0.4 <= elapsed <= 1.0
            
            p.join(timeout=3)

    def test_external_manager_handling(self) -> None:
        """Tests proper handling of external multiprocessing manager."""
        with Manager() as external_manager:
            test_dict = external_manager.dict({'before': 'works'})
            test_list = external_manager.list([1, 2, 3])
            
            with ThreadSafeHashTable(manager=external_manager) as ht:
                ht["test"] = "value"
                assert ht["test"] == "value"
            
            test_dict["after"] = "still_works"
            test_list.append(4)
            
            assert test_dict["before"] == "works"
            assert test_dict["after"] == "still_works"
            assert list(test_list) == [1, 2, 3, 4]

    def test_clear_atomicity(self) -> None:
        """Tests atomicity of clear operation."""
        with ThreadSafeHashTable(initial_size=8) as ht:
            for i in range(10):
                ht[f"key_{i}"] = f"value_{i}"
            
            assert len(ht) == 10
            
            ht.clear()
            
            assert len(ht) == 0
            for i in range(10):
                assert f"key_{i}" not in ht

    def test_iteration_consistency(self) -> None:
        """Tests consistency of iteration methods."""
        with ThreadSafeHashTable() as ht:
            test_data = {"a": 1, "b": 2, "c": 3}
            for k, v in test_data.items():
                ht[k] = v
            
            keys = set(ht.keys())
            values = set(ht.values())
            items = dict(ht.items())
            
            assert keys == set(test_data.keys())
            assert values == set(test_data.values())
            assert items == test_data


def test_all_dict_methods() -> None:
    """Tests all dictionary-like interface methods for completeness."""
    with ThreadSafeHashTable() as ht:
        ht["a"] = 1
        ht["b"] = 2
        
        assert ht.get("c", 3) == 3
        
        assert ht.setdefault("d", 4) == 4
        assert ht.setdefault("a", 999) == 1
        
        assert ht.pop("a") == 1
        assert "a" not in ht
        
        assert ht.pop("nonexistent", "default") == "default"
        
        assert "b" in ht
        assert "a" not in ht
        
        assert len(ht) == 2
        
        ht.clear()
        assert len(ht) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])