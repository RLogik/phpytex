package types

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"encoding/json"
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
		"Ignore":    BoolPtr(config.Ignore),
		"Root":      StringPtr(config.Root),
		"Output":    StringPtr(config.Output),
		"Debug":     BoolPtr(config.Debug),
		"Compile":   BoolPtr(config.Compile),
		"InsertBib": BoolPtr(config.InsertBib),
		"Comments":  InterfacePtr(config.Comments),
		"ShowTree":  BoolPtr(config.ShowTree),
		"MaxLength": IntPtr(config.MaxLength),
		"Tabs":      BoolPtr(config.Tabs),
		"Spaces":    IntPtr(config.Spaces),
		"Seed":      IntPtr(config.Seed),
		"Offset":    StringPtr(config.Offset),
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
		"File":      StringPtr(config.File),
		"Overwrite": BoolPtr(config.Overwrite),
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
		"File":      StringPtr(config.File),
		"Overwrite": BoolPtr(config.Overwrite),
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
