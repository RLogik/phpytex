package appconfig

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"phpytex/internal/setup/userconfig"
)

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

type AppConfig struct {
	PatternConfig     ConfigString
	PathRoot          ConfigPath
	FileStart         ConfigFile
	FileTranspiled    ConfigFile
	FileOutput        ConfigFile
	WithFileStamp     ConfigBool
	FileStamp         ConfigFile
	WithFileParamsPy  ConfigBool
	FileParamsPy      ConfigFile
	ImportParamsPy    ConfigString
	ParamModuleName   ConfigString
	PythonPath        ConfigString
	IndentCharacter   ConfigString
	IndentCharacterRe ConfigString
	CensorSymbol      ConfigString
	// compile options
	OptionLegacy       ConfigBool
	OptionIgnore       ConfigBool
	OptionDebug        ConfigBool
	OptionCompileLatex ConfigBool
	OptionShowTree     ConfigBool
	OptionCommentsAuto ConfigBool
	OptionCommentsOn   ConfigBool
	OptionInsertBib    ConfigBool
	MaxLength          ConfigInt // <-- prevents transpiler from creating overlarge file"MaxLength"s
	Seed               ConfigInt
	Offset             ConfigString
	// stamp/param options
	OptionOverwriteStamp  ConfigBool
	OptionOverwriteParams ConfigBool
	DictionaryStamp       *(map[string]interface{})
	DictionaryParams      *(map[string]interface{})
	ProjectTree           *userconfig.TreeConfig
}

var Parameters AppConfig = AppConfig{
	PatternConfig:     ConfigString{Name: "PatternConfig"},
	PathRoot:          ConfigPath{Name: "PathRoot"},
	FileStart:         ConfigFile{Name: "FileStart"},
	FileTranspiled:    ConfigFile{Name: "FileTranspiled"},
	FileOutput:        ConfigFile{Name: "FileOutput"},
	WithFileStamp:     ConfigBool{Name: "WithFileStamp"},
	FileStamp:         ConfigFile{Name: "FileStamp"},
	WithFileParamsPy:  ConfigBool{Name: "WithFileParamsPy"},
	FileParamsPy:      ConfigFile{Name: "FileParamsPy"},
	ImportParamsPy:    ConfigString{Name: "ImportParamsPy"},
	ParamModuleName:   ConfigString{Name: "ParamModuleName"},
	PythonPath:        ConfigString{Name: "PythonPath"},
	IndentCharacter:   ConfigString{Name: "IndentCharacter"},
	IndentCharacterRe: ConfigString{Name: "IndentCharacterRe"},
	CensorSymbol:      ConfigString{Name: "CensorSymbol"},
	// compile options
	OptionLegacy:       ConfigBool{Name: "OptionLegacy"},
	OptionIgnore:       ConfigBool{Name: "OptionIgnore"},
	OptionDebug:        ConfigBool{Name: "OptionDebug"},
	OptionCompileLatex: ConfigBool{Name: "OptionCompileLatex"},
	OptionShowTree:     ConfigBool{Name: "OptionShowTree"},
	OptionCommentsAuto: ConfigBool{Name: "OptionCommentsAuto"},
	OptionCommentsOn:   ConfigBool{Name: "OptionCommentsOn"},
	OptionInsertBib:    ConfigBool{Name: "OptionInsertBib"},
	MaxLength:          ConfigInt{Name: "MaxLength"},
	Seed:               ConfigInt{Name: "Seed"},
	Offset:             ConfigString{Name: "OffsetSymbol"},
	// stamp/param options
	OptionOverwriteStamp:  ConfigBool{Name: "OptionOverwriteStamp"},
	OptionOverwriteParams: ConfigBool{Name: "OptionOverwriteParams"},
	DictionaryStamp:       nil,
	DictionaryParams:      nil,
}
