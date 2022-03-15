// Usage: https://blog.gopheracademy.com/advent-2017/parsing-with-antlr4-and-go
grammar grammarPhpytex; // NOTE: do not change this name!

// ---------------- SYMBOLS ---------------- //

NEWLINE: [\r?\n];
WORD: [a-zA-Z]+;

blocks: (block NEWLINE)* block?;
block: blocktypeone | blocktypetwo;

blocktypeone: '1' WORD;
blocktypetwo: '2' WORD;
