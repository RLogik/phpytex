package userconfig

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"phpytex/internal/types"
)

/* ---------------------------------------------------------------- *
 * DEFAULTS
 * ---------------------------------------------------------------- */

var DefaultHeaderConfig = types.HeaderConfig{
	Ignore: types.BoolToPtr(false),
}

var DefaultTreeConfig = types.TreeConfig{
	Files:   &([]string{}),
	Folders: &(map[string](*types.TreeConfig){}),
}

var DefaultCompileConfig = types.CompileConfig{
	Ignore:   types.BoolToPtr(false),
	Comments: types.InterfaceToPtr("auto"),
	Tabs:     types.BoolToPtr(false),
	Spaces:   types.IntToPtr(4),
	Legacy:   types.BoolToPtr(false),
	// NOTE: do not provide default offset, as need to check if user does not set this
}

var DefaultStampConfig = types.StampFileConfig{
	Overwrite: types.BoolToPtr(true),
	File:      types.StringToPtr("stamp.tex"),
}

var DefaultParametersConfig = types.ParametersFileConfig{
	Overwrite: types.BoolToPtr(true),
}

var DefaultUserConfig = types.UserConfig{
	Header:     &DefaultHeaderConfig,
	Compile:    &DefaultCompileConfig,
	Stamp:      &DefaultStampConfig,
	Parameters: &DefaultParametersConfig,
	Tree:       &DefaultTreeConfig,
	// Tree:       &types.TreeConfig{},
}
