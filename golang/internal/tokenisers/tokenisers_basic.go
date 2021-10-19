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
	var lexer = createLexer(text)
	var tokenStream = lexerToTokenStream(lexer)
	var prs = grammarPhpytex.NewgrammarPhpytexParser(tokenStream)
	var tree = prs.Start()
	var ant = newAntlrTree(tree, prs)
	return ant
}

/* ---------------------------------------------------------------- *
 * PRIVATE
 * ---------------------------------------------------------------- */

func exprToStream(u string) *antlr.InputStream {
	return antlr.NewInputStream(u)
}

func createLexer(u string) antlr.Lexer {
	stream := exprToStream(u)
	return grammarPhpytex.NewgrammarPhpytexLexer(stream)
}

func lexerToTokenStream(lexer antlr.Lexer) antlr.TokenStream {
	return antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
}

func newAntlrTree(tree antlr.Tree, parser antlr.Parser) types.AntlrTree {
	return types.AntlrTree{Tree: tree, Parser: &parser}
}
