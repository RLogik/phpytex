package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"bufio"
	"fmt"
	"io"
	"os/exec"
	"runtime"
	"strings"
)

/* ---------------------------------------------------------------- *
 * METHODS os sensitive commands
 * ---------------------------------------------------------------- */

func IsLinux() bool {
	return !(runtime.GOOS == "windows")
}

func PipeCall(name string, parts ...string) error {
	var (
		err    error
		cmd    *exec.Cmd
		pipe   io.ReadCloser
		stream *bufio.Reader
		line   []byte
	)
	cmd = exec.Command(name, parts...)
	pipe, err = cmd.StdoutPipe()
	if err == nil {
		err = cmd.Start()
		stream = bufio.NewReader(pipe)
	}
	for err == nil {
		line, _, err = stream.ReadLine()
		if err == nil {
			fmt.Println(string(line))
		}
	}
	if err != nil && err != io.EOF {
		return fmt.Errorf(
			"Shell command < \033[94;1m%[1]s\033[0m > failed.",
			strings.Join(append([]string{name}, parts...), " "),
		)
	}
	return nil
}
