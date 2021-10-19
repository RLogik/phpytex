package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"github.com/antlr/antlr4/runtime/Go/antlr"
)

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

type AntlrTree struct {
	Tree   antlr.Tree
	Parser *antlr.Parser
}

/* ---------------------------------------------------------------- *
 * METHODS for types
 * ---------------------------------------------------------------- */

func (self AntlrTree) GetChildren() []AntlrTree {
	var nodes = self.Tree.GetChildren()
	var subants = make([]AntlrTree, len(nodes))
	for i, node := range nodes {
		subants[i] = AntlrTree{Tree: node, Parser: self.Parser}
	}
	return subants
}

func (self AntlrTree) GetLabel() string {
	return antlr.TreesGetNodeText(self.Tree, []string{}, *self.Parser)
}

func (self AntlrTree) GetTextContent() string {
	var expr string = ""
	var subants = self.GetChildren()
	if len(subants) == 0 {
		return self.GetLabel()
	}
	for _, subant := range subants {
		expr += subant.GetTextContent()
	}
	return expr
}
