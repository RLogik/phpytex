package main

import (
	"os"
	"phpytex/core/utils"
	"phpytex/endpoints/ep_help"
	"phpytex/endpoints/ep_run"
	"phpytex/endpoints/ep_version"
)

func main() {
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
