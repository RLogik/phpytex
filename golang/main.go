package main

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"embed"
	"os"

	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
	"phpytex/internal/endpoints"
	"phpytex/internal/setup"
	"phpytex/internal/setup/appconfig"
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
	patternConfig = `^(|.*\.)(phpytex|phpycreate)\.(yml|yaml)$`
)

/* ---------------------------------------------------------------- *
 * METHOD main
 * ---------------------------------------------------------------- */

func main() {
	// set assets
	setup.Res = res
	setup.Assets = assets

	// parse cli arguments
	arguments := setup.ParseCli(os.Args)

	// initialise internal app config
	appconfig.Init()
	appconfig.SetPatternConfig(utils.StringToPtr(patternConfig))

	// initialise logging options
	logging.SetQuietMode(*arguments.Quiet)
	logging.SetAnsiMode(arguments.ShowColour())

	if arguments.Version.Happened() {
		endpoints.Version()
		return
	} else if arguments.Help.Happened() {
		endpoints.Help()
		return
	} else if arguments.Run.Happened() {
		endpoints.Run(*arguments.File)
		return
	} else {
		endpoints.Help()
		return
	}
}
