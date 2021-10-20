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

type Ant struct {
	tree   antlr.Tree
	parser *antlr.Parser
}

type AntlrTree struct {
	Terminal bool
	Kind     string
	Value    *string
	ant      *Ant
	children *[]AntlrTree
}

/* ---------------------------------------------------------------- *
 * METHODS for types
 * ---------------------------------------------------------------- */

func NewAnt(tree antlr.Tree, parser antlr.Parser) Ant {
	return Ant{tree: tree, parser: &parser}
}

func NewAntlrTree(tree antlr.Tree, parser antlr.Parser) AntlrTree {
	var result Ant = NewAnt(tree, parser)
	return result.ToTree()
}

func (self Ant) ToTree() AntlrTree {
	var tree AntlrTree
	if self.IsTerminal() {
		tree = AntlrTree{
			Terminal: true,
			Kind:     "TERMINAL",
			Value:    StringToPtr(self.GetText()),
			ant:      &self,
			children: nil,
		}
	} else {
		tree = AntlrTree{
			Terminal: false,
			Kind:     self.GetText(),
			Value:    nil,
			ant:      &self,
			children: nil,
		}
	}
	var children []AntlrTree
	var nodes []Ant = self.GetChildren()
	children = make([]AntlrTree, len(nodes))
	for i, subant := range nodes {
		children[i] = subant.ToTree()
	}
	if len(children) > 0 {
		tree.children = &children
	}
	return tree
}

func (self Ant) GetChildren() []Ant {
	var nodes = self.tree.GetChildren()
	var subants = make([]Ant, len(nodes))
	for i, node := range nodes {
		subants[i] = Ant{tree: node, parser: self.parser}
	}
	return subants
}

func (self AntlrTree) GetChildren() []AntlrTree {
	if self.children == nil {
		return []AntlrTree{}
	}
	return *self.children
}

func (self Ant) IsTerminal() bool {
	return (len(self.tree.GetChildren()) == 0)
}

func (self AntlrTree) IsTerminal() bool {
	return self.children == nil
}

func (self Ant) GetText() string {
	return antlr.TreesGetNodeText(self.tree, []string{}, *self.parser)
}

func (self Ant) GetTextContent() string {
	var expr string = ""
	var subants = self.GetChildren()
	if self.IsTerminal() {
		return self.GetText()
	}
	for _, subant := range subants {
		expr += subant.GetTextContent()
	}
	return expr
}

func (self AntlrTree) GetTextContent() string {
	if self.ant == nil {
		return ""
	}
	return (*self.ant).GetTextContent()
}
