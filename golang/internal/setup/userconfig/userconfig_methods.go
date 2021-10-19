package userconfig

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"phpytex/internal/types"
)

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

// deals with missing main sections of config
func HandleMissingSections(config *types.UserConfig) {
	if config.Header == nil {
		config.Header = DefaultUserConfig.Header
	}
	if config.Compile == nil {
		config.Compile = DefaultUserConfig.Compile
	}
}

// cleans up structure to handle backwards compatibility
func HandleBackwardsCompatibility(config *types.UserConfig) {
	// [ignore] prioritise setting from: [header -> ignore], compile [option -> ignore]:
	var ignore bool
	ignore = types.PtrToBool(config.Header.Ignore, false) || types.PtrToBool(config.Compile.Ignore, false)
	config.Header.Ignore = types.BoolToPtr(ignore)
	config.Compile.Ignore = nil

	// flatten [compile -> options] ~~> [compile]:
	if config.Compile.Options != nil {
		config.Compile = config.Compile.Options
		config.Compile.Options = nil
	}
	// [root] can be either [root] or [input]:
	if config.Compile.Input != nil && config.Compile.Root == nil {
		config.Compile.Root = types.StringToPtr(*config.Compile.Input)
		config.Compile.Input = nil
	}
	// [compile] can be either [compile] or [compile-latex]:
	if config.Compile.CompileLatex != nil && config.Compile.Compile == nil {
		config.Compile.Compile = types.BoolToPtr(*config.Compile.CompileLatex)
		config.Compile.CompileLatex = nil
	}
	// [show-tree] can be either [show-tree] or [show-structure]:
	if config.Compile.ShowStructure != nil && config.Compile.ShowTree == nil {
		config.Compile.ShowTree = types.BoolToPtr(*config.Compile.ShowStructure)
		config.Compile.ShowStructure = nil
	}

	// if [tree] option not used:
	if config.Tree == nil {
		tree := types.TreeConfig{
			Files:   nil,
			Folders: nil,
		}
		if config.Files != nil {
			tree.Files = &(*config.Files)
		}
		if config.Folders != nil {
			tree.Folders = &(*config.Folders)
		}
		config.Tree = &tree
		config.Files = nil
		config.Folders = nil
	}
}

// cleans up structure to handle missing values
func HandleMissingKeys(config *types.UserConfig) {
	if config.Compile.Tabs == nil {
		config.Compile.Tabs = DefaultUserConfig.Compile.Tabs
	}
	if config.Compile.Spaces == nil {
		config.Compile.Spaces = DefaultUserConfig.Compile.Spaces
	}
	if config.Compile.Legacy == nil {
		config.Compile.Legacy = DefaultUserConfig.Compile.Legacy
	}
	if config.Stamp != nil {
		if config.Stamp.Overwrite == nil {
			config.Stamp.Overwrite = DefaultUserConfig.Stamp.Overwrite
		}
		if config.Stamp.File == nil {
			config.Stamp.File = DefaultUserConfig.Stamp.File
		}
	}
	if config.Parameters != nil {
		if config.Parameters.Overwrite == nil {
			config.Parameters.Overwrite = DefaultUserConfig.Parameters.Overwrite
		}
		// if config.Parameters.File == nil {
		// 	config.Parameters.File = DefaultUserConfig.Parameters.File
		// }
	}
}
