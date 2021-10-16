package steps

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"io/ioutil"
	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
	"phpytex/internal/setup"
	"phpytex/internal/setup/appconfig"

	"gopkg.in/yaml.v3"
)

/* ---------------------------------------------------------------- *
 * METHOD configure
 * ---------------------------------------------------------------- */

func Configure(fnameConfig string) {
	logging.LogInfo("READ CONFIG STARTED")
	// get configuration file
	config := getPhpytexConfig(fnameConfig)
	// // get main parts of config
	// config_compile = getAttribute(config, 'compile', 'options', expectedtype=dict, default=None) \
	// 				 or getAttribute(config, 'compile', expectedtype=dict, default={});
	// config_compile = preProcessCompileConfig({ **restrictDictionary(config, ['ignore']), **config_compile });
	// config_stamp = getAttribute(config, 'stamp', expectedtype=dict, default={});
	// config_parameters = getAttribute(config, 'parameters', expectedtype=dict, default={});

	//// set app config
	// setCompileConfig(**config_compile);
	// setStampConfig(**toPythonKeysDict(config_stamp));
	// setParamsConfig(**toPythonKeysDict(config_parameters));
	// setConfigFilesAndFolders(toPythonKeysDict(config));

	logging.LogInfo("READ CONFIG COMPLETE")
}

/* ---------------------------------------------------------------- *
 * PRIVATE METHODS
 * ---------------------------------------------------------------- */

func getPhpytexConfig(fnameConfig string) setup.PhpytexConfig {
	var err error = nil
	var config setup.PhpytexConfig
	var contents []byte
	config = setup.DefaultPhpytexConfig

	if fnameConfig == "" {
		config_files := utils.GetFilesByPattern(appconfig.GetPathRoot(), appconfig.GetPatternConfig())
		if len(config_files) == 0 {
			logging.LogFatal("Could not find or read any phpytex configuration files.")
		}
		fnameConfig = config_files[0]
	}
	for true {
		contents, err = ioutil.ReadFile(fnameConfig)
		if err != nil {
			break
		}
		err = yaml.Unmarshal(contents, &config)
		if err != nil {
			break
		}
		break
	}
	if err != nil {
		logging.LogFatal(fmt.Sprintf("Could not read config file \033[1m%s\033[0mor its contents were invalid.", fnameConfig), err)
	}
	return config
}
