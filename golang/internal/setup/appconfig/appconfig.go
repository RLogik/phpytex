package appconfig

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"phpytex/internal/types"
)

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

var Parameters types.AppConfig = types.AppConfig{
	PatternConfig:     types.ConfigString{Name: "PatternConfig"},
	PathRoot:          types.ConfigPath{Name: "PathRoot"},
	FileStart:         types.ConfigFile{Name: "FileStart"},
	FileTranspiled:    types.ConfigFile{Name: "FileTranspiled"},
	FileOutput:        types.ConfigFile{Name: "FileOutput"},
	WithFileStamp:     types.ConfigBool{Name: "WithFileStamp"},
	FileStamp:         types.ConfigFile{Name: "FileStamp"},
	WithFileParamsPy:  types.ConfigBool{Name: "WithFileParamsPy"},
	FileParamsPy:      types.ConfigFile{Name: "FileParamsPy"},
	ImportParamsPy:    types.ConfigString{Name: "ImportParamsPy"},
	ParamModuleName:   types.ConfigString{Name: "ParamModuleName"},
	PythonPath:        types.ConfigString{Name: "PythonPath"},
	IndentCharacter:   types.ConfigString{Name: "IndentCharacter"},
	IndentCharacterRe: types.ConfigString{Name: "IndentCharacterRe"},
	CensorSymbol:      types.ConfigString{Name: "CensorSymbol"},
	// compile options
	OptionLegacy:       types.ConfigBool{Name: "OptionLegacy"},
	OptionIgnore:       types.ConfigBool{Name: "OptionIgnore"},
	OptionDebug:        types.ConfigBool{Name: "OptionDebug"},
	OptionCompileLatex: types.ConfigBool{Name: "OptionCompileLatex"},
	OptionShowTree:     types.ConfigBool{Name: "OptionShowTree"},
	OptionCommentsAuto: types.ConfigBool{Name: "OptionCommentsAuto"},
	OptionCommentsOn:   types.ConfigBool{Name: "OptionCommentsOn"},
	OptionInsertBib:    types.ConfigBool{Name: "OptionInsertBib"},
	MaxLength:          types.ConfigInt{Name: "MaxLength"},
	Seed:               types.ConfigInt{Name: "Seed"},
	Offset:             types.ConfigString{Name: "OffsetSymbol"},
	// stamp/param options
	OptionOverwriteStamp:  types.ConfigBool{Name: "OptionOverwriteStamp"},
	OptionOverwriteParams: types.ConfigBool{Name: "OptionOverwriteParams"},
}

var DictionaryStamp types.Dictionary
var DictionaryParams types.Dictionary
var ProjectTree *types.TreeConfig
var ExportVariables types.Dictionary
