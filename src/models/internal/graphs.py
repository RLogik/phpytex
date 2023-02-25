#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.models.internal.dictionaries import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'property_inheritance_graph',
    'get_roots_graph',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS for graphs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def update_inheritance_graph(
    edges: list[tuple[str, str]],
    state: DictionaryWithDefault[str, bool],
    force: list[str] = [],
):
    '''
    @inputs:
    - `edges` - edges of a finite graph.
    - `state` - dictionary, assigning to each node, if property holds.
    - `force` - list of nodes forced to have property.

    @returns:
    Updates `state` to be the transitive closure: children forcibly inherit `True` from parent nodes.
    '''
    for key in force:
        state[key] = True;
    while True:
        changed = False;
        for u, v in edges:
            if state[u] and not state[v]:
                state[v] = True;
                changed = True;
        if not changed:
            break;
    return;

def get_roots_graph(
    nodes: list[str],
    edges: list[tuple[str, str]],
) -> list[str]:
    '''
    Returns minimal elements in graph.
    '''
    rank = factory_dictionary_str_int_zero();
    for u, v in edges:
        rank[v] = max(rank[v], rank[u] + 1);
    return [u for u in nodes if rank[u] == 0];
