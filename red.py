from collections import deque

class Red:
    def __init__(self):
        self._podaci = []

    def enqueue(self, element):
        self._podaci.append(element)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue sa praznog reda")
        return self._podaci.pop(0)

    def head(self):
        if self.is_empty():
            raise IndexError("head praznog reda")
        return self._podaci[0]

    def is_empty(self):
        return len(self._podaci) == 0

    def __len__(self):
        return len(self._podaci)

    def __iter__(self):
        return iter(self._podaci)

class DequeRed:
    def __init__(self):
        self._podaci = deque()

    def enqueue(self, element):
        self._podaci.append(element)

    def dequeue(self):
        if not self._podaci:
            raise IndexError("dequeue sa praznog reda")
        return self._podaci.popleft()

    def head(self):
        if not self._podaci:
            raise IndexError("head praznog reda")
        return self._podaci[0]

    def is_empty(self):
        return len(self._podaci) == 0

    def __len__(self):
        return len(self._podaci)
