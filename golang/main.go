package main

import (
	"embed"
	"os"
	"phpytex/internal/core/utils"
	"phpytex/internal/endpoints/ep_help"
	"phpytex/internal/endpoints/ep_run"
	"phpytex/internal/endpoints/ep_version"
)

var (
	//go:embed assets/*
	res   embed.FS
	files = map[string]string{
		"version": "assets/VERSION",
	}
)

func main() {
	cliArgs := os.Args[1:]
	if utils.ArrayContains(cliArgs, "version") {
		ep_version.Endpoint(res, files)
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
