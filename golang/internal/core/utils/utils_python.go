package utils

import (
	"encoding/json"
)

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * METHOD pipe
 * ---------------------------------------------------------------- */

func PythonCommand() string {
	if IsLinux() {
		return "python3"
	} else {
		return "py -3"
	}
}

/* ---------------------------------------------------------------- *
 * METHOD conversion
 * ---------------------------------------------------------------- */

func ConvertToPythonString(value interface{}, indent int, multiline bool, indentchar string) (string, error) {
	var err error
	var obj []byte
	obj, err = json.Marshal(value)
	if err != nil {
		return "", err
	}
	return string(obj), nil
}
