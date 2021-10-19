package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

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
}
