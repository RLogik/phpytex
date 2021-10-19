package tokenisers

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"strings"

	"phpytex/internal/types"
)

/* ---------------------------------------------------------------- *
 * GLOBAL VARIABLES, CONSTANTS
 * ---------------------------------------------------------------- */

var grammars map[string]string
var lexers map[string]interface{}

/* ---------------------------------------------------------------- *
 * METHODS tokenisers
 * ---------------------------------------------------------------- */

func getLexer(mode string) interface{} {
	// if _, ok := grammars[mode]; !ok {
	//     grammars[mode] = setup.GetGrammar();
	// }
	// if _, ok := lexers[mode]; !ok {
	//     lexers[mode] = Lark(
	//         grammars[mode],
	//         mode,
	//         True,
	//         'earley', # 'lalr', 'earley', 'cyk'
	//         'invert', # auto (default), none, normal, invert
	//     );
	// return lexers[mode];
	return nil
}

func tokeniseInput(mode string, text string) {
	// u, err := getLexer(mode).parse(text)
	// fmt.Errorf('Could not tokenise input as \033[1m{}\033[0m!'.format(mode));
}

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func ParseText(
	text string,
	indentation types.IndentationTracker,
	offset string,
) ([]types.TranspileBlock, error) {
	var err error = nil
	var blocks []types.TranspileBlock

	fmt.Println(text)

	// TODO
	if strings.TrimSpace(text) == "" {
		return []types.TranspileBlock{}, nil
	}

	// tree = tokeniseInput("blocks", text)
	// return lexedToBlocks(tree, offset, indentation)

	return blocks, err
}
