package utils

import (
	"fmt"
	"log"
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
