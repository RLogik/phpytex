package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"strings"

	"github.com/akamensky/argparse"

	"phpytex/pkg/re"
)

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

type CliArguments struct {
	Help    *argparse.Command
	Version *argparse.Command
	Run     *argparse.Command
	Quiet   *bool
	Colour  *string
	Color   *string
	File    *string
}

/* ---------------------------------------------------------------- *
 * METHODS convert string option to boolean
 * ---------------------------------------------------------------- */

func IsTrue(text string) bool {
	text = strings.TrimSpace(text)
	return re.Matches(`(?i)(^(true|t|yes|y|1|\+|\+1)$)`, text)
}

func IsFalse(text string) bool {
	text = strings.TrimSpace(text)
	return re.Matches(`(?i)(^(false|f|no|n|0|-|-1)$)`, text)
}

func (arguments *CliArguments) ShowColour() bool {
	return !(IsFalse(*arguments.Colour) || IsFalse(*arguments.Color))
}
