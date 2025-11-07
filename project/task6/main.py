from typing import Any, Iterator, List, Tuple, Dict, Optional
from collections.abc import MutableMapping
from multiprocessing.managers import SyncManager
import random
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class ThreadSafeHashTable(MutableMapping):
    """
    Thread-safe hash table implementation for multiprocessing environments.
    """

    def __init__(self, initial_size: int = 32, load_factor: float = 0.75, manager: Optional[SyncManager] = None) -> None:
        """
        Initializes a thread-safe hash table.

        Parameters:
            initial_size : int (Initial number of buckets in the hash table)
            load_factor : float (Threshold for triggering resizing operation)
            manager : Optional[SyncManager] (External multiprocessing manager instance)

        Raises:
            ValueError: If initial_size is less than 1 or load_factor is not in range (0.1, 1]
        """
        if initial_size < 1:
            raise ValueError("Initial size must be at least 1")
        if not 0.1 < load_factor <= 1:
            raise ValueError("Load factor must be between 0.1 and 1")
        
        self._external_manager = manager is not None
        self._manager: SyncManager
        
        if manager is not None:
            self._manager = manager
        else:
            self._manager = SyncManager()
            self._manager.start()
        
        self._capacity_var = self._manager.Value('i', initial_size)
        self._size_var = self._manager.Value('i', 0)
        self._load_factor = load_factor
        
        self._size_lock = self._manager.Lock()
        
        self._buckets: List[Any] = [self._manager.dict() for _ in range(initial_size)]
        self._locks: List[Any] = [self._manager.Lock() for _ in range(initial_size)]
        
        logger.debug(f"Initialized ThreadSafeHashTable with capacity {initial_size}, load_factor {load_factor}")
    
    def __enter__(self) -> 'ThreadSafeHashTable':
        """
        Enters the context manager.

        Returns:
            ThreadSafeHashTable: The hash table instance for context management.
        """
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exits the context manager and cleans up resources.

        Parameters:
            exc_type : Any (Exception type if an exception occurred)
            exc_val : Any (Exception value if an exception occurred)
            exc_tb : Any (Exception traceback if an exception occurred)
        """
        self.close()
    
    def close(self) -> None:
        """
        Closes the internal manager if it was created by this instance.
        """
        if hasattr(self, '_manager') and not self._external_manager:
            self._manager.shutdown()
            logger.debug("Internal manager shut down")
    
    def _hash(self, key: Any) -> int:
        """
        Computes the bucket index for a given key.

        Parameters:
            key : Any (Key to hash)

        Returns:
            int: Bucket index in the range [0, capacity-1]
        """
        return hash(key) % self.capacity
    
    @contextmanager
    def _bucket_lock(self, index: int, timeout: float = 5.0) -> Iterator[None]:
        """
        Context manager for safe bucket lock acquisition with timeout.

        Parameters:
            index : int (Bucket index to lock)
            timeout : float (Maximum time to wait for lock acquisition)

        Raises:
            TimeoutError: If lock cannot be acquired within timeout
        """
        acquired = False
        try:
            acquired = self._locks[index].acquire(timeout=timeout)
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for bucket {index} within {timeout}s")
            yield
        except Exception as e:
            logger.error(f"Error acquiring lock for bucket {index}: {e}")
            raise
        finally:
            if acquired:
                self._locks[index].release()
    
    def _safe_acquire_all_locks(self, timeout: float = 10.0) -> List[int]:
        """
        Safely acquires all bucket locks with guaranteed release on failure.

        Parameters:
            timeout : float (Maximum time to wait for each lock)

        Returns:
            List[int]: List of successfully acquired lock indices

        Raises:
            TimeoutError: If any lock cannot be acquired within timeout
        """
        acquired: List[int] = []
        current_capacity = self.capacity
        
        try:
            for i in range(current_capacity):
                if self._locks[i].acquire(timeout=timeout):
                    acquired.append(i)
                else:
                    raise TimeoutError(f"Could not acquire lock for bucket {i}")
            return acquired
        except Exception:
            for idx in acquired:
                try:
                    self._locks[idx].release()
                except Exception as e:
                    logger.warning(f"Error releasing lock {idx}: {e}")
            raise
    
    def _should_resize(self) -> bool:
        """
        Checks if the hash table needs resizing based on load factor.

        Returns:
            bool: True if resizing is needed, False otherwise
        """
        with self._size_lock:
            current_size = self._size_var.value  # type: ignore
            max_size = int(self.capacity * self._load_factor)
            return current_size >= max_size
    
    def _resize_if_needed(self) -> None:
        """
        Performs resizing operation if the load factor threshold is exceeded.
        """
        if not self._should_resize():
            return
            
        logger.info(f"Starting resize from capacity {self.capacity}")
        
        acquired_locks = self._safe_acquire_all_locks()
        
        try:
            if not self._should_resize():
                return
            
            old_capacity = self.capacity
            new_capacity = old_capacity * 2
            
            new_buckets: List[Any] = [self._manager.dict() for _ in range(new_capacity)]
            new_locks: List[Any] = [self._manager.Lock() for _ in range(new_capacity)]
            
            total_moved = 0
            for old_bucket in self._buckets:
                bucket_dict = dict(old_bucket.items())
                for key, value in bucket_dict.items():
                    new_index = hash(key) % new_capacity
                    new_buckets[new_index][key] = value
                    total_moved += 1
            
            self._buckets = new_buckets
            self._locks = new_locks
            self._capacity_var.value = new_capacity  # type: ignore
            
            logger.info(f"Resize completed: {total_moved} elements moved to new capacity {new_capacity}")
            
        finally:
            for idx in acquired_locks:
                try:
                    self._locks[idx].release()
                except Exception as e:
                    logger.warning(f"Error releasing lock during resize: {e}")

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Sets the value for the specified key.

        Parameters:
            key : Any (Key to set)
            value : Any (Value to associate with the key)

        Note:
            Automatically triggers resizing if load factor is exceeded.
        """
        index = self._hash(key)
        
        with self._bucket_lock(index):
            bucket = self._buckets[index]
            key_existed = key in bucket
            bucket[key] = value
            
            if not key_existed:
                with self._size_lock:
                    self._size_var.value += 1  # type: ignore
        
        self._resize_if_needed()
    
    def __getitem__(self, key: Any) -> Any:
        """
        Retrieves the value for the specified key.

        Parameters:
            key : Any (Key to look up)

        Returns:
            Any: Value associated with the key

        Raises:
            KeyError: If the key is not found in the hash table
        """
        index = self._hash(key)
        
        with self._bucket_lock(index):
            bucket = self._buckets[index]
            if key in bucket:
                return bucket[key]
            raise KeyError(f"Key {key!r} not found")
    
    def __delitem__(self, key: Any) -> None:
        """
        Deletes the key-value pair for the specified key.

        Parameters:
            key : Any (Key to delete)

        Raises:
            KeyError: If the key is not found in the hash table
        """
        index = self._hash(key)
        
        with self._bucket_lock(index):
            bucket = self._buckets[index]
            if key in bucket:
                del bucket[key]
                with self._size_lock:
                    self._size_var.value -= 1  # type: ignore
            else:
                raise KeyError(f"Key {key!r} not found")
    
    def __contains__(self, key: Any) -> bool:
        """
        Checks if the specified key exists in the hash table.

        Parameters:
            key : Any (Key to check)

        Returns:
            bool: True if key exists, False otherwise
        """
        index = self._hash(key)
        
        with self._bucket_lock(index):
            return key in self._buckets[index]
    
    def __len__(self) -> int:
        """
        Returns the number of key-value pairs in the hash table.

        Returns:
            int: Current size of the hash table
        """
        with self._size_lock:
            return self._size_var.value  # type: ignore
    
    def _create_snapshot(self) -> Dict[Any, Any]:
        """
        Creates a consistent snapshot of the entire hash table.

        Returns:
            Dict[Any, Any]: Dictionary containing all key-value pairs
        """
        acquired_locks = self._safe_acquire_all_locks(timeout=5.0)
        try:
            snapshot: Dict[Any, Any] = {}
            current_capacity = self.capacity
            for i in range(current_capacity):
                bucket = self._buckets[i]
                snapshot.update(dict(bucket.items()))
            return snapshot
        finally:
            for idx in acquired_locks:
                try:
                    self._locks[idx].release()
                except Exception as e:
                    logger.warning(f"Error releasing lock during snapshot: {e}")
    
    def __iter__(self) -> Iterator[Any]:
        """
        Returns an iterator over all keys in the hash table.

        Returns:
            Iterator[Any]: Iterator yielding all keys
        """
        snapshot = self._create_snapshot()
        return iter(snapshot.keys())
    
    def keys(self) -> Iterator[Any]:  # type: ignore[override]
        """
        Returns an iterator over all keys in the hash table.

        Returns:
            Iterator[Any]: Iterator yielding all keys
        """
        return iter(self)
    
    def values(self) -> Iterator[Any]:  # type: ignore[override]
        """
        Returns an iterator over all values in the hash table.

        Returns:
            Iterator[Any]: Iterator yielding all values
        """
        snapshot = self._create_snapshot()
        return iter(snapshot.values())

    def items(self) -> Iterator[Tuple[Any, Any]]:  # type: ignore[override]
        """
        Returns an iterator over all key-value pairs in the hash table.

        Returns:
            Iterator[Tuple[Any, Any]]: Iterator yielding (key, value) pairs
        """
        snapshot = self._create_snapshot()
        return iter(snapshot.items())
    
    def get(self, key: Any, default: Any = None) -> Any:
        """
        Retrieves the value for the specified key or returns default if not found.

        Parameters:
            key : Any (Key to look up)
            default : Any (Default value to return if key not found)

        Returns:
            Any: Value associated with key or default if key not found
        """
        try:
            return self[key]
        except KeyError:
            return default
    
    def clear(self) -> None:
        """
        Removes all key-value pairs from the hash table.
        """
        acquired_locks = self._safe_acquire_all_locks()
        try:
            total_cleared = 0
            current_capacity = self.capacity
            for i in range(current_capacity):
                bucket = self._buckets[i]
                total_cleared += len(bucket)
                bucket.clear()
            
            with self._size_lock:
                self._size_var.value = 0  # type: ignore
                
            logger.debug(f"Cleared {total_cleared} elements from table")
            
        finally:
            for idx in acquired_locks:
                try:
                    self._locks[idx].release()
                except Exception as e:
                    logger.warning(f"Error releasing lock during clear: {e}")
    
    def setdefault(self, key: Any, default: Any = None) -> Any:
        """
        Returns the value for key if it exists, otherwise sets it to default and returns default.

        Parameters:
            key : Any (Key to look up or set)
            default : Any (Default value to set if key not found)

        Returns:
            Any: Existing value if key exists, otherwise default
        """
        index = self._hash(key)
        
        with self._bucket_lock(index):
            bucket = self._buckets[index]
            if key in bucket:
                return bucket[key]
            else:
                bucket[key] = default
                with self._size_lock:
                    self._size_var.value += 1  # type: ignore
                return default
    
    def pop(self, key: Any, default: Any = None) -> Any:
        """
        Removes the specified key and returns its value.

        Parameters:
            key : Any (Key to remove)
            default : Any (Default value to return if key not found)

        Returns:
            Any: Value associated with the removed key

        Raises:
            KeyError: If key not found and no default provided
        """
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise
    
    def popitem(self) -> Tuple[Any, Any]:
        """
        Removes and returns an arbitrary key-value pair from the hash table.

        Returns:
            Tuple[Any, Any]: Removed (key, value) pair

        Raises:
            KeyError: If the hash table is empty
        """
        current_capacity = self.capacity
        start_index = random.randint(0, current_capacity - 1)
        
        for offset in range(current_capacity):
            i = (start_index + offset) % current_capacity
            
            try:
                with self._bucket_lock(i, timeout=1.0):
                    bucket = self._buckets[i]
                    if bucket:
                        for key, value in bucket.items():
                            del bucket[key]
                            with self._size_lock:
                                self._size_var.value -= 1  # type: ignore
                            return key, value
            except TimeoutError:
                continue
        
        raise KeyError("popitem(): hash table is empty")
    
    def update(self, other: Any = None, **kwargs: Any) -> None:  # type: ignore[override]
        """
        Updates the hash table with key-value pairs from another mapping or iterable.

        Parameters:
            other : Any (Mapping or iterable of key-value pairs)
            **kwargs : Any (Additional key-value pairs as keyword arguments)
        """
        if other is not None:
            if hasattr(other, 'items'):
                items = other.items()
            elif hasattr(other, 'keys'):
                items = [(k, other[k]) for k in other.keys()]
            else:
                items = other
            for key, value in items:
                self[key] = value
                
        for key, value in kwargs.items():
            self[key] = value
    
    def __str__(self) -> str:
        """
        Returns a string representation of the hash table.

        Returns:
            str: String in dictionary format
        """
        items = list(self.items())
        item_strs = [f"{key!r}: {value!r}" for key, value in items]
        return "{" + ", ".join(item_strs) + "}"
    
    def __repr__(self) -> str:
        """
        Returns a formal string representation of the hash table.

        Returns:
            str: String that can be used to recreate the object
        """
        return f"ThreadSafeHashTable(capacity={self.capacity}, size={len(self)}, load_factor={self.load_factor:.2f})"
    
    @property
    def load_factor(self) -> float:
        """
        Returns the current load factor of the hash table.

        Returns:
            float: Ratio of current size to capacity
        """
        with self._size_lock:
            current_size = self._size_var.value  # type: ignore
            current_capacity = self.capacity
            return current_size / current_capacity if current_capacity > 0 else 0
    
    @property
    def capacity(self) -> int:
        """
        Returns the current capacity of the hash table.

        Returns:
            int: Number of buckets in the hash table
        """
        return self._capacity_var.value  # type: ignore