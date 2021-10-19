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
	"phpytex/internal/setup/appconfig"
	"phpytex/internal/setup/cli"
	"phpytex/internal/types"
)

/* ---------------------------------------------------------------- *
 * GLOBAL VARIABLES
 * ---------------------------------------------------------------- */

var (
	// !!! NOTE: do not remove the following "comment", as it is a preprocessing instruction !!!
	//go:embed assets/*
	res    embed.FS
	assets = map[string]string{
		"version": "assets/VERSION",
		"logo":    "assets/LOGO",
		"help":    "assets/HELP",
		"pre":     "assets/templates/template_pre",
		"post":    "assets/templates/template_post",
	}
)

/* ---------------------------------------------------------------- *
 * METHOD main
 * ---------------------------------------------------------------- */

func main() {
	var err error
	var arguments *types.CliArguments

	// set assets
	setup.Res = res
	setup.Assets = assets

	// parse cli arguments
	arguments, err = cli.ParseCli(os.Args)

	// initialise internal app config
	if err == nil {
		err = appconfig.Init()
	}

	// initialise logging options
	if err == nil {
		logging.SetQuietMode(*arguments.Quiet)
		logging.SetAnsiMode(arguments.ShowColour())
	}

	if err == nil {
		if arguments.Version.Happened() {
			endpoints.Version()
		} else if arguments.Help.Happened() {
			endpoints.Help()
		} else if arguments.Run.Happened() {
			err = endpoints.Run(*arguments.File)
		} else {
			endpoints.Help()
		}
	}

	if err != nil {
		logging.LogFatal(err)
	}
}
