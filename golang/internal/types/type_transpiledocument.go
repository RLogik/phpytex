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

func (docs TranspileDocuments) GetVariables() []string {
	if docs.Variables != nil {
		return *docs.Variables
	}
	return []string{}
}

func (docs TranspileDocuments) DocumentTree(seed *int) TranspileBlock {
	// TODO
	return TranspileBlock{}
}

func (docs *TranspileDocuments) AddPreamble(name string, blocks TranspileBlocks) {
	// TODO
}

func (docs TranspileDocuments) GenerateCode(
	offset int, // 0
	preambles []string, // []string{},
	globalvars []string, // []string{},
) []string {
	var lines []string
	lines = []string{}
	// TODO
	return lines
}
