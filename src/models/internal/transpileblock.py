#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.utils import *;
from src.models.generated.tokenisation import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'TokenisationBlock',
    'TranspileBlock',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile block
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileBlock(TokenisationBlock):
    def contents(self) -> Generator[str, None, None]:
        tab = self.indent_symbol if self.kind == EnumTokenisationBlockKind.code else '';
        if self.line is None:
            yield from text_block_indent(self.lines, indent=tab, unindent=False);
        else:
            yield f'{tab}{self.line}';

    @property
    @final_property
    def content(self) -> str:
        return '\\n'.join(list(self.contents()));

    def to_code(
        self,
        offset: int = 0,
        anon: bool = False,
        hide: bool = False,
    ) -> Generator[str, None, None]:
        # temporarily increase indentation level (restore at end):
        current_level = self.indent_level
        self.indent_level += offset;
        n = self.indent_level;
        tab = self.indent_symbol;

        match (self.kind, self.sub_kind):
            # --------------------------------
            # INPUT
            # --------------------------------
            case (EnumTokenisationBlockKind.input):
                pass;
            # --------------------------------
            # TEXT
            # --------------------------------
            case (EnumTokenisationBlockKind.text, EnumTokenisationBlockSubKind.empty):
                yield f"{tab * n}____print('', anon={anon}, hide={hide});";
            case (EnumTokenisationBlockKind.text, EnumTokenisationBlockSubKind.subst):
                if len(self.substitution) == 0:
                    yield f"{tab * n}____print('''{self.content}'''.format(), anon={anon}, hide={hide});";
                else:
                    yield f"{tab * n}____print('''{self.content}'''.format(";
                    for key, block in self.substitution.items():
                        # level = block.level;
                        value_lines = text_block_indent(block.lines, indent=tab * (n + 2), unindent=True);
                        value_lines[0] = re.sub(r'^\s*(.*)$', r'\1', value_lines[0]);
                        value_lines_as_str = '\n'.join(value_lines);
                        yield f'{tab * n}{tab}{key} = {value_lines_as_str},';
                        # block.level = level;
                    yield f'{tab * n}), anon={anon}, hide={hide});';
            case (EnumTokenisationBlockKind.text, _):
                for line in self.contents():
                    content = escape_for_python(line, with_formatting=False);
                    yield f"{tab * n}____print('''{content}''', anon={anon}, hide={hide});";
            # --------------------------------
            # CODE
            # --------------------------------
            case (EnumTokenisationBlockKind.code, EnumTokenisationBlockSubKind.set):
                block = TranspileBlock(
                    kind = EnumTokenisationBlockKind.code,
                    line = f'{self.variable_name} = {self.variable_value};',
                    indent_level = current_level,
                    indent_symbol = self.indent_symbol,
                );
                yield from block.to_code(offset=offset);
            case (EnumTokenisationBlockKind.code, EnumTokenisationBlockSubKind.escape):
                block = TranspileBlock(
                    kind = EnumTokenisationBlockKind.code,
                    line = 'pass;',
                    indent_level = current_level,
                    indent_symbol = self.indent_symbol
                );
                yield from block.to_code(offset=offset);
            case (EnumTokenisationBlockKind.code, _):
                yield self.content;

        # restore original indentation level:
        self.indent_level = current_level;
        return;
