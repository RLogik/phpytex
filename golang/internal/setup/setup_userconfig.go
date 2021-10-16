package setup

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * YAML SCHEMES
 * ---------------------------------------------------------------- */

type HeaderConfig struct {
	Ignore bool `yaml:"ignore"`
}

type CompileConfig struct {
	Root      string      `yaml:"root"`
	Output    string      `yaml:"output"`
	Debug     bool        `yaml:"debug"`
	Compile   bool        `yaml:"compile"`
	InsertBib bool        `yaml:"insert-bib"`
	Comments  interface{} `yaml:"comments"`
	ShowTree  bool        `yaml:"show-tree"`
	MaxLength int         `yaml:"max-length"`
	Tabs      bool        `yaml:"tabs"`
	Spaces    int         `yaml:"spaces"`
	Seed      int         `yaml:"seed"`
	// can be optionally placed here or at level 0 of the yaml file:
	Ignore bool `yaml:"ignore"`
	// need the following for backwards compatibility:
	Input         string         `yaml:"input"`
	CompileLatex  bool           `yaml:"compile-latex"`
	ShowStructure bool           `yaml:"show-structure"`
	Options       *CompileConfig `yaml:"options"`
}

type SpecialFileConfig struct {
	File      string                    `yaml:"file"`
	Overwrite bool                      `yaml:"overwrite"`
	Options   *(map[string]interface{}) `yaml:"options"`
}

type TreeConfig struct {
	Files   *([]string)                 `yaml:"files"`
	Folders *(map[string](*TreeConfig)) `yaml:"folders"`
}

type PhpytexConfig struct {
	Header     HeaderConfig
	Compile    CompileConfig     `yaml:"compile"`
	Stamp      SpecialFileConfig `yaml:"stamp"`
	Parameters SpecialFileConfig `yaml:"parameters"`
	Tree       TreeConfig        `yaml:"tree"`
	// need the following for backwards compatibility:
	Files   *([]string)                 `yaml:"files"`
	Folders *(map[string](*TreeConfig)) `yaml:"folders"`
}

/* ---------------------------------------------------------------- *
 * DEFAULTS
 * ---------------------------------------------------------------- */

var DefaultHeaderConfig = HeaderConfig{}
var DefaultCompileConfig = CompileConfig{
	Ignore:    false,
	Output:    "main.tex",
	Debug:     false,
	Compile:   false,
	InsertBib: false,
	Comments:  "auto",
	ShowTree:  true,
	MaxLength: 10000,
	Tabs:      false,
	Spaces:    4,
	// can be optionally placed here or at level 0 of the yaml file:
	// need the following for backwards compatibility:
	CompileLatex:  false,
	ShowStructure: true,
	Options:       nil,
}
var DefaultPhpytexConfig = PhpytexConfig{
	Header:     HeaderConfig{},
	Compile:    DefaultCompileConfig,
	Stamp:      SpecialFileConfig{},
	Parameters: SpecialFileConfig{},
	Tree:       TreeConfig{},
	Files:      nil,
	Folders:    nil,
}
