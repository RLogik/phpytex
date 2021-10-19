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

func (ant AntlrTree) getChildren() []AntlrTree {
	var nodes = ant.Tree.GetChildren()
	var subants = make([]AntlrTree, len(nodes))
	for i, node := range nodes {
		subants[i] = AntlrTree{Tree: node, Parser: ant.Parser}
	}
	return subants
}

func (ant AntlrTree) getLabel() string {
	return antlr.TreesGetNodeText(ant.Tree, []string{}, *ant.Parser)
}

func (ant AntlrTree) getTextContent() string {
	var expr string = ""
	var subants = ant.getChildren()
	if len(subants) == 0 {
		return ant.getLabel()
	}
	for _, subant := range subants {
		expr += subant.getTextContent()
	}
	return expr
}
