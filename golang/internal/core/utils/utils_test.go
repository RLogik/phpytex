package utils_test

/* ---------------------------------------------------------------- *
 * UNIT TESTS
 * ---------------------------------------------------------------- */

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"

	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * TESTCASE arrays
 * ---------------------------------------------------------------- */

func TestArrayContains(test *testing.T) {
	var assert = assert.New(test)
	var arr []string

	arr = []string{"apple", "pear", "banana"}
	assert.True(utils.ArrayContains(arr, "pear"))
	assert.False(utils.ArrayContains(arr, "Pear"))
	assert.False(utils.ArrayContains(arr, 57))
	assert.False(utils.ArrayContains(arr, true))
}

/* ---------------------------------------------------------------- *
 * TESTCASE dictionaries
 * ---------------------------------------------------------------- */

/* ---------------------------------------------------------------- *
 * TESTCASE strings
 * ---------------------------------------------------------------- */

func TestFormatPythonString(test *testing.T) {
	var assert = assert.New(test)

	// simple
	assert.Equal(utils.FormatPythonString(`The value of {{{key}}} is {value}.`, map[string]interface{}{
		"key":   "frequency",
		"value": 2109.1,
	}), `The value of {frequency} is 2109.1.`)

	// brackets
	assert.Equal(utils.FormatPythonString(`This will be {unexpanded}.`, map[string]interface{}{
		"unexpanded": "expanded",
	}), `This will be expanded.`)
	assert.Equal(utils.FormatPythonString(`This remains {{unexpanded}}.`, map[string]interface{}{
		"unexpandedkey": "expanded",
	}), `This remains {unexpanded}.`)

	// multiline
	assert.Equal(utils.FormatPythonString(`
		Hello {name}!
		Welcome to {place}!

		The temperature is {T} C.
		The sky appears blue: {is_blue_sky}.
	`, map[string]interface{}{
		"name":        "James",
		"place":       "Scotland Yard",
		"T":           7.31,
		"is_blue_sky": true,
	}), `
		Hello James!
		Welcome to Scotland Yard!

		The temperature is 7.31 C.
		The sky appears blue: true.
	`)
}

func TestDedentAndExpand(test *testing.T) {
	var assert = assert.New(test)
	var text string
	var result string

	text = `
		This is a \033[1mbold text\033[0m

	This is a text in \033[91;1mred\033[0m.
			This is indented (2 x '\\t').
	This is not indented.
	`
	result = strings.Join([]string{
		"",
		"\tThis is a \033[1mbold text\033[0m",
		"",
		"This is a text in \033[91;1mred\033[0m.",
		"\t\tThis is indented (2 x '\\t').",
		"This is not indented.",
		"",
	}, "\n")
	assert.Equal(utils.DedentAndExpand(text), result)
}
