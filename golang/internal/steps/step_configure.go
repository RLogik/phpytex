package steps

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
	"phpytex/internal/setup"
	"phpytex/internal/setup/appconfig"
	"reflect"
	"strings"

	"gopkg.in/yaml.v3"
)

/* ---------------------------------------------------------------- *
 * METHOD configure
 * ---------------------------------------------------------------- */

func Configure(fnameConfig string) {
	var config *setup.UserConfig
	logging.LogInfo("READ CONFIG STARTED")
	// get configuration file
	config = &(setup.UserConfig{})
	getPhpytexConfig(fnameConfig, config)
	preProcessConfig(config)

	// set app config
	setCompileConfig(config.Compile)
	// setStampConfig(**toPythonKeysDict(config_stamp));
	// setParamsConfig(**toPythonKeysDict(config_parameters));
	// setConfigFilesAndFolders(toPythonKeysDict(config));

	logging.LogInfo("READ CONFIG COMPLETE")
}

/* ---------------------------------------------------------------- *
 * PRIVATE METHODS
 * ---------------------------------------------------------------- */

func getPhpytexConfig(fnameConfig string, config *setup.UserConfig) {
	var err error = nil
	var contents []byte
	for true {
		if fnameConfig == "" {
			fnameConfig, err = utils.GetFirstFileByPattern(appconfig.GetPathRoot(), appconfig.GetPatternConfig())
		}
		if err != nil {
			break
		}
		contents, err = ioutil.ReadFile(fnameConfig)
		if err != nil {
			break
		}
		err = yaml.Unmarshal(contents, config)
		if err != nil {
			break
		}
		break
	}
	if err != nil {
		logging.LogFatal(fmt.Sprintf("Could not read config file \033[1m%s\033[0mor its contents were invalid.", fnameConfig), err)
	}
	return
}

// cleans up structure to handle backwards compatibility
func preProcessConfig(config *setup.UserConfig) {
	// flatten [compile -> options] ~~> [compile]:
	if config.Compile.Options != nil {
		config.Compile = *((*config).Compile.Options)
		config.Compile.Options = nil
	}
	// [ignore] prioritise setting from: [header -> ignore], compile [option -> ignore]:
	if config.Compile.Ignore != nil && config.Header.Ignore == nil {
		config.Header.Ignore = utils.BoolToPtr(*config.Compile.Ignore)
		config.Header.Ignore = nil
	}
	// [root] can be either [root] or [input]:
	if config.Compile.Input != nil && config.Compile.Root == nil {
		config.Compile.Root = utils.StringToPtr(*config.Compile.Input)
		config.Compile.Input = nil
	}
	// [compile] can be either [compile] or [compile-latex]:
	if config.Compile.CompileLatex != nil && config.Compile.Compile == nil {
		config.Compile.Compile = utils.BoolToPtr(*config.Compile.CompileLatex)
		config.Compile.CompileLatex = nil
	}
	// [show-tree] can be either [show-tree] or [show-structure]:
	if config.Compile.ShowStructure != nil && config.Compile.ShowTree == nil {
		config.Compile.ShowTree = utils.BoolToPtr(*config.Compile.ShowStructure)
		config.Compile.ShowStructure = nil
	}
	// if [tree] option not used:
	if (config.Files != nil || config.Folders != nil) && config.Tree == nil {
		tree := setup.TreeConfig{
			Files:   nil,
			Folders: nil,
		}
		if config.Files != nil {
			tree.Files = &(*config.Files)
		}
		if config.Folders != nil {
			tree.Folders = &(*config.Folders)
		}
		config.Tree = &tree
		config.Files = nil
		config.Folders = nil
	}
}

func setCompileConfig(config setup.CompileConfig) {
	var err error
	var (
		comments    interface{}
		valueString string
		valueBool1  bool
		valueBool2  bool
	)
	var (
		indentSymb string
		spaces     int
	)
	var (
		fileStart  string
		fileOutput string
		file       string
	)

	root := appconfig.GetPathRoot()
	appconfig.SetOptionLegacy(config.Legacy)
	appconfig.SetOptionIgnore(config.Ignore)
	appconfig.SetOptionDebug(config.Debug)
	appconfig.SetOptionCompileLatex(config.Compile)
	appconfig.SetOptionInsertBib(config.InsertBib)
	appconfig.SetOptionShowTree(config.ShowTree)

	comments = *config.Comments
	if reflect.TypeOf(comments).Kind() == reflect.String {
		valueString = comments.(string)
		valueBool1 = utils.ArrayContains([]string{"auto", "default"}, valueString)
		valueBool2 = utils.ArrayContains([]string{"on", "default"}, valueString) || !utils.ArrayContains([]string{"off"}, valueString)
	} else if reflect.TypeOf(comments).Kind() == reflect.Bool {
		// NOTE: if boolean value used, then user wants all on or all off, thus [auto] = false
		valueBool1 = false
		valueBool2 = comments.(bool)
	} else {
		valueBool1 = true
		valueBool2 = true
	}
	appconfig.SetOptionCommentsAuto(utils.BoolToPtr(valueBool1))
	appconfig.SetOptionCommentsOn(utils.BoolToPtr(valueBool2))

	appconfig.SetMaxLength(config.MaxLength)
	appconfig.SetSeed(config.Seed)

	if utils.PtrToBool(config.Tabs, false) {
		appconfig.SetIndentCharacter(utils.StringToPtr("\t"))
		appconfig.SetIndentCharacterRe(utils.StringToPtr(`\t`))
	} else {
		spaces = utils.PtrToInt(config.Spaces, 4)
		indentSymb = strings.Repeat(" ", spaces)
		appconfig.SetIndentCharacter(utils.StringToPtr(indentSymb))
		appconfig.SetIndentCharacterRe(utils.StringToPtr(indentSymb))
	}
	indentSymb = appconfig.GetIndentCharacter()
	if utils.LengthOfWhiteSpace(indentSymb) == 0 {
		logging.LogFatal("Indentation symbol cannot be the empty string!")
	}

	appconfig.SetOffsetSymbol(config.Offset)
	if utils.PtrToBool(config.Legacy, false) && config.Offset == nil {
		appconfig.SetOffsetSymbol(utils.StringToPtr(indentSymb))
	}

	fileStart, err = utils.FormatPath(*config.Root, root, false)
	if err != nil {
		logging.LogFatal(fmt.Sprintf("Could not process input path \033[1m%[1]s\033[0m.", *config.Root))
	}
	fileOutput, err = utils.FormatPath(*config.Output, root, false, nil, utils.StringToPtr(".tex"))
	if err != nil {
		logging.LogFatal(fmt.Sprintf("Could not process output path \033[1m%[1]s\033[0m.", *config.Root))
	}
	if filepath.Dir(fileOutput) != root {
		logging.LogFatal("The output file can only be set to be in the root directory!'")
	}
	if fileStart == fileOutput {
		logging.LogFatal("The output and start ('root'-attribute in config) paths must be different!")
	}

	appconfig.SetFileStart(utils.StringToPtr(fileStart))
	appconfig.SetFileOutput(utils.StringToPtr(fileOutput))

	file, err = utils.FormatPath("phpytex_transpiled.py", root, false)
	if err != nil {
		logging.LogFatal(err)
	}
	appconfig.SetFileTranspiled(utils.StringToPtr(file))
	return
}
