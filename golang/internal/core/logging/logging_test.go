package logging_test

/* ---------------------------------------------------------------- *
 * UNIT TESTS
 * ---------------------------------------------------------------- */

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"bytes"
	"io"
	"os"
)

/* ---------------------------------------------------------------- *
 * GLOBAL VARIABLES
 * ---------------------------------------------------------------- */

var stdout = os.Stdout
var stderr = os.Stderr

func listenToStdOut() *os.File {
	r, w, _ := os.Pipe()
	os.Stdout = w
	return r
}

func listenToStdErr() *os.File {
	r, w, _ := os.Pipe()
	os.Stderr = w
	return r
}

func readPipe(r *os.File) string {
	var buf bytes.Buffer
	io.Copy(&buf, r)
	return buf.String()
}

func restorePipes() {
	os.Stdout.Close()
	os.Stderr.Close()
	os.Stdout = stdout
	os.Stderr = stderr
}

/* ---------------------------------------------------------------- *
 * TESTCASE arrays
 * ---------------------------------------------------------------- */

// func TestArrayContains(test *testing.T) {
// 	var assert = assert.New(test)
// 	_stdout := listenToStdOut()
// 	_stderr := listenToStdErr()
// 	defer func() {
// 		restorePipes()
// 	}()
// 	logging.LogPlain("hello")
// 	assert.Equal(readPipe(_stdout), "hello")
// 	assert.Equal(readPipe(_stderr), "")
// }
