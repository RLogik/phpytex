package appconfig

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"encoding/json"
)

/* ---------------------------------------------------------------- *
 * METHODS serialisation of basic types
 * ---------------------------------------------------------------- */

func (c *ConfigString) Serialise() interface{} {
	if c == nil || c.value == nil {
		return nil
	}
	return *(c.value)
}

func (c *ConfigBool) Serialise() interface{} {
	if c == nil || c.value == nil {
		return nil
	}
	return *(c.value)
}

func (c *ConfigInt) Serialise() interface{} {
	if c == nil || c.value == nil {
		return nil
	}
	return *(c.value)
}

func (c *ConfigPath) Serialise() interface{} {
	if c == nil || c.value == nil {
		return nil
	}
	return *(c.value)
}

func (c *ConfigFile) Serialise() interface{} {
	if c == nil || c.value == nil {
		return nil
	}
	return *(c.value)
}

/* ---------------------------------------------------------------- *
 * METHOD serialisation of app config
 * ---------------------------------------------------------------- */

func (config *AppConfig) String() string {
	var object = config.Serialise()
	coded, _ := json.Marshal(object)
	return string(coded)
}

func (config *AppConfig) Serialise() interface{} {
	return map[string]interface{}{
		"PatternConfig":         config.PatternConfig.Serialise(),
		"PathRoot":              config.PathRoot.Serialise(),
		"FileStart":             config.FileStart.Serialise(),
		"FileTranspiled":        config.FileTranspiled.Serialise(),
		"FileOutput":            config.FileOutput.Serialise(),
		"WithFileStamp":         config.WithFileStamp.Serialise(),
		"FileStamp":             config.FileStamp.Serialise(),
		"WithFileParamsPy":      config.WithFileParamsPy.Serialise(),
		"FileParamsPy":          config.FileParamsPy.Serialise(),
		"ImportParamsPy":        config.ImportParamsPy.Serialise(),
		"ParamModuleName":       config.ParamModuleName.Serialise(),
		"PythonPath":            config.PythonPath.Serialise(),
		"IndentCharacter":       config.IndentCharacter.Serialise(),
		"IndentCharacterRe":     config.IndentCharacterRe.Serialise(),
		"CensorSymbol":          config.CensorSymbol.Serialise(),
		"OptionLegacy":          config.OptionLegacy.Serialise(),
		"OptionIgnore":          config.OptionIgnore.Serialise(),
		"OptionDebug":           config.OptionDebug.Serialise(),
		"OptionCompileLatex":    config.OptionCompileLatex.Serialise(),
		"OptionShowTree":        config.OptionShowTree.Serialise(),
		"OptionCommentsAuto":    config.OptionCommentsAuto.Serialise(),
		"OptionCommentsOn":      config.OptionCommentsOn.Serialise(),
		"OptionInsertBib":       config.OptionInsertBib.Serialise(),
		"MaxLength":             config.MaxLength.Serialise(),
		"Seed":                  config.Seed.Serialise(),
		"Offset":                config.Offset.Serialise(),
		"OptionOverwriteStamp":  config.OptionOverwriteStamp.Serialise(),
		"OptionOverwriteParams": config.OptionOverwriteParams.Serialise(),
	}
}
