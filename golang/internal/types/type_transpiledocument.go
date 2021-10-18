package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

type TranspileFileNameScheme struct {
	File string
	Pre  string
	Main string
}

type TranspileDocument struct {
	Root       string
	IndentSymb string
}

type TranspileDocuments struct {
	Root       string
	IndentSymb string
	Schemes    TranspileFileNameScheme
	Variables  *[]string
}

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func (docs *TranspileDocuments) DocumentTree(seed *int) TranspileBlock {
	// TODO
	return TranspileBlock{}
}

func (docs *TranspileDocuments) AddPreamble(name string, blocks TranspileBlocks) {
	// TODO
}
