package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

type TranspileCommentOptions struct {
	CommentsAuto bool
	CommentsOn   bool
	ShowTree     bool
}

type TranspileBlockParameters struct {
	Keep bool
}
type TranspileBlock struct {
	Kind       string
	Content    string
	Level      int
	IndentSymb string
	Parameters TranspileBlockParameters
}

type TranspileBlocks struct {
}

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func (blocks *TranspileBlocks) Init(b ...TranspileBlock) {

}

func (blocks *TranspileBlocks) Append(block TranspileBlock) {
	// TODO
}

func (blocks *TranspileBlocks) GenerateCode(offset int) []string {
	var lines []string
	lines = []string{}
	// TODO
	return lines
}
