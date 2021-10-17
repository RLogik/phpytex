package userconfig

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * DEFAULTS
 * ---------------------------------------------------------------- */

var DefaultHeaderConfig = HeaderConfig{
	Ignore: utils.BoolToPtr(false),
}

var DefaultTreeConfig = TreeConfig{
	Files:   &([]string{}),
	Folders: &(map[string](*TreeConfig){}),
}

var DefaultCompileConfig = CompileConfig{
	Ignore:   utils.BoolToPtr(false),
	Comments: utils.InterfaceToPtr("auto"),
	Tabs:     utils.BoolToPtr(false),
	Spaces:   utils.IntToPtr(4),
	Legacy:   utils.BoolToPtr(false),
	// NOTE: do not provide default offset, as need to check if user does not set this
}

var DefaultStampConfig = StampFileConfig{
	Overwrite: utils.BoolToPtr(true),
	File:      utils.StringToPtr("stamp.tex"),
}

var DefaultParametersConfig = ParametersFileConfig{
	Overwrite: utils.BoolToPtr(true),
}

var DefaultUserConfig = UserConfig{
	Header:     &DefaultHeaderConfig,
	Compile:    &DefaultCompileConfig,
	Stamp:      &DefaultStampConfig,
	Parameters: &DefaultParametersConfig,
	Tree:       &TreeConfig{},
}
