package customtypes

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"regexp"
	"strings"

	"github.com/akamensky/argparse"
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
	re := regexp.MustCompile(`(?i)(^(true|t|yes|y|1|\+|\+1)$)`)
	return re.MatchString(text)
}

func IsFalse(text string) bool {
	text = strings.TrimSpace(text)
	re := regexp.MustCompile(`(?i)(^(false|f|no|n|0|-|-1)$)`)
	return re.MatchString(text)
}

func (arguments *CliArguments) ShowColour() bool {
	return !(IsFalse(*arguments.Colour) || IsFalse(*arguments.Color))
}
