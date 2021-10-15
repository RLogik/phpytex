package main

import (
	"embed"
	"os"

	"phpytex/internal/core/utils"
	"phpytex/internal/endpoints/ep_help"
	"phpytex/internal/endpoints/ep_run"
	"phpytex/internal/endpoints/ep_version"
	"phpytex/internal/setup/appconfig"
)

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

func main() {
	appconfig.Res = res
	appconfig.Assets = assets
	cliArgs := os.Args[1:]
	if utils.ArrayContains(cliArgs, "version") {
		ep_version.Endpoint()
		return
	} else if utils.ArrayContains(cliArgs, "help") {
		ep_help.Endpoint()
		return
	} else if utils.ArrayContains(cliArgs, "run") {
		ep_run.Endpoint()
		return
	} else {
		ep_help.Endpoint()
		return
	}
}
