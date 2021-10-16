package appconfig

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"math/rand"
	"os"

	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
	"phpytex/internal/customtypes"
)

/* ---------------------------------------------------------------- *
 * GLOBAL / LOCAL VARIABLES
 * ---------------------------------------------------------------- */

var pattern_config customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "patternConfig"}
var path_app customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "pathApp"}
var path_root customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "pathRoot"}
var file_start customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "fileStart"}
var file_transpiled customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "fileTranspiled"}
var file_output customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "fileOutput"}
var file_stamp customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "fileStamp"}
var with_file_stamp customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "withFileStamp"}
var file_params_py customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "bool"}
var with_file_params_py customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "withFileParamsPy"}
var import_param_py customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "importParamPy"}
var param_module_name customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "paramModuleName"}
var python_path customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "pythonPath"}

var option_legacy customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionLegacy"}
var option_ignore customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionIgnore"}
var option_debug customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionDebug"}
var option_compile_latex customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionCompileLatex"}
var option_show_tree customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionShowTree"}
var option_comments_auto customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionCommentsAuto"}
var option_comments_on customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionCommentsOn"}
var option_insert_bib customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionInsertBib"}
var option_overwrite_stamp customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionOverwriteStamp"}
var option_overwrite_params customtypes.ConfigParameterBool = customtypes.ConfigParameterBool{Name: "optionOverwriteParams"}
var max_length customtypes.ConfigParameterInt = customtypes.ConfigParameterInt{Name: "maxLength"}

// <-- prevents transpiler from creating overlarge files

var seed customtypes.ConfigParameterInt = customtypes.ConfigParameterInt{Name: "seed"}
var indent_character customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "indentCharacter"}
var indent_character_re customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "indentCharacterRe"}
var censor_symbol customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "censorSymbol"}
var offset_symbol customtypes.ConfigParameterString = customtypes.ConfigParameterString{Name: "offsetSymbol"}

/* ---------------------------------------------------------------- *
 * METHOD initialise
 * ---------------------------------------------------------------- */

func Init() {
	cwd, err := os.Getwd()
	if err != nil {
		logging.LogFatal(err)
	}
	path_root.SetDefault(cwd)
	with_file_stamp.SetDefault(false)
	with_file_params_py.SetDefault(false)
	param_module_name.SetDefault("MODULE_GLOBAL_PARAMS")
	python_path.SetDefault(utils.PythonCommand())
	option_legacy.SetDefault(false)
	option_ignore.SetDefault(false)
	option_debug.SetDefault(false)
	option_compile_latex.SetDefault(false)
	option_show_tree.SetDefault(true)
	option_comments_auto.SetDefault(true)
	option_comments_on.SetDefault(true)
	option_insert_bib.SetDefault(false)
	option_overwrite_stamp.SetDefault(true)
	option_overwrite_params.SetDefault(true)
	max_length.SetDefault(10000)
	censor_symbol.SetDefault("########")
	offset_symbol.SetDefault("")
}

/* ---------------------------------------------------------------- *
 * METHODS getters and setters
 * ---------------------------------------------------------------- */

func GetPatternConfig() string {
	return pattern_config.GetValue()
}

func SetPatternConfig(x string) {
	pattern_config.SetValue(x)
}

func GetPathApp() string {
	return path_app.GetValue()
}

func SetPathApp(x string) {
	path_app.SetValue(x)
}

func GetPathRoot() string {
	return path_root.GetValue()
}

func SetPathRoot(x string) {
	path_root.SetValue(x)
}

func GetFileStart() string {
	return file_start.GetValue()
}

func SetFileStart(x string) {
	file_start.SetValue(x)
}

func GetFileTranspiled() string {
	return file_transpiled.GetValue()
}

func SetFileTranspiled(x string) {
	file_transpiled.SetValue(x)
}

func GetFileOutput() string {
	return file_output.GetValue()
}

func SetFileOutput(x string) {
	file_output.SetValue(x)
}

func GetFileStamp() string {
	return file_stamp.GetValue()
}

func SetFileStamp(x string) {
	file_stamp.SetValue(x)
}

func GetWithFileStamp() bool {
	return with_file_stamp.GetValue()
}

func SetWithFileStamp(x bool) {
	with_file_stamp.SetValue(x)
}

func GetFileParamsPy() string {
	return file_params_py.GetValue()
}

func SetFileParamsPy(x string) {
	file_params_py.SetValue(x)
}

func GetWithFileParamsPy() bool {
	return with_file_params_py.GetValue()
}

func SetWithFileParamsPy(x bool) {
	with_file_params_py.SetValue(x)
}

func GetImportParamPy() string {
	return import_param_py.GetValue()
}

func SetImportParamPy(x string) {
	import_param_py.SetValue(x)
}

func GetParamModuleName() string {
	return param_module_name.GetValue()
}

func SetParamModuleName(x string) {
	param_module_name.SetValue(x)
}

func GetPythonPath() string {
	return python_path.GetValue()
}

func SetPythonPath(x string) {
	python_path.SetValue(x)
}

func GetOptionLegacy() bool {
	return option_legacy.GetValue()
}

func SetOptionLegacy(x bool) {
	option_legacy.SetValue(x)
}

func GetOptionIgnore() bool {
	return option_ignore.GetValue()
}

func SetOptionIgnore(x bool) {
	option_ignore.SetValue(x)
}

func GetOptionDebug() bool {
	return option_debug.GetValue()
}

func SetOptionDebug(x bool) {
	option_debug.SetValue(x)
}

func GetOptionCompileLatex() bool {
	return option_compile_latex.GetValue()
}

func SetOptionCompileLatex(x bool) {
	option_compile_latex.SetValue(x)
}

func GetOptionShowTree() bool {
	return option_show_tree.GetValue()
}

func SetOptionShowTree(x bool) {
	option_show_tree.SetValue(x)
}

func GetOptionCommentsAuto() bool {
	return option_comments_auto.GetValue()
}

func SetOptionCommentsAuto(x bool) {
	option_comments_auto.SetValue(x)
}

func GetOptionCommentsOn() bool {
	return option_comments_on.GetValue()
}

func SetOptionCommentsOn(x bool) {
	option_comments_on.SetValue(x)
}

func GetOptionInsertBib() bool {
	return option_insert_bib.GetValue()
}

func SetOptionInsertBib(x bool) {
	option_insert_bib.SetValue(x)
}

func GetOptionOverwriteStamp() bool {
	return option_overwrite_stamp.GetValue()
}

func SetOptionOverwriteStamp(x bool) {
	option_overwrite_stamp.SetValue(x)
}

func GetOptionOverwriteParams() bool {
	return option_overwrite_params.GetValue()
}

func SetOptionOverwriteParams(x bool) {
	option_overwrite_params.SetValue(x)
}

func GetMaxLength() int {
	return max_length.GetValue()
}

func SetMaxLength(x int) {
	max_length.SetValue(x)
}

func GetSeed() int {
	return seed.GetValue()
}

func SetSeed(x int) {
	seed.SetValue(x)
}

func ReSeed() {
	if seed.HasValue() {
		_seed := int64(seed.GetValue())
		rand.Seed(_seed)
	}
}

func GetIndentCharacter() string {
	return indent_character.GetValue()
}

func SetIndentCharacter(x string) {
	indent_character.SetValue(x)
}

func GetIndentCharacterRe() string {
	return indent_character_re.GetValue()
}

func SetIndentCharacterRe(x string) {
	indent_character_re.SetValue(x)
}

func GetCensorSymbol() string {
	return censor_symbol.GetValue()
}

func SetCensorSymbol(x string) {
	censor_symbol.SetValue(x)
}

func GetOffsetSymbol() string {
	return offset_symbol.GetValue()
}

func SetOffsetSymbol(x string) {
	offset_symbol.SetValue(x)
}
