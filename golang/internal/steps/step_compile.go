package steps

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"phpytex/internal/core/logging"
	"phpytex/internal/setup/appconfig"
)

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func Compile() error {
	var (
		err        error = nil
		fnamePy    string
		fnameLatex string
	)
	logging.LogInfo("CONVERSION (python -> latex [+ latex -> pdf]) STARTED.")

	fnamePy = appconfig.Parameters.FileTranspiled.GetValue(true)
	fnameLatex = appconfig.Parameters.FileOutput.GetValue(true)
	err = execTranspiledCode(fnamePy, fnameLatex)
	if err != nil {
		return err
	}

	logging.LogInfo("CONVERSION (python -> latex) COMPLETE.")
	if appconfig.Parameters.OptionCompileLatex.GetValue() {
		logging.LogInfo("CONVERSION (latex -> pdf) COMPLETE.")
	}

	return nil
}

/* ---------------------------------------------------------------- *
 * SECONDARY METHODS
 * ---------------------------------------------------------------- */

func execTranspiledCode(fnamePy string, fnameLatex string) error {
	return nil
}
