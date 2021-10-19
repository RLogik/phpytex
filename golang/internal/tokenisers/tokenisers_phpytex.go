package tokenisers

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"phpytex/internal/types"
)

/* ---------------------------------------------------------------- *
 * GLOBAL VARIABLES, CONSTANTS
 * ---------------------------------------------------------------- */

//

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
	blocks = []types.TranspileBlock{}
	// TODO
	return blocks, err
}
