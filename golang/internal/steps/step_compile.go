package steps

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"fmt"
	"os"
	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
	"phpytex/internal/setup/appconfig"
	"phpytex/pkg/re"
	"strings"
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
	var err error
	var cmd string
	var cmdParts []string

	cmd = appconfig.Parameters.PythonPath.GetValue()
	cmdParts = re.Split(`\s+`, cmd)
	cmdParts = append(cmdParts, fnamePy)
	logging.LogInfo(fmt.Sprintf(
		"CALL < \033[94;1m%[1]s\033[0m >",
		strings.Join(cmdParts, " "),
	))
	err = utils.PipeCall(cmdParts[0], cmdParts[1:]...)
	os.Remove(fnamePy)
	if err != nil {
		logging.LogError(
			"An error occurred during (python -> latex -> pdf) conversion.",
			fmt.Sprintf("  - Consult the error logs and the script \033[1m%[1]s\033[0m for more information.", fnamePy),
			fmt.Sprintf("  - Partial output may also be found in \033[1m%[1]s\033[0m.", fnameLatex),
		)
	}
	return err
}
