package steps

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
	"reflect"
	"strings"

	"gopkg.in/yaml.v3"

	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
	"phpytex/internal/setup/appconfig"
	"phpytex/internal/setup/userconfig"
	"phpytex/pkg/re"
)

/* ---------------------------------------------------------------- *
 * METHOD configure
 * ---------------------------------------------------------------- */

func Configure(fnameConfig string) error {
	var err error
	var config = &(userconfig.UserConfig{})

	logging.LogInfo("READ CONFIG STARTED")

	err = getUserConfig(fnameConfig, config)
	if err != nil {
		return fmt.Errorf(fmt.Sprintf("Could not read config file \033[1m%s\033[0mor its contents were invalid.", fnameConfig))
	}

	err = setHeaderConfig(config.Header)
	if err != nil {
		return err
	}

	err = setCompileConfig(config.Compile)
	if err != nil {
		return err
	}

	err = setStampConfig(config.Stamp)
	if err != nil {
		return err
	}

	err = setParamsConfig(config.Parameters)
	if err != nil {
		return err
	}

	setConfigFilesAndFolders(config.Tree)

	logging.LogInfo("READ CONFIG COMPLETE")
	return nil
}

/* ---------------------------------------------------------------- *
 * PRIVATE METHODS
 * ---------------------------------------------------------------- */

func getUserConfig(fnameConfig string, config *userconfig.UserConfig) error {
	var err error
	var contents []byte
	if fnameConfig == "" {
		fnameConfig, err = utils.GetFirstFileByPattern(appconfig.Parameters.PathRoot.GetValue(), appconfig.Parameters.PatternConfig.GetValue())
	}
	if err != nil {
		return err
	}
	contents, err = ioutil.ReadFile(fnameConfig)
	if err != nil {
		return err
	}
	err = yaml.Unmarshal(contents, config)
	if err != nil {
		return err
	}
	userconfig.HandleMissingSections(config)
	userconfig.HandleBackwardsCompatibility(config)
	userconfig.HandleMissingKeys(config)
	return nil
}

func setHeaderConfig(config *userconfig.HeaderConfig) error {
	appconfig.Parameters.OptionIgnore.SetValueFromPtr(config.Ignore)
	return nil
}

func setCompileConfig(config *userconfig.CompileConfig) error {
	var err error = nil
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
		root       string
		fileStart  string
		fileOutput string
		file       string
	)

	appconfig.Parameters.OptionLegacy.SetValueFromPtr(config.Legacy)
	appconfig.Parameters.OptionDebug.SetValueFromPtr(config.Debug)
	appconfig.Parameters.OptionCompileLatex.SetValueFromPtr(config.Compile)
	appconfig.Parameters.OptionInsertBib.SetValueFromPtr(config.InsertBib)
	appconfig.Parameters.OptionShowTree.SetValueFromPtr(config.ShowTree)

	comments = *config.Comments
	if reflect.TypeOf(comments).Kind() == reflect.String {
		valueString = comments.(string)
		valueBool1 = re.Matches(`(?i)(^(auto|default)$)`, valueString)
		valueBool2 = re.Matches(`(?i)(^(on|default)$)`, valueString) || !re.Matches(`(?i)(^(|off)$)`, valueString)
	} else if reflect.TypeOf(comments).Kind() == reflect.Bool {
		// NOTE: if boolean value used, then user wants all on or all off, thus [auto] = false
		valueBool1 = false
		valueBool2 = comments.(bool)
	} else {
		valueBool1 = true
		valueBool2 = true
	}
	appconfig.Parameters.OptionCommentsAuto.SetValue(valueBool1)
	appconfig.Parameters.OptionCommentsOn.SetValue(valueBool2)

	appconfig.Parameters.MaxLength.SetValueFromPtr(config.MaxLength)
	appconfig.Parameters.Seed.SetValueFromPtr(config.Seed)

	if *config.Tabs {
		appconfig.Parameters.IndentCharacter.SetValue("\t")
		appconfig.Parameters.IndentCharacterRe.SetValue(`\t`)
	} else {
		spaces = *config.Spaces
		indentSymb = strings.Repeat(" ", spaces)
		appconfig.Parameters.IndentCharacter.SetValue(indentSymb)
		appconfig.Parameters.IndentCharacterRe.SetValue(indentSymb)
	}
	indentSymb = appconfig.Parameters.IndentCharacter.GetValue()
	if utils.LengthOfWhiteSpace(indentSymb) == 0 {
		return fmt.Errorf("Indentation symbol cannot be the empty string!")
	}

	appconfig.Parameters.Offset.SetValueFromPtr(config.Offset)
	if *config.Legacy && config.Offset == nil {
		appconfig.Parameters.Offset.SetValue(indentSymb)
	}

	root = appconfig.Parameters.PathRoot.GetValue()
	fileStart, err = utils.FormatPath(*config.Root, root, false)
	if err != nil {
		return fmt.Errorf(fmt.Sprintf("Could not process input path \033[1m%[1]s\033[0m.", *config.Root))
	}
	fileOutput, err = utils.FormatPath(*config.Output, root, false, nil, utils.StringToPtr(".tex"))
	if err != nil {
		return fmt.Errorf(fmt.Sprintf("Could not process output path \033[1m%[1]s\033[0m.", *config.Root))
	}
	if filepath.Dir(fileOutput) != root {
		return fmt.Errorf("The output file can only be set to be in the root directory!'")
	}
	if fileStart == fileOutput {
		return fmt.Errorf("The output and start ('root'-attribute in config) paths must be different!")
	}

	appconfig.Parameters.FileStart.SetValue(fileStart)
	appconfig.Parameters.FileOutput.SetValue(fileOutput)

	file, err = utils.FormatPath("phpytex_transpiled.py", root, false)
	if err != nil {
		return err
	}
	appconfig.Parameters.FileTranspiled.SetValue(file)
	return nil
}

func setStampConfig(config *userconfig.StampFileConfig) error {
	var err error = nil
	var (
		root string
		file string
	)

	appconfig.Parameters.WithFileStamp.SetValue(false)
	if config != nil && config.Options != nil && len(*config.Options) != 0 {
		root = appconfig.Parameters.PathRoot.GetValue()
		file = *config.File
		file, err = utils.FormatPath(file, root, false)
		if err != nil {
			return err
		}
		appconfig.Parameters.WithFileStamp.SetValue(true)
		appconfig.Parameters.FileStamp.SetValue(file)
		appconfig.Parameters.OptionOverwriteStamp.SetValueFromPtr(config.Overwrite)
		appconfig.DictionaryStamp.SetValues(config.Options)
	}
	return err
}

func setParamsConfig(config *userconfig.ParametersFileConfig) error {
	var err error = nil
	var (
		root string
	)
	var (
		modulename string
		path       string
	)

	appconfig.Parameters.WithFileParamsPy.SetValue(false)
	appconfig.Parameters.OptionOverwriteParams.SetValueFromPtr(config.Overwrite)
	appconfig.DictionaryParams.SetValues(config.Options)

	root = appconfig.Parameters.PathRoot.GetValue()
	if config != nil && config.Options != nil && len(*config.Options) != 0 {
		modulename = utils.PtrToString(config.File, "")
		if re.Matches(`^[^\.\s]*(\.[^\.\s]*)+$`, modulename) {
			path = re.Sub(`([^\.]+)\.`, `$1/`, modulename)
			path = path + ".py"
		} else {
			return fmt.Errorf("\033[1mparameters > file\033[0m option must by a python-like import path (relative to the root of the project).")
		}
		appconfig.Parameters.WithFileParamsPy.SetValue(true)
		appconfig.Parameters.ImportParamsPy.SetValue(modulename)
		path, err = utils.FormatPath(path, root, false)
		if err != nil {
			return err
		}
		appconfig.Parameters.FileParamsPy.SetValue(path)
	}

	return err
}

func setConfigFilesAndFolders(config *userconfig.TreeConfig) {
	appconfig.ProjectTree = config
}
