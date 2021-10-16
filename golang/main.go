package main

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"embed"
	"os"

	"phpytex/internal/core/utils"
	"phpytex/internal/endpoints"
	"phpytex/internal/setup"
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
	cliArgs := os.Args[1:]
	if utils.ArrayContains(cliArgs, "version") {
		endpoints.Version()
		return
	} else if utils.ArrayContains(cliArgs, "help") {
		endpoints.Help()
		return
	} else if utils.ArrayContains(cliArgs, "run") {
		endpoints.Run()
		return
	} else {
		endpoints.Help()
		return
	}
}
