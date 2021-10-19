package cli

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"github.com/akamensky/argparse"

	"phpytex/internal/types"
)

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

func ParseCli(args []string) (*types.CliArguments, error) {
	var err error
	parser := argparse.NewParser("cli parser", "Reads options and flags from command line.")
	arguments := types.CliArguments{
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
