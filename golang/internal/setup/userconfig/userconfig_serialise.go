package userconfig

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"encoding/json"
	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * METHODS serialisation
 * ---------------------------------------------------------------- */

func (config *UserConfig) String() string {
	var object = config.Serialise()
	coded, _ := json.Marshal(object)
	return string(coded)
}

func (config *UserConfig) Serialise() interface{} {
	if config == nil {
		return nil
	}
	var result = map[string]interface{}{
		"Header":     config.Header.Serialise(),
		"Compile":    config.Compile.Serialise(),
		"Stamp":      config.Stamp.Serialise(),
		"Parameters": config.Parameters.Serialise(),
		"Tree":       config.Tree.Serialise(),
	}
	return result
}

func (config *HeaderConfig) Serialise() interface{} {
	if config == nil {
		return nil
	}
	var result = map[string]interface{}{
		"Ignore": nil,
	}
	if config.Ignore != nil {
		result["Ignore"] = *config.Ignore
	}
	return result
}

func (config *CompileConfig) Serialise() interface{} {
	if config == nil {
		return nil
	}
	return map[string]interface{}{
		"Ignore":    utils.SerialiseBoolPtr(config.Ignore),
		"Root":      utils.SerialiseStringPtr(config.Root),
		"Output":    utils.SerialiseStringPtr(config.Output),
		"Debug":     utils.SerialiseBoolPtr(config.Debug),
		"Compile":   utils.SerialiseBoolPtr(config.Compile),
		"InsertBib": utils.SerialiseBoolPtr(config.InsertBib),
		"Comments":  utils.SerialiseInterfacePtr(config.Comments),
		"ShowTree":  utils.SerialiseBoolPtr(config.ShowTree),
		"MaxLength": utils.SerialiseIntPtr(config.MaxLength),
		"Tabs":      utils.SerialiseBoolPtr(config.Tabs),
		"Spaces":    utils.SerialiseIntPtr(config.Spaces),
		"Seed":      utils.SerialiseIntPtr(config.Seed),
		"Offset":    utils.SerialiseStringPtr(config.Offset),
	}
}

func (config *StampFileConfig) Serialise() interface{} {
	if config == nil {
		return nil
	}
	var options interface{} = nil
	if config.Options != nil {
		options = *config.Options
	}
	return map[string]interface{}{
		"File":      utils.SerialiseStringPtr(config.File),
		"Overwrite": utils.SerialiseBoolPtr(config.Overwrite),
		"Options":   options,
	}
}

func (config *ParametersFileConfig) Serialise() interface{} {
	if config == nil {
		return nil
	}
	var options interface{} = nil
	if config.Options != nil {
		options = *config.Options
	}
	return map[string]interface{}{
		"File":      utils.SerialiseStringPtr(config.File),
		"Overwrite": utils.SerialiseBoolPtr(config.Overwrite),
		"Options":   options,
	}
}

func (config *TreeConfig) Serialise() interface{} {
	if config == nil {
		return nil
	}
	var files interface{} = nil
	var folders interface{} = nil
	if config.Files != nil {
		files = *config.Files
	}
	if config.Folders != nil {
		folders := map[string]interface{}{}
		for key, value := range *config.Folders {
			folders[key] = value.Serialise()
		}
	}
	return map[string]interface{}{
		"Files":   files,
		"Folders": folders,
	}
}
