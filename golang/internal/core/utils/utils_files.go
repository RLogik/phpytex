package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"io/ioutil"
	"os"
	"regexp"
)

/* ---------------------------------------------------------------- *
 * METHOD get files by pattern
 * ---------------------------------------------------------------- */

func GetFilesByPattern(path string, filepattern string) []string {
	files_filtered := []string{}
	regex := regexp.MustCompile(filepattern)
	files, err := ioutil.ReadDir(path)
	if err == nil {
		for _, file := range files {
			fname := file.Name()
			if regex.MatchString(fname) {
				files_filtered = append(files_filtered, fname)
			}
		}
	}
	return files_filtered
}

/* ---------------------------------------------------------------- *
 * METHOD check path exists
 * ---------------------------------------------------------------- */

func CheckPathExists(path string) bool {
	_, err := os.Stat(path)
	return !os.IsNotExist(err)
}
