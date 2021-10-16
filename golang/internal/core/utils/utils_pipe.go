package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"runtime"
)

/* ---------------------------------------------------------------- *
 * METHODS os sensitive commands
 * ---------------------------------------------------------------- */

func IsLinux() bool {
	return !(runtime.GOOS == "windows")
}

func PythonCommand() string {
	if IsLinux() {
		return "python3"
	} else {
		return "py -3"
	}
}
