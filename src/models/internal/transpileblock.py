#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    def tab(self, delta: int = 0) -> str:
        return self.indent_symbol * (self.indent_level + delta);

    @property
    def generateContent(self) -> Generator[str, None, None]:
        tab = self.tab() if self.kind == EnumTokenisationBlockKind.code else '';
        if self.line is None:
            yield from formatBlockIndent(self.lines, indent=tab, unindent=False);
        else:
            yield f'{tab}{self.line}';

    def generateCode(
        self,
        offset: int = 0,
        anon: bool = False,
        hide: bool = False,
    ) -> Generator[str, None, None]:
        # temporarily increase indentation level (restore at end):
        current_level = self.indent_level
        self.indent_level += offset;

        match (self.kind, self.sub_kind):
            case (EnumTokenisationBlockKind.input):
                pass;
            case (EnumTokenisationBlockKind.text, EnumTokenisationBlockSubKind.empty):
                yield '{tab}____print(\'\', anon={anon}, hide={hide});'.format(tab=self.tab(), anon=anon, hide=hide);
            case (EnumTokenisationBlockKind.text, EnumTokenisationBlockSubKind.subst):
                if len(self.substitution) == 0:
                    content = '\n'.join(list(self.generateContent()));
                    yield f'{self.tab()}____print(\'\'\'{content}\'\'\'.format(), anon={anon}, hide={hide});';
                else:
                    content = '\n'.join(list(self.generateContent()));
                    yield f'{self.tab()}____print(\'\'\'{content}\'\'\'.format(';
                    for key, block in self.substitution.items():
                        # level = block.level;
                        value_lines = formatBlockIndent(block.lines, indent=self.tab(2), unindent=True);
                        value_lines[0] = re.sub(r'^\s*(.*)$', r'\1', value_lines[0]);
                        value_lines_as_str = '\n'.join(value_lines);
                        yield f'{self.tab(1)}{key} = {value_lines_as_str},';
                        # block.level = level;
                    yield f'{self.tab()}), anon={anon}, hide={hide});';
            case (EnumTokenisationBlockKind.text, _):
                for line in self.generateContent():
                    content = escapeForPython(line, withformatting=False);
                    yield f'{self.tab()}____print(\'\'\'{content}\'\'\', anon={anon}, hide={hide});';
            case (EnumTokenisationBlockKind.code, EnumTokenisationBlockSubKind.set):
                block = TranspileBlock(
                    kind = EnumTokenisationBlockKind.code,
                    line = f'{self.variable_name} = {self.variable_value};',
                    indent_level = current_level,
                    indent_symbol = self.indent_symbol,
                );
                yield from block.generateCode(offset=offset);
            case (EnumTokenisationBlockKind.code, EnumTokenisationBlockSubKind.escape):
                block = TranspileBlock(
                    kind = EnumTokenisationBlockKind.code,
                    line = 'pass;',
                    indent_level = current_level,
                    indent_symbol = self.indent_symbol
                );
                yield from block.generateCode(offset=offset);
            case (EnumTokenisationBlockKind.code, _):
                yield from self.generateContent();

        # restore original indentation level:
        self.indent_level = current_level;
        return;
