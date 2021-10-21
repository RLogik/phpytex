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

func TokenisePhpytex(text string) types.AntlrTree {
	var stream = exprToStream(text)
	var lexer = createLexer(stream)
	var tokenStream = lexerToTokenStream(lexer)
	var parser = grammarPhpytex.NewgrammarPhpytexParser(tokenStream)

	var t = parser.Start()
	var tree = types.NewAntlrTree(t, parser)

	return tree
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
