class Stek:
    def __init__(self):
        self._podaci = []

    def push(self, element):
        self._podaci.append(element)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop sa praznog steka")
        return self._podaci.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek na praznom steku")
        return self._podaci[-1]

    def is_empty(self):
        return len(self._podaci) == 0

    def __len__(self):
        return len(self._podaci)

    def __iter__(self):
        return iter(self._podaci)
