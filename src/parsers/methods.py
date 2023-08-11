#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.logic import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'tokenise_input',
    'lexed_to_string',
    'prune_tree',
    'get_subtrees',
    'collapse_tree',
    'sub_expressions',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOCAL CONSTANTS / VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# local usage only
_lexer: dict[tuple[str, str], Lark] = dict();
T = TypeVar('T');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS obtain lexer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def tokenise_input(
    grammar_name: str,
    grammar: str,
    start_token: str,
    text: str,
    collapse: bool = True,
    prune: bool = True,
    remove_terminal: bool = True,
) -> LarkTree:
    '''
    General method to token text via a grammar.

    @inputs
    - `grammar_name` - <string> unique name of the grammar (as internal identifier)
    - `grammar`      - <string> contents of \*.lark file
    - `start_token`  - <string> the token to start parsing the input with (a lowercase name from the \*.lark file)
    - `text`         - <string> text to be tokenised via the grammar.
    - `collapse`     - <boolean> whether to collapse rules marked 'collapse'.
    - `prune`        - <boolean> whether to recursively remove rules marked 'noncapture'.

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
        if collapse:
            tree = collapse_tree(tree, recursive=True);
        if prune:
            tree = prune_tree(tree, recursive=True, remove_terminal=remove_terminal);
        return tree;
    except Exception as e:
        e.add_note(f'Could not tokenise input as \x1b[1m{start_token}\x1b[0m in the grammar \x1b[1m{grammar_name}\x1b[0m!');
        raise e;

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

def prune_tree(u: LarkTree, recursive: bool = False, remove_terminal: bool = True) -> LarkTree:
    '''
    - filters out rules tagged by force with 'noncapture'.
    - optionally filters out TERMINAL rules.
    '''
    if remove_terminal:
        filt = lambda child: \
            not isinstance(child, LarkTree) \
            or not (child.data == 'noncapture' or re.match(r'[A-Z]', child.data));
    else:
        filt = lambda child: \
            not isinstance(child, LarkTree) \
            or child.data != 'noncapture';

    children = filter(filt, u.children);

    if recursive:
        children = map(
            lambda child: \
                prune_tree(child, recursive=True, remove_terminal=remove_terminal)
                if isinstance(child, LarkTree)
                else child,
            children
        );

    children: list[str | LarkTree] = list(children);

    return LarkTree(data=u.data, children=children, meta=u.meta);

def get_subtrees(u: LarkTree, remove_terminal: bool = True) -> list[LarkTree]:
    '''
    - filters out rules tagged by force with 'noncapture'.
    - optionally filters out TERMINAL rules.
    - only retains children which are themselves trees.
    '''
    u = prune_tree(u, recursive=False, remove_terminal=remove_terminal);
    return [ child for child in u.children if isinstance(u, LarkTree) ];

def collapse_tree(u: LarkTree, recursive: bool = False) -> LarkTree:
    '''
    Flattens out rules tagged by force with 'collapse'.
    '''
    if recursive:
        children = [
            collapse_tree(child, recursive=True)
            if isinstance(child, LarkTree)
            else
            child
                for child in u.children
        ];
    children = flatten([
        child.children
        if isinstance(child, LarkTree)
        and child.data == 'collapse'
        else
        [ child ]
            for child in u.children
    ]);
    return LarkTree(data=u.data, children=children, meta=u.meta);

def sub_expressions(u: LarkTree) -> list[LarkTree]:
    return [ child for child in u.children if isinstance(child, LarkTree) ];
