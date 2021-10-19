package types

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

type StampFileConfig SpecialFileConfig
type ParametersFileConfig SpecialFileConfig

type TreeConfig struct {
	Files   *([]string)                 `yaml:"files"`
	Folders *(map[string](*TreeConfig)) `yaml:"folders"`
}

type UserConfig struct {
	Header     *HeaderConfig
	Compile    *CompileConfig        `yaml:"compile"`
	Stamp      *StampFileConfig      `yaml:"stamp"`
	Parameters *ParametersFileConfig `yaml:"parameters"`
	Tree       *TreeConfig           `yaml:"tree"`
	// need the following for backwards compatibility:
	Files   *([]string)                 `yaml:"files"`
	Folders *(map[string](*TreeConfig)) `yaml:"folders"`
}
