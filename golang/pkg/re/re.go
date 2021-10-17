package re

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"regexp"
)

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func Matches(pattern string, text string) bool {
	var reader *regexp.Regexp
	reader = regexp.MustCompile(pattern)
	return reader.MatchString(text)
}

func Sub(pattern string, substitute string, text string) string {
	var reader *regexp.Regexp
	reader = regexp.MustCompile(pattern)
	return reader.ReplaceAllString(text, substitute)
}
