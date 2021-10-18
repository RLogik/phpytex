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
	"phpytex/internal/setup/userconfig"
)

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func Create() error {
	var err error = nil
	logging.LogInfo("CREATION STAGE STARTED.")
	var root string = appconfig.Parameters.PathRoot.GetValue()
	createFilesAndFolders(root, appconfig.Parameters.ProjectTree)
	if appconfig.Parameters.WithFileStamp.GetValue() {
		createFileStamp(
			appconfig.Parameters.FileStamp.GetValue(false),
			appconfig.Parameters.OptionOverwriteStamp.GetValue(),
			appconfig.Parameters.DictionaryStamp,
		)
	}
	if appconfig.Parameters.WithFileParamsPy.GetValue() {
		// createParameters(appconfig.Parameters.DictionaryParams.GetValue());
	}
	logging.LogInfo("CREATION STAGE COMPLETE.")
	return err
}

/* ---------------------------------------------------------------- *
 * SECONDARY METHODS
 * ---------------------------------------------------------------- */

func createFilesAndFolders(path string, projectTree *userconfig.TreeConfig) error {
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
		lines  string
		border string
	)

	lines, err = utils.DisplayMapAsStamp(*options, "%% ", "  ", false, true, false, false)

	if err != nil {
		return err
	}

	if len(lines) > 0 {
		border = "%% " + strings.Repeat(`*`, 80)
		lines = strings.Join([]string{border, lines, border}, "\n")
	}
	err = utils.WriteTextFile(path, lines)

	return err
}

// func createFileParameters(
//     path: str,
//     overwrite: bool,
//     options: Dict[str, Any]
// ) {
//     if os.path.exists(path) and not overwrite:
//         return;
//     appconfig.setExportVars({});
//     lines = [];
//     for key, value in options.items():
//         try:
//             typ, codedvalue = convertToPythonString(value, indent=0, multiline=False);
//             appconfig.setExportVarsKeyValue(key=key, value=value, codedvalue=codedvalue);
//             lines.append('<<< global set {key} = {value}; >>>'.format(key = key, value = codedvalue));
//         except:
//             continue;
//     if os.path.isfile(path) and not overwrite:
//         return;
//     writeTextFile(path=path, lines=lines);
// }

// func createParameters(options: Dict[str, Any]) {
//     appconfig.setExportVars({});
//     lines = [];
//     for key, value in options.items():
//         try:
//             typ, codedvalue = convertToPythonString(value, indent=0, multiline=False);
//             appconfig.setExportVarsKeyValue(key=key, value=value, codedvalue=codedvalue);
//         except:
//             continue;
// }

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
