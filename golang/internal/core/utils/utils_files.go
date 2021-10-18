package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"io/fs"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"

	"phpytex/pkg/re"
)

/* ---------------------------------------------------------------- *
 * METHOD working directory
 * ---------------------------------------------------------------- */

func GetCwd() (string, error) {
	var cwd string
	var err error
	cwd, err = os.Getwd()
	if err == nil {
		cwd, err = filepath.Abs(cwd)
	}
	return cwd, err
}

/* ---------------------------------------------------------------- *
 * METHOD get files by pattern
 * ---------------------------------------------------------------- */

func GetFilesByPattern(path string, filepattern string) ([]string, error) {
	var err error
	var files []fs.FileInfo
	files_filtered := []string{}
	files, err = ioutil.ReadDir(path)
	if err != nil {
		return []string{}, err
	}
	for _, file := range files {
		fname := file.Name()
		if re.Matches(filepattern, fname) {
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

func IsFile(path string) bool {
	mode, err := os.Stat(path)
	return err == nil && !mode.Mode().IsRegular()
}

func IsDir(path string) bool {
	mode, err := os.Stat(path)
	return err == nil && mode.Mode().IsDir()
}

/* ---------------------------------------------------------------- *
 * METHOD format path
 * ---------------------------------------------------------------- */

func FormatPath(path string, root string, rel bool, options ...*string) (string, error) {
	var err error
	var (
		ext          *string = nil
		ext_if_empty *string = nil
	)
	var (
		ext_  string
		path_ string
	)
	if len(options) > 0 {
		ext = options[0]
	}
	if len(options) > 1 {
		ext_if_empty = options[1]
	}
	if filepath.IsAbs(path) {
		if rel {
			path, err = filepath.Rel(root, path)
		}
	} else {
		if !rel {
			path, err = filepath.Abs(filepath.Join(root, path))
		}
	}
	if err == nil {
		ext_ = filepath.Ext(path)
		path_ = path[:len(path)-len(ext_)]
		if ext != nil {
			path = fmt.Sprintf("%[1]s%[2]s", path_, *ext)
		} else if ext_if_empty != nil && ext_ == "" {
			path = fmt.Sprintf("%[1]s%[2]s", path_, *ext_if_empty)
		}
	}
	return path, err
}

/* ---------------------------------------------------------------- *
 * METHOD create paths/files
 * ---------------------------------------------------------------- */

func CreatePath(path string) error {
	var err error = nil
	cwd, _ := GetCwd()
	if path == cwd || path == "" || path == "." {
		return nil
	}
	if !CheckPathExists(path) {
		err = os.Mkdir(path, 0644)
	}
	if err != nil || !CheckPathExists(path) {
		return fmt.Errorf("Could not create or find path \033[93;1m%[1]s\033[0m!", path)
	}
	return nil
}

func CreateFile(path string) error {
	var err error = nil
	cwd, _ := GetCwd()
	if path == cwd || path == "" || path == "." {
		return nil
	}
	if !CheckPathExists(path) {
		// pathlib.Path(path).mkdir(parents=True, exist_ok=True);
		_, err = os.Create(path)
	}
	if err != nil || !CheckPathExists(path) {
		return fmt.Errorf("Could not create or find file \033[93;1m%[1]s\033[0m!", path)
	}
	return nil
}

func WriteTextFile(path string, text string, options ...bool) error {
	var err error
	var forceCreatePath bool = GetArrayBoolValue(&options, 0, false)
	var forceCreateEmptyLine bool = GetArrayBoolValue(&options, 1, true)
	var (
		lines []string
		line  string
		index int
	)

	if forceCreatePath {
		err = CreatePath(filepath.Dir(path))
		if err != nil {
			return err
		}
	}

	// deal with trailing lines
	lines = re.Split(`\n`, text)
	index = len(lines) - 1
	for index > 0 {
		line = strings.TrimSpace(lines[index])
		if line != "" {
			break
		}
		lines = lines[:index]
		index--
	}
	if forceCreateEmptyLine {
		lines = append(lines, "")
	}
	text = strings.Join(lines, "\n")

	err = os.WriteFile(path, []byte(text), 0666)

	return err
}
