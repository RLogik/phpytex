#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.logic import *;
from src.thirdparty.misc import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'tokenise_input',
    'lexed_to_string',
    'prune_tree',
    'collapse_tree',
    'sub_expressions',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# local usage only
_lexer: dict[tuple[str, str], Lark] = dict();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS obtain lexer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def tokenise_input(
    grammar_name: str,
    grammar: str,
    start_token: str,
    text: str,
) -> LarkTree:
    '''
    General method to token text via a grammar.

    @inputs
    - `grammar_name` - <string> unique name of the grammar (as internal identifier)
    - `grammar`      - <string> contents of \*.lark file
    - `start_token`  - <string> the token to start parsing the input with (a lowercase name from the \*.lark file)
    - `text`         - <string> text to be tokenised via the grammar.

    @returns
    A Lark-Tree object with the tokens, if the text is valid according to the grammar.
    Otherwise raises Error.
    '''
    global _lexer;
    try:
        if not ((grammar_name, start_token) in _lexer):
            _lexer[(grammar_name, start_token)] = Lark(
                grammar,
                start = start_token,
                regex = True,
                # options: 'lalr', 'earley', 'cyk'
                parser = 'earley',
                # options:  auto (default), none, normal, invert
                priority = 'invert',
            );
        lexer = _lexer[(grammar_name, start_token)];
        tree = lexer.parse(text);
        return tree;
    except:
        raise Exception(f'Could not tokenise input as \x1b[1m{start_token}\x1b[0m in the grammar \x1b[1m{grammar_name}\x1b[0m!');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS filtration and conversion
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexed_to_string(u: str | LarkTree) -> str:
    '''
    Recursively collapse token to string.
    '''
    if isinstance(u, str):
        return u;
    return ''.join([ lexed_to_string(uu) for uu in u.children ]);

def prune_tree(u: LarkTree, recursive: bool = False) -> LarkTree:
    '''
    Filter out rules tagged by force with 'noncapture'.
    Filter out TERMINAL rules.
    '''
    children = [];
    for child in u.children:
        if not isinstance(child, LarkTree):
            children.append(child);
            continue;
        if child.data == 'noncapture':
            continue;
        if recursive:
            child = prune_tree(child, recursive=True);
        children.append(child);
    return LarkTree(data=u.data, children=children, meta=u.meta)

def collapse_tree(u: LarkTree, recursive: bool = False) -> LarkTree:
    '''
    Flattens out rules tagged by force with 'collapse'.
    '''
    children = [];
    for child in u.children:
        if not isinstance(child, LarkTree):
            children.append(child);
            continue;
        if recursive:
            child = collapse_tree(child, recursive=True);
        if child.data == 'collapse':
            children += child.children;
        else:
            children.append(child);
    return LarkTree(data=u.data, children=children, meta=u.meta);

def sub_expressions(u: LarkTree) -> list[LarkTree]:
    return [ child for child in u.children if isinstance(child, LarkTree) ];
