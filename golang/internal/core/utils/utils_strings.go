package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"log"
	"regexp"
	"strconv"
	"strings"

	"github.com/lithammer/dedent"
	"github.com/slongfield/pyfmt"
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
	re := regexp.MustCompile(`\x1b[^m]*m`)
	return re.ReplaceAllString(text, "")
}
