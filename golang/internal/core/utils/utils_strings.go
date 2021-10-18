package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"log"
	"strconv"
	"strings"

	"github.com/lithammer/dedent"
	"github.com/slongfield/pyfmt"
	"gopkg.in/yaml.v3"

	"phpytex/pkg/re"
)

/* ---------------------------------------------------------------- *
 * METHOD format strings with dictionary substitution
 * ---------------------------------------------------------------- */

func FormatString(text string, args map[string]interface{}) string {
	var s string
	var err error
	s, err = pyfmt.Fmt(text, args)
	if err != nil {
		log.Fatal(err)
	}
	return s
}

/*
Alternative, uses standard imports
Issue: cannot handle '{' as literal character.

import (
	"bytes"
	"html/template"
)

func FormatString(text string, args map[string]interface{}) string {
	var buff bytes.Buffer
	temp := template.New("")
	template.Must(temp.Parse(text)).Execute(&buff, args)
	s := buff.String()
	return s
}
*/

/* ---------------------------------------------------------------- *
 * METHOD dedent textblock and expand escaped symbols
 * ---------------------------------------------------------------- */

func DedentAndExpand(text string) string {
	var err error
	var result []string
	result = []string{}
	text = dedent.Dedent(text)
	lines := strings.Split(text, "\n")
	for _, line := range lines {
		line = fmt.Sprintf(`"%s"`, line)
		line, err = strconv.Unquote(line)
		if err != nil {
			log.Fatal(err)
		}
		result = append(result, line)
	}
	return strings.Join(result, "\n")
}

/* ---------------------------------------------------------------- *
 * METHODS metrics
 * ---------------------------------------------------------------- */

func LengthOfWhiteSpace(s string) int {
	var char_ string
	var n int = 0
	for _, char := range s {
		char_ = string(char)
		if char_ == " " {
			n += 1
		} else if char_ == "\t" {
			n = (n - n%8) + 8 // next tab stop
		}
	}
	return n
}

func SizeOfIndent(s string, indentSymb string) int {
	lenIndent := LengthOfWhiteSpace(s)
	lenUnit := LengthOfWhiteSpace(indentSymb)
	return int(float64(lenIndent) / float64(lenUnit))
}

/* ---------------------------------------------------------------- *
 * METHODS ansi
 * ---------------------------------------------------------------- */

func StripAnsi(text string) string {
	return re.Sub(`\x1b[^m]*m`, ``, text)
}

/* ---------------------------------------------------------------- *
 * METHOD display map as a simplified yaml with special formatting
 * ---------------------------------------------------------------- */

func DisplayMapAsStamp(x map[string]interface{}, prefix string, tab string, options ...bool) (string, error) {
	var err error
	var serialised string
	var obj []byte
	var alignKeys bool = GetArrayBoolValue(&options, 0, false)
	var upperCase bool = GetArrayBoolValue(&options, 1, false)
	var lowerCase bool = GetArrayBoolValue(&options, 2, false)
	var titleCase bool = GetArrayBoolValue(&options, 3, false)
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
		transformer = func(x string) string { return strings.ToTitle(x) }
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
