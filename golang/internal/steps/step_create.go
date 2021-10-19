package steps

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"fmt"
	"path/filepath"
	"strings"

	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
	"phpytex/internal/setup/appconfig"
	"phpytex/internal/types"
)

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func Create() error {
	var err error = nil
	logging.LogInfo("CREATION STAGE STARTED.")
	var root string = appconfig.Parameters.PathRoot.GetValue()
	createFilesAndFolders(root, appconfig.ProjectTree)
	if appconfig.Parameters.WithFileStamp.GetValue() {
		err = createFileStamp(
			appconfig.Parameters.FileStamp.GetValue(false),
			appconfig.Parameters.OptionOverwriteStamp.GetValue(),
			appconfig.DictionaryStamp.GetValues(),
		)
	}
	if err != nil {
		return err
	}
	if appconfig.Parameters.WithFileParamsPy.GetValue() {
		err = createParameters(appconfig.DictionaryParams.GetValues())
	}
	if err != nil {
		return err
	}
	logging.LogInfo("CREATION STAGE COMPLETE.")
	return nil
}

/* ---------------------------------------------------------------- *
 * SECONDARY METHODS
 * ---------------------------------------------------------------- */

func createFilesAndFolders(path string, projectTree *types.TreeConfig) error {
	if projectTree == nil {
		return nil
	}
	if projectTree.Files != nil {
		for _, fname := range *projectTree.Files {
			err := makeFileIfNotExists(path, fname)
			if err != nil {
				return err
			}
		}
	}
	if projectTree.Folders != nil {
		for relpath, _ := range *projectTree.Folders {
			err := makeDirIfNotExists(path, relpath)
			if err != nil {
				return err
			}
		}
		for relpath, tree := range *projectTree.Folders {
			createFilesAndFolders(filepath.Join(path, relpath), tree)
		}
	}
	return nil
}

func createFileStamp(path string, overwrite bool, options *map[string]interface{}) error {
	if (utils.CheckPathExists(path) && !overwrite) || options == nil {
		return nil
	}

	var (
		err    error
		text   string
		border string
	)

	text, err = utils.DisplayMapAsStamp(*options, "%% ", "  ", false, true, false, false)

	if err != nil {
		return err
	}

	if len(text) > 0 {
		border = "%% " + strings.Repeat(`*`, 80)
		text = strings.Join([]string{border, text, border}, "\n")
	}
	err = utils.WriteTextFile(path, text)

	return err
}

func createFileParameters(path string, overwrite bool, options *map[string]interface{}) error {
	if (utils.CheckPathExists(path) && !overwrite) || options == nil {
		return nil
	}
	var (
		err        error
		lines      []string
		line       string
		text       string
		key        string
		value      interface{}
		codedvalue string
	)

	appconfig.ExportVariables.Init()
	lines = []string{}
	for key, value = range *options {
		codedvalue, err = utils.ConvertToPythonString(value, 0, false, "    ")
		if err != nil {
			break
		}
		appconfig.ExportVariables.SetValue(key, []interface{}{value, codedvalue})
		line = fmt.Sprintf(`<<< global set %[1]s = %[2]v; >>>`, key, codedvalue)
		lines = append(lines, line)
	}
	text = strings.Join(lines, "\n")

	err = utils.WriteTextFile(path, text)

	return err
}

func createParameters(options *map[string]interface{}) error {
	if options == nil {
		return nil
	}
	var (
		err        error
		key        string
		value      interface{}
		codedvalue string
	)

	appconfig.ExportVariables.Init()
	for key, value = range *options {
		codedvalue, err = utils.ConvertToPythonString(value, 0, true, "    ")
		if err != nil {
			break
		}
		appconfig.ExportVariables.SetValue(key, []interface{}{value, codedvalue})
	}

	return err
}

/* ---------------------------------------------------------------- *
 * TERTIARY METHODS
 * ---------------------------------------------------------------- */

func makeFileIfNotExists(path string, fname string) error {
	var err error = nil
	var pathFull string
	pathFull = filepath.Join(path, fname)
	if utils.CheckPathExists(pathFull) {
		if !utils.IsFile(pathFull) {
			return fmt.Errorf("The path \033[96;1m%[1]s\033[0m already exists and cannot be made into a file.", pathFull)
		}
	} else {
		logging.LogInfo(fmt.Sprintf("File \033[96;1m%[1]s\033[0m will be created.", fname))
		err = utils.CreatePath(pathFull)
	}
	return err
}

func makeDirIfNotExists(path string, relpath string) error {
	var err error = nil
	var pathFull string
	pathFull = filepath.Join(path, relpath)
	if utils.CheckPathExists(pathFull) {
		if !utils.IsDir(pathFull) {
			return fmt.Errorf("The path \033[96;1m%[1]s\033[0m already exists and cannot be made into a directory.", pathFull)
		}
	} else {
		logging.LogInfo(fmt.Sprintf("Folder \033[96;1m%[1]s\033[0m will be created.", relpath))
		err = utils.CreatePath(pathFull)
	}
	return err
}
