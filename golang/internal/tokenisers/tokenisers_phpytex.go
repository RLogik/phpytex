package tokenisers

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
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

func tokeniseInput(mode string, text string) types.AntlrTree {
	return TokenisePhpytex(mode, text)
}

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func ParseText(
	text string,
	indentation types.IndentationTracker,
	offset string,
) ([]types.TranspileBlock, error) {
	if strings.TrimSpace(text) == "" {
		return []types.TranspileBlock{}, nil
	}

	tree := tokeniseInput("blocks", text)
	return lexedToBlocks(tree, offset, indentation)
}

func lexedToBlocks(
	u types.AntlrTree,
	offset string,
	indentation types.IndentationTracker,
) ([]types.TranspileBlock, error) {
	// TODO
	return []types.TranspileBlock{}, nil
}
