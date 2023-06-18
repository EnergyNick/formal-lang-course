from collections import namedtuple

ArgName = namedtuple("ArgName", ["value"])
EmptyArg = namedtuple("EmptyArg", [])


class MemoryContext:
    def __init__(self):
        self._memory: dict[str, object] = dict()

    def __contains__(self, item):
        return item in self._memory

    def __setitem__(self, key, value):
        self._memory[key] = value

    def __getitem__(self, key):
        return self._memory[key]

    def clone(self):
        val = MemoryContext()
        val._memory = self._memory.copy()
        return val
