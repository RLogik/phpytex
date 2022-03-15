package logging

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"os"

	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * GLOBAL VARIABLES
 * ---------------------------------------------------------------- */

var quietmode bool = false
var ansimode bool = true
var loggingPrefix string = ""
var force bool = false
var tagAll bool = false

func GetQuietMode() bool {
	return quietmode
}

func SetQuietMode(mode bool) {
	quietmode = mode
}

func GetAnsiMode() bool {
	return ansimode
}

func SetAnsiMode(mode bool) {
	ansimode = mode
}

func GetForce() bool {
	return force
}

func SetForce(mode bool) {
	force = mode
}

func SetTagAll(mode bool) {
	tagAll = mode
}

/* ---------------------------------------------------------------- *
 * METHOD logging
 * ---------------------------------------------------------------- */

func logGeneric(tag string, lines ...interface{}) {
	if !force && quietmode {
		return
	}
	if !(tag == "") {
		tag = tag + " "
	}
	for _, line := range lines {
		_line := fmt.Sprintf("%[1]s%[2]s%[3]v", loggingPrefix, tag, line)
		if !ansimode {
			_line = utils.StripAnsi(_line)
		}
		fmt.Println(_line)
		if !tagAll {
			tag = ""
		}
	}
}

func LogPlain(lines ...interface{}) {
	SetTagAll(false)
	logGeneric("", lines...)
}

func LogInfo(lines ...interface{}) {
	SetTagAll(true)
	logGeneric("[\033[94;1mINFO\033[0m]", lines...)
}

func LogDebug(lines ...interface{}) {
	SetTagAll(true)
	logGeneric("[\033[96;1mDEBUG\033[0m]", lines...)
}

func LogWarn(lines ...interface{}) {
	SetTagAll(false)
	logGeneric("[\033[93;1mWARNING\033[0m]", lines...)
}

func LogError(lines ...interface{}) {
	SetTagAll(false)
	logGeneric("[\033[91;1mERROR\033[0m]", lines...)
}

func LogFatal(lines ...interface{}) {
	SetTagAll(false)
	logGeneric("[\033[91;1mFATAL\033[0m]", lines...)
	os.Exit(1)
}
