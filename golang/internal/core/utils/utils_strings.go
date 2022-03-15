package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"log"
	"reflect"
	"strconv"
	"strings"

	"github.com/lithammer/dedent"
	"github.com/slongfield/pyfmt"

	"phpytex/pkg/re"
)

/* ---------------------------------------------------------------- *
 * METHOD format strings with dictionary substitution
 * ---------------------------------------------------------------- */

func FormatPythonString(text string, arguments map[string]interface{}) string {
	var (
		err      error
		key      string
		value    interface{}
		kind     reflect.Kind
		refValue reflect.Value
	)
	// force compatibility of expressions with python
	for key, value = range arguments {
		kind = reflect.TypeOf(value).Kind()
		switch kind {
		case reflect.Ptr:
			refValue = reflect.ValueOf(value)
			if refValue.IsNil() {
				arguments[key] = "None"
			}
		case reflect.Bool:
			arguments[key] = strings.Title(fmt.Sprintf(`%v`, value))
		}
	}
	text, err = pyfmt.Fmt(text, arguments)
	if err != nil {
		log.Fatal(err)
	}
	return text
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

func DedentIgnoreEmptyLines(text string) string {
	return dedent.Dedent(text)
}

func DedentIgnoreFirstAndLast(text string) string {
	text = re.Sub(`^\s*[\n\r]|[\n\r]\s*$`, ``, text)
	return DedentIgnoreEmptyLines(text)
}

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

func FormatTextBlockAsList(text string, options ...bool) []string {
	var unindent bool = GetArrayBoolValue(&options, 0, true)
	if unindent {
		text = DedentIgnoreFirstAndLast(text)
	}
	return re.Split(`\n`, text)
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
