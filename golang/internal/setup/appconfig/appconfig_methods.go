package appconfig

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"math/rand"

	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * METHOD initialise
 * ---------------------------------------------------------------- */

func Init() error {
	var err error
	var cwd string
	cwd, err = utils.GetCwd()
	if err != nil {
		return err
	}
	Parameters.PatternConfig.SetValue(`^(|.*\.)(phpytex|phpycreate)\.(yml|yaml)$`)
	Parameters.PathRoot.SetValue(cwd)
	Parameters.FileTranspiled.SetValue("phpytex_transpiled.py")
	Parameters.FileOutput.SetValue("main.tex")
	Parameters.WithFileStamp.SetValue(false)
	Parameters.WithFileParamsPy.SetValue(false)
	Parameters.ParamModuleName.SetValue("MODULE_GLOBAL_PARAMS")
	Parameters.IndentCharacter.SetValue("    ")
	Parameters.IndentCharacterRe.SetValue("    ")
	Parameters.CensorSymbol.SetValue(("########"))
	Parameters.OptionLegacy.SetValue(false)
	Parameters.OptionIgnore.SetValue(false)
	Parameters.OptionDebug.SetValue(false)
	Parameters.OptionCompileLatex.SetValue(false)
	Parameters.OptionShowTree.SetValue(true)
	Parameters.OptionCommentsAuto.SetValue(true)
	Parameters.OptionCommentsOn.SetValue(true)
	Parameters.OptionInsertBib.SetValue(true)
	Parameters.MaxLength.SetValue(10000)
	Parameters.Offset.SetValue("")
	Parameters.OptionOverwriteStamp.SetValue(true)
	Parameters.OptionOverwriteParams.SetValue(true)
	return err
}

/* ---------------------------------------------------------------- *
 * METHODS reseed
 * ---------------------------------------------------------------- */

func ReSeed() {
	if Parameters.Seed.HasValue() {
		seed := int64(Parameters.Seed.GetValue())
		rand.Seed(seed)
	}
}
