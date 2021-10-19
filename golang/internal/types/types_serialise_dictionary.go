package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"strings"

	"gopkg.in/yaml.v3"

	"phpytex/internal/core/utils"
	"phpytex/pkg/re"
)

/* ---------------------------------------------------------------- *
 * METHOD display map as a simplified yaml with special formatting
 * ---------------------------------------------------------------- */

func (dict Dictionary) DisplayMapAsStamp(prefix string, tab string, options ...bool) (string, error) {
	var x map[string]interface{}
	var err error
	var serialised string
	var obj []byte
	var alignKeys bool = utils.GetArrayBoolValue(&options, 0, false)
	var upperCase bool = utils.GetArrayBoolValue(&options, 1, false)
	var lowerCase bool = utils.GetArrayBoolValue(&options, 2, false)
	var titleCase bool = utils.GetArrayBoolValue(&options, 3, false)
	var transformer func(string) string
	var (
		lines   []string
		indent  string
		line    string
		key     string
		value   string
		pattern string
		reader  re.Reader
	)

	if dict.GetValues() == nil {
		return "", nil
	}

	x = *dict.GetValues()

	obj, err = yaml.Marshal(x)
	if err != nil {
		return "", err
	}
	serialised = string(obj)

	transformer = func(x string) string { return x }
	if upperCase {
		transformer = func(x string) string { return strings.ToUpper(x) }
	} else if lowerCase {
		transformer = func(x string) string { return strings.ToLower(x) }
	} else if titleCase {
		transformer = func(x string) string { return strings.Title(x) }
	}

	if !(alignKeys || upperCase || lowerCase || titleCase) {
		return serialised, nil
	}

	lines = re.Split(`\n`, serialised)
	serialised = ""
	for _, line = range lines {
		indent = re.Sub(`^(\s*)(.*)$`, `$1`, line)
		line = re.Sub(`^(\s*)(.*)$`, `$2`, line)
		line = re.Sub(`^(.*)(:|-)\s*\|.*$`, `$1$2`, line)
		pattern = `^(\S.*):\s*(.*)$`
		if reader.Matches(pattern, line) {
			key = reader.Sub(pattern, `$1`, line)
			value = reader.Sub(pattern, `$2`, line)
			if value == "" {
				line = fmt.Sprintf(`%[1]s:`, transformer(key))
			} else {
				line = fmt.Sprintf(`%[1]s: %[2]s`, transformer(key), value)
			}
		}
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		if serialised != "" {
			serialised += "\n"
		}
		serialised += prefix + re.Sub(`    `, tab, indent) + line
	}

	// TODO add formatting for key alignment

	return serialised, nil
}
