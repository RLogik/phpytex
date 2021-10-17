package endpoints

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"phpytex/internal/core/logging"
	"phpytex/internal/setup"
	"phpytex/internal/setup/appconfig"
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

func Run(fnameConfig string) error {
	var err error
	logging.LogPlain(setup.Logo())
	err = steps.Configure(fnameConfig)
	if err != nil {
		return err
	}
	if appconfig.Parameters.OptionIgnore.GetValue() {
		logging.LogInfo("Transpilation will be skipped.")
		return nil
	}
	err = steps.Create()
	if err != nil {
		return err
	}
	// err = steps.Transpile()
	// if err != nil {
	// 	return err
	// }
	// if appconfig.Parameters.OptionDebug.GetValue() {
	// 	logging.LogInfo(utils.FormatString(
	// 		"The result of transpilation can be viewed in \033[1m{fnamePy}\033[0m",
	// 		map[string]interface{}{
	// 			"fnamePy": appconfig.Parameters.FileTranspiled.GetValue(),
	// 		}))
	// 	return nil
	// }
	// err = steps.Compile()
	// if err != nil {
	// 	return err
	// }
	return nil
}
