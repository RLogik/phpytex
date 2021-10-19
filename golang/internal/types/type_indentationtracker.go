package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

type IndentationTracker struct {
	Symb      string
	Pattern   string
	reference int
	level     int
}

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func NewIndentationTracker(Symb string, Pattern string) IndentationTracker {
	var it IndentationTracker = IndentationTracker{Symb: Symb, Pattern: Pattern}
	it.Init()
	return it
}

func (it *IndentationTracker) Init(options ...string) {
	var reference string = utils.GetArrayStringValue(&options, 0, "")
	it.level = 0
	it.reference = utils.SizeOfIndent(reference, it.Symb)
}

func (it IndentationTracker) GetLevel() int {
	return it.level
}

func (it *IndentationTracker) relativeOffset(s string) int {
	var n int = utils.SizeOfIndent(s, it.Symb) - it.reference
	if n < 0 {
		n = 0
	}
	return n
}

func (it *IndentationTracker) SetOffset(s string) {
	it.level = it.relativeOffset(s)
}

func (it *IndentationTracker) DecrOffset() {
	it.level--
	if it.level < 0 {
		it.level = 0
	}
}

func (it *IndentationTracker) Incroffset() {
	it.level++
}
