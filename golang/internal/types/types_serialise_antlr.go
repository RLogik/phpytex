package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"strings"
)

/* ---------------------------------------------------------------- *
 * METHODS serialisation of antlr types
 * ---------------------------------------------------------------- */

func (self AntlrTree) Serialise() map[string]interface{} {
	var serialised = map[string]interface{}{
		"Kind":     self.Kind,
		"Value":    self.Value,
		"children": nil,
	}
	var subtrees = self.GetChildren()
	if len(subtrees) > 0 {
		var children = make([]map[string]interface{}, len(subtrees))
		for i, subtree := range subtrees {
			children[i] = subtree.Serialise()
		}
	}
	serialised["children"] = subtrees
	return serialised
}

func (self AntlrTree) String() string {
	var lines []string
	self.stringify(0, "", "  ", "  ", &lines)
	return strings.Join(lines, "\n")
}

func (self AntlrTree) stringify(
	depth int,
	prefix string,
	tab string,
	branch string,
	lines *[]string,
) {
	var indent string
	var line string
	var children = self.GetChildren()
	indent = prefix
	if depth > 0 {
		indent += strings.Repeat(tab, depth-1) + branch
	}
	if self.Terminal {
		line = fmt.Sprintf(`%[1]s- "%[2]s"`, indent, PtrToString(self.Value, `null`))
	} else {
		line = fmt.Sprintf(`%[1]s'%[2]s': # has %[3]v children`, indent, self.Kind, len(*self.children))
	}
	*lines = append(*lines, line)
	for _, subtree := range children {
		subtree.stringify(depth+1, prefix, tab, branch, lines)
	}
}
