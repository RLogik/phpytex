package cli

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

type Arguments struct {
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

func (arguments *Arguments) ShowColour() bool {
	return !(IsFalse(*arguments.Colour) || IsFalse(*arguments.Color))
}

/* ---------------------------------------------------------------- *
 * LOCAL VARIABLES / CONSTANTS
 * ---------------------------------------------------------------- */

var optionsQuiet = argparse.Options{
	Help:     "Runs the programme in quite mode.",
	Required: false,
	Default:  false,
}

var optionsColour = argparse.Options{
	Help:     "Whether or not to display console logging in colour (default=true).",
	Required: false,
	// NOTE: no `Boolean` option available!
	Default: "true",
}

var optionsFile = argparse.Options{
	Help:     "Optional path to config file for run endpoint.",
	Required: false,
	Default:  "",
}

/* ---------------------------------------------------------------- *
 * METHODS parse cli
 * ---------------------------------------------------------------- */

func ParseCli(args []string) (*Arguments, error) {
	var err error
	parser := argparse.NewParser("cli parser", "Reads options and flags from command line.")
	arguments := Arguments{
		Help:    parser.NewCommand("help", "Calls endpoint to display help."),
		Version: parser.NewCommand("version", "Calls endpoint to display version."),
		Run:     parser.NewCommand("run", "Calls endpoint to run transpiler."),
		Quiet:   parser.Flag("q", "quiet", &optionsQuiet),
		// NOTE: allow both spellings
		Colour: parser.String("", "colour", &optionsColour),
		Color:  parser.String("", "color", &optionsColour),
		File:   parser.String("", "file", &optionsFile),
	}
	err = parser.Parse(args)
	return &arguments, err
}
