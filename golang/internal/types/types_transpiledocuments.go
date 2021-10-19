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

type TranspileDocuments struct {
	Root       string
	IndentSymb string
	Schemes    TranspileFileNameScheme
	// private
	edges     *[][2]string
	paths     *[]string
	variables *[]string
	anon      map[string]bool
}

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func (docs TranspileDocuments) GetEdges() [][2]string {
	if docs.edges != nil {
		return *docs.edges
	}
	return [][2]string{}
}

func (docs TranspileDocuments) GetVariables() []string {
	if docs.variables != nil {
		return *docs.variables
	}
	return []string{}
}

func (docs TranspileDocuments) GetPaths() []string {
	if docs.paths != nil {
		return *docs.paths
	}
	return []string{}
}

func (docs TranspileDocuments) GetSubPaths(path string) []string {
	var m map[string]bool
	var subpath string
	var subpaths []string
	var edge [2]string
	subpaths = []string{}
	for _, edge = range docs.GetEdges() {
		if edge[1] == path {
			subpath = edge[0]
			if _, ok := m[subpath]; ok {
				continue
			}
			m[subpath] = true
			subpaths = append(subpaths, path)
		}
	}
	return subpaths
}

func (docs TranspileDocuments) IsAnon(path string) bool {
	if value, ok := docs.anon[path]; ok {
		return value
	}
	return false
}

func (docs *TranspileDocuments) AddDocument(path string) {
	// TODO
}

func (docs *TranspileDocuments) AddBlocks(name string, blocks TranspileBlocks) {
	// TODO
}

func (docs *TranspileDocuments) AddPreamble(name string, blocks TranspileBlocks) {
	// TODO
}

func (docs *TranspileDocuments) DocumentStamp(depth int, start bool) TranspileBlock {
	var block TranspileBlock
	block = TranspileBlock{}
	// TODO
	return block
}
