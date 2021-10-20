package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"strings"
	"sync"
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
	var ch chan string
	var wg *sync.WaitGroup = &sync.WaitGroup{}
	var lines []string
	ch = make(chan string)
	wg.Add(1)
	go self.stringify(0, "", "  ", "  ", wg, ch)
	go (func() {
		wg.Wait()
		close(ch)
	})()
	lines = []string{}
	for line := range ch {
		lines = append(lines, line)
	}
	return strings.Join(lines, "\n")
}

func (self AntlrTree) stringify(
	depth int,
	prefix string,
	tab string,
	branch string,
	wg *sync.WaitGroup,
	ch chan string,
) {
	defer wg.Done()
	var indent string
	var line string
	var children = self.GetChildren()
	indent = prefix
	if depth > 0 {
		indent += strings.Repeat(tab, depth-1) + branch
	}
	if self.Terminal {
		line = fmt.Sprintf(`%[1]s- "%[2]s"`, indent, PtrToString(self.Value, "<null>"))
	} else {
		line = fmt.Sprintf(`%[1]s'%[2]s' (%[3]v):`, indent, self.Kind, len(*self.children))
	}
	ch <- line
	wg.Add(len(children)) // NOTE: do not wg.Add(1) inside loop
	for _, subtree := range children {
		go subtree.stringify(depth+1, prefix, tab, branch, wg, ch)
	}
}
