package main

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"embed"
	"os"

	"phpytex/internal/core/logging"
	"phpytex/internal/endpoints"
	"phpytex/internal/setup"

	"github.com/akamensky/argparse"
)

/* ---------------------------------------------------------------- *
 * GLOBAL VARIABLES
 * ---------------------------------------------------------------- */

var (
	//go:embed assets/*
	res    embed.FS
	assets = map[string]string{
		"version": "assets/VERSION",
		"help":    "assets/HELP",
		"pre":     "assets/templates/template_pre",
		"post":    "assets/templates/template_post",
	}
)

/* ---------------------------------------------------------------- *
 * METHOD main
 * ---------------------------------------------------------------- */

func main() {
	setup.Res = res
	setup.Assets = assets
	arguments := setParser(os.Args)

	logging.SetQuietMode(*arguments.quiet)

	if arguments.version.Happened() {
		endpoints.Version()
		return
	} else if arguments.help.Happened() {
		endpoints.Help()
		return
	} else if arguments.run.Happened() {
		endpoints.Run(*arguments.file)
		return
	} else {
		endpoints.Help()
		return
	}
}

/* ---------------------------------------------------------------- *
 * PRIVATE METHODS
 * ---------------------------------------------------------------- */

type cliArguments struct {
	help    *argparse.Command
	version *argparse.Command
	run     *argparse.Command
	quiet   *bool
	file    *string
}

func setParser(cliArgs []string) cliArguments {
	parser := argparse.NewParser("cli parser", "Reads options and flags from command line.")
	arguments := cliArguments{
		help:    parser.NewCommand("help", "Calls endpoint to display help."),
		version: parser.NewCommand("version", "Calls endpoint to display version."),
		run:     parser.NewCommand("run", "Calls endpoint to run transpiler."),
		quiet: parser.Flag("q", "quiet", &argparse.Options{
			Help:     "Runs the programme in quite mode.",
			Required: false,
			Default:  false,
		}),
		file: parser.String("", "file", &argparse.Options{
			Help:     "Optional path to config file for run endpoint.",
			Required: false,
			Default:  "",
		}),
	}
	parser.Parse(cliArgs)
	return arguments
}
