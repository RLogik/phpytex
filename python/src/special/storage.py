#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;
from typing import Dict;
from typing import List;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Storage',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Storage
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Storage():
    _depth: int;
    states: List[Dict[str, Any]];

    def __init__(self):
        self.states = [];
        self._depth   = -1;
        return;

    def __len__(self):
        return len(self.states);

    def clear(self):
        '''
        Clears state at current depth.
        '''
        n = self._depth;
        if n < 0 or n >= len(self.states):
            raise Exception('Cannot clear state from storage. Index out of bounds!');
        self.states[n] = dict();
        return;

    def save(self, key: str, value):
        '''
        Save key-value pair to state at current depth.
        '''
        n = self._depth;
        if n < 0 or n >= len(self.states):
            raise Exception('Cannot save from storage. Index out of bounds!');
        self.states[n][key] = value;
        return;

    def load(self) -> Dict[str, Any]:
        '''
        Get key-value dictionary of state at current depth.
        '''
        n = self._depth;
        if n < 0 or n >= len(self.states):
            raise Exception('Cannot load from storage. Index out of bounds!');
        return self.states[n];

    def get(self, key: str) -> Any:
        '''
        Get value based on key at current depth.
        '''
        state = { key: None, **self.load() };
        return state[key];

    def push(self, state: Dict[str, Any] = {}):
        '''
        Create state at deeper level and move to this depth.
        '''
        n = self._depth;
        self._depth = max(n + 1, 0);
        self.states.append(state);
        return;

    def pop(self) -> Dict[str, Any]:
        '''
        Extract state at current level, and move to higher depth.
        '''
        item = self.load_all();
        n = self._depth;
        self.states = self.states[:max(n,0)];
        self._depth = max(n - 1, -1);
        return item;
