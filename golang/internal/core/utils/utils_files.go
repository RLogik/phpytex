package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"io/fs"
	"io/ioutil"
	"os"
	"regexp"
)

/* ---------------------------------------------------------------- *
 * METHOD get files by pattern
 * ---------------------------------------------------------------- */

func GetFilesByPattern(path string, filepattern string) ([]string, error) {
	var err error
	var files []fs.FileInfo
	files_filtered := []string{}
	regex := regexp.MustCompile(filepattern)
	files, err = ioutil.ReadDir(path)
	if err != nil {
		return []string{}, err
	}
	for _, file := range files {
		fname := file.Name()
		if regex.MatchString(fname) {
			files_filtered = append(files_filtered, fname)
		}
	}
	return files_filtered, err
}

func GetFirstFileByPattern(path string, filepattern string) (string, error) {
	var file string = ""
	files, err := GetFilesByPattern(path, filepattern)
	if err == nil {
		if len(files) > 0 {
			file = files[0]
		} else {
			err = fmt.Errorf(fmt.Sprintf("No files found in path \033[1m%[1]s\033[0m of pattern \033[1m%[2]s\033[0m.", path, filepattern))
		}
	}
	return file, err
}

/* ---------------------------------------------------------------- *
 * METHOD check path exists
 * ---------------------------------------------------------------- */

func CheckPathExists(path string) bool {
	_, err := os.Stat(path)
	return !os.IsNotExist(err)
}
