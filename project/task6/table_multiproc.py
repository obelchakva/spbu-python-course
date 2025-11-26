import multiprocessing
from collections.abc import MutableMapping
from typing import Any, Iterator

class MultiHashTable(MutableMapping):

    def __init__(self, ini_size: int = 32) -> None:
        """
        Initializes the MultiHashTable with the specified initial size.

        Parameters:
            ini_size : int (Initial size of the hash table, default is 32)
        """
        self.manager = multiprocessing.Manager()
        self.ini_size = ini_size
        self.hash_table = self.manager.list([self.manager.list() for i in range(ini_size)])
        self.locks = self.manager.list([self.manager.Lock() for i in range(ini_size)])

    def _hash(self, key: Any) -> int:
        """
        Computes the hash value for a given key to determine its bucket index.

        Parameters:
            key : Any (Key to be hashed)

        Returns:
            int: Hash value modulo the table size, representing the bucket index.
        """
        return hash(key) % self.ini_size
    
    def __getitem__(self, key: Any) -> Any:
        """
        Retrieves the value associated with the specified key.

        Parameters:
            key : Any (Key to look up in the hash table)

        Returns:
            Any: Value associated with the given key

        Raises:
            KeyError: If the key is not found in the hash table
        """
        index = self._hash(key)
        for k, v in self.hash_table[index]:
            if k == key:
                return v
        raise KeyError(key)
    
    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Sets the value for the specified key in the hash table.

        Parameters:
            key : Any (Key to set in the hash table)
            value : Any (Value to associate with the key)
        """
        index = self._hash(key)
        with self.locks[index]:
            cell = self.hash_table[index]
            for idx, item in enumerate(cell):
                if item[0] == key:
                    cell[idx] = (key, value)
                    return
            cell.append((key, value))

    def __delitem__(self, key: Any) -> None:
        """
        Removes the specified key and its associated value from the hash table.

        Parameters:
            key : Any (Key to remove from the hash table)

        Raises:
            KeyError: If the key is not found in the hash table
        """
        index = self._hash(key)
        with self.locks[index]:
            cell = self.hash_table[index]
            for i, item in enumerate(cell):
                if item[0] == key:
                    del cell[i]
                    return
            raise KeyError(key)
        
    def __iter__(self) -> Iterator[Any]:
        """
        Returns an iterator over the keys in the hash table.

        Returns:
            Iterator[Any]: Iterator yielding all keys in the hash table
        """
        for i in range(self.ini_size):
            with self.locks[i]:
                cell = list(self.hash_table[i])
            for item in cell:
                yield item[0]

    def __len__(self) -> int:
        """
        Returns the number of key-value pairs in the hash table.

        Returns:
            int: Total number of elements in the hash table
        """
        size = 0
        s = self.ini_size
        for i in range(s):
            with self.locks[i]:
                size += len(self.hash_table[i])
        return size
    
    def __contains__(self, key: Any) -> bool:
        """
        Checks if the specified key exists in the hash table.

        Parameters:
            key : Any (Key to check for existence)

        Returns:
            bool: True if the key exists, False otherwise
        """
        index = self._hash(key)
        cell = self.hash_table[index]
        for item in cell:
            if item[0] == key:
                return True
        return False
    
    def clear(self) -> None:
        """
        Removes all key-value pairs from the hash table.

        Returns:
            None
        """
        s = self.ini_size
        for i in range(s):
            with self.locks[i]:
                self.hash_table[i] = self.manager.list()