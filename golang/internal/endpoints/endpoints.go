package endpoints

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"phpytex/internal/core/logging"
	"phpytex/internal/setup"
	"phpytex/internal/steps"
)

/* ---------------------------------------------------------------- *
 * METHOD version
 * ---------------------------------------------------------------- */

func Version() {
	logging.SetForce(true)
	logging.LogPlain(setup.Version())
}

/* ---------------------------------------------------------------- *
 * METHOD help
 * ---------------------------------------------------------------- */

func Help() {
	logging.SetForce(true)
	logging.LogPlain(
		"",
		setup.Logo(),
		setup.Help(),
		"",
	)
}

/* ---------------------------------------------------------------- *
 * METHOD run
 * ---------------------------------------------------------------- */

func Run(fnameConfig string) {
	logging.LogPlain(setup.Logo())
	steps.Configure(fnameConfig)
	// if appconfig.getOptionIgnore() {
	// 	logging.LogInfo("\033[32;1m(PH(p)y)tex\033[0m transpilation will be skipped.")
	// 	return
	// }
	// steps.Create()
	// steps.Transpile()
	// if appconfig.getOptionDebug() {
	// 	logging.LogInfo(utils.FormatString(
	// 		"The result of transpilation can be viewed in \033[1m{fnamePy}\033[0m",
	// 		map[string]interface{}{
	// 			"fnamePy": appconfig.getFileTranspiled(),
	// 		}))
	// 	return
	// }
	// steps.Compile()
	// return
}
