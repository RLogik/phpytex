package re

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"regexp"
)

/* ---------------------------------------------------------------- *
 * GLOBAL VARIABLES
 * ---------------------------------------------------------------- */

type Reader struct {
	regex       *regexp.Regexp
	lastpattern *string
}

var defaultReader Reader = Reader{}

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func Matches(pattern string, text string) bool {
	return defaultReader.Matches(pattern, text)
}

func Sub(pattern string, substitute string, text string) string {
	return defaultReader.Sub(pattern, substitute, text)
}

func Split(pattern string, text string) []string {
	return defaultReader.Split(pattern, text)
}

func (r *Reader) Matches(pattern string, text string) bool {
	r.setReader(pattern)
	return r.regex.MatchString(text)
}

func (r *Reader) Sub(pattern string, substitute string, text string) string {
	r.setReader(pattern)
	return r.regex.ReplaceAllString(text, substitute)
}

func (r *Reader) Split(pattern string, text string) []string {
	r.setReader(pattern)
	return r.regex.Split(text, -1)
}

/* ---------------------------------------------------------------- *
 * PRIVATE MEHODS
 * ---------------------------------------------------------------- */

func (r *Reader) setReader(pattern string) {
	if r.regex == nil || r.lastpattern == nil || *r.lastpattern != pattern {
		r.lastpattern = &pattern
		r.regex = regexp.MustCompile(pattern)
	}
}
