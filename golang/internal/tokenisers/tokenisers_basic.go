package tokenisers

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"github.com/antlr/antlr4/runtime/Go/antlr"

	"phpytex/internal/tokenisers/grammars/grammarPhpytex"
	"phpytex/internal/types"
)

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func ParseExpr(text string) types.AntlrTree {
	var stream = exprToStream(text)
	var lexer = createLexer(stream)
	var tokenStream = lexerToTokenStream(lexer)
	var parser = grammarPhpytex.NewgrammarPhpytexParser(tokenStream)

	var tree = parser.Start()
	var ant = types.NewAntlrTree(tree, parser)

	return ant
}

/* ---------------------------------------------------------------- *
 * PRIVATE
 * ---------------------------------------------------------------- */

func exprToStream(text string) *antlr.InputStream {
	return antlr.NewInputStream(text)
}

func createLexer(stream *antlr.InputStream) antlr.Lexer {
	return grammarPhpytex.NewgrammarPhpytexLexer(stream)
}

func lexerToTokenStream(lexer antlr.Lexer) antlr.TokenStream {
	return antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
}
