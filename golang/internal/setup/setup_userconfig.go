package setup

import "phpytex/internal/core/utils"

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * YAML SCHEMES
 * ---------------------------------------------------------------- */

type HeaderConfig struct {
	Ignore *bool `yaml:"ignore"`
}

type CompileConfig struct {
	Root      *string      `yaml:"root"`
	Output    *string      `yaml:"output"`
	Debug     *bool        `yaml:"debug"`
	Compile   *bool        `yaml:"compile"`
	InsertBib *bool        `yaml:"insert-bib"`
	Comments  *interface{} `yaml:"comments"`
	ShowTree  *bool        `yaml:"show-tree"`
	MaxLength *int         `yaml:"max-length"`
	Tabs      *bool        `yaml:"tabs"`
	Spaces    *int         `yaml:"spaces"`
	Seed      *int         `yaml:"seed"`
	Offset    *string      `yaml:"offset"`
	// can be optionally placed here or at level 0 of the yaml file:
	Ignore *bool `yaml:"ignore"`
	// need the following for backwards compatibility:
	Legacy        *bool          `yaml:"legacy"`
	Input         *string        `yaml:"input"`
	CompileLatex  *bool          `yaml:"compile-latex"`
	ShowStructure *bool          `yaml:"show-structure"`
	Options       *CompileConfig `yaml:"options"`
}

type SpecialFileConfig struct {
	File      *string                   `yaml:"file"`
	Overwrite *bool                     `yaml:"overwrite"`
	Options   *(map[string]interface{}) `yaml:"options"`
}

type TreeConfig struct {
	Files   *([]string)                 `yaml:"files"`
	Folders *(map[string](*TreeConfig)) `yaml:"folders"`
}

type UserConfig struct {
	Header     HeaderConfig
	Compile    CompileConfig     `yaml:"compile"`
	Stamp      SpecialFileConfig `yaml:"stamp"`
	Parameters SpecialFileConfig `yaml:"parameters"`
	Tree       *TreeConfig       `yaml:"tree"`
	// need the following for backwards compatibility:
	Files   *([]string)                 `yaml:"files"`
	Folders *(map[string](*TreeConfig)) `yaml:"folders"`
}

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
	Ignore:    utils.BoolToPtr(false),
	Output:    utils.StringToPtr("main.tex"),
	Debug:     utils.BoolToPtr(false),
	Compile:   utils.BoolToPtr(false),
	InsertBib: utils.BoolToPtr(false),
	Comments:  utils.InterfaceToPtr("auto"),
	ShowTree:  utils.BoolToPtr(true),
	MaxLength: utils.IntToPtr(10000),
	Tabs:      utils.BoolToPtr(false),
	Spaces:    utils.IntToPtr(4),
}

var DefaultPhpytexConfig = UserConfig{
	Header:     HeaderConfig{},
	Compile:    DefaultCompileConfig,
	Stamp:      SpecialFileConfig{},
	Parameters: SpecialFileConfig{},
	Tree:       &TreeConfig{},
}
