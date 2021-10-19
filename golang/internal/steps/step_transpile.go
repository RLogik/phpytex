package steps

/* ---------------------------------------------------------------- *
* IMPORTS
* ---------------------------------------------------------------- */

import (
	"fmt"
	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
	"phpytex/internal/setup"
	"phpytex/internal/setup/appconfig"
	"phpytex/internal/setup/templates"
	"phpytex/internal/types"
	"strings"
)

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func Transpile() error {
	logging.LogInfo("TRANSPILATION (phpytex -> python) STARTED.")
	var (
		err        error = nil
		root       string
		indentSymb string
		seed       *int
		name       string
		preambles  []string
		documents  types.TranspileDocuments
		blocks     types.TranspileBlocks
		imports    types.TranspileBlocks
		globalvars []string
	)

	root = appconfig.Parameters.PathRoot.GetValue()
	indentSymb = appconfig.Parameters.IndentCharacter.GetValue()
	seed = appconfig.Parameters.Seed.Ptr

	// Initialise structures for recording transpilation units:
	appconfig.ReSeed() // <-- only do this once!
	preambles = []string{}
	imports = types.TranspileBlocks{}
	documents = types.TranspileDocuments{
		Root:       root,
		IndentSymb: indentSymb,
		Schemes: types.TranspileFileNameScheme{
			File: templates.FUNCTION_NAME_FILE,
			Main: templates.FUNCTION_NAME_MAIN,
			Pre:  templates.FUNCTION_NAME_PRE,
		},
	}

	// Transpile preamble:
	if appconfig.Parameters.WithFileStamp.GetValue() {
		name = "stamp"
		preambles = append(preambles, name)
		err = transpileDocument(
			appconfig.Parameters.FileStamp.GetValue(true),
			documents,
			types.TranspileBlocks{},
			name,
			true, // is_preamble
			true, // silent
			types.TranspileCommentOptions{
				CommentsOn:   true,
				CommentsAuto: false,
				ShowTree:     false,
			},
		)
	}

	if err != nil {
		return err
	}

	// Transpile document file:
	err = transpileDocument(
		appconfig.Parameters.FileStart.GetValue(true),
		documents,
		imports,
		"",
		false,
		logging.GetQuietMode(),
		types.TranspileCommentOptions{
			CommentsOn:   appconfig.Parameters.OptionCommentsOn.GetValue(),
			CommentsAuto: appconfig.Parameters.OptionCommentsAuto.GetValue(),
			ShowTree:     appconfig.Parameters.OptionShowTree.GetValue(),
		},
	)

	if err != nil {
		return err
	}

	// Add document structure:
	name = "tree"
	if appconfig.Parameters.OptionShowTree.GetValue() {
		preambles = append(preambles, name)
	}
	blocks = types.TranspileBlocks{}
	blocks.Init(documents.DocumentTree(seed))
	documents.AddPreamble(name, blocks)

	// Handle global parameters:
	if appconfig.Parameters.WithFileParamsPy.GetValue() {
		// Create file:
		err = createImportFileParameters(
			appconfig.Parameters.FileParamsPy.GetValue(false),
			appconfig.Parameters.OptionOverwriteParams.GetValue(),
			documents,
		)
		// Add import block for global parameters:
		imports.Append(types.TranspileBlock{
			Kind:       "code",
			Content:    fmt.Sprintf(`from %[1]s import *;`, appconfig.Parameters.ImportParamsPy.GetValue()),
			Level:      0,
			IndentSymb: indentSymb,
		})
	}

	if err != nil {
		return err
	}

	// Generate result of transpilation (phpytex -> python):
	globalvars = []string{}
	if appconfig.ExportVariables.GetValues() != nil {
		for name, _ = range *appconfig.ExportVariables.GetValues() {
			globalvars = append(globalvars, name)
		}
	}
	for _, name = range documents.GetVariables() {
		globalvars = append(globalvars, name)
	}
	globalvars = utils.UniqueListOfStrings(globalvars)
	err = createMetaCode(
		documents,
		imports,
		preambles,
		globalvars,
		seed,
	)

	if err != nil {
		return err
	}

	logging.LogInfo("TRANSPILATION (phpytex -> python) COMPLETE.")
	return nil
}

/* ---------------------------------------------------------------- *
 * SECONDARY METHODS
 * ---------------------------------------------------------------- */

func transpileDocument(
	path string,
	documents types.TranspileDocuments,
	imports types.TranspileBlocks,
	name string,
	isPreamble bool,
	silent bool,
	params types.TranspileCommentOptions,
) error {
	// TODO
	return nil
}

func createImportFileParameters(
	path string,
	overwrite bool,
	documents types.TranspileDocuments,
) error {
	if utils.CheckPathExists(path) && !overwrite {
		return nil
	}
	var (
		err        error
		lines      []string
		text       string
		line       string
		name       string
		obj        interface{}
		valuePair  *[]interface{}
		codedvalue interface{}
	)
	lines = utils.FormatTextBlockAsList(`
		#!/usr/bin/env python3
		# -*- coding: utf-8 -*-
	`)
	lines = append(lines, "")
	if appconfig.ExportVariables.GetValues() != nil {
		for name, obj = range *appconfig.ExportVariables.GetValues() {
			valuePair = utils.InterfaceToArray(obj)
			if valuePair == nil || len(*valuePair) != 2 {
				continue
			}
			codedvalue = (*valuePair)[1]
			line = fmt.Sprintf(`%[1]s = %[2]v;`, name, codedvalue)
			lines = append(lines, line)
		}
	}
	for _, name = range documents.GetVariables() {
		if appconfig.ExportVariables.HasKey(name) {
			continue
		}
		line = fmt.Sprintf(`%[1]s = None;`, name)
		lines = append(lines, line)
	}
	lines = append(lines, "")
	text = strings.Join(lines, "\n")
	err = utils.WriteTextFile(path, text, true)
	return err
}

func createMetaCode(
	documents types.TranspileDocuments,
	imports types.TranspileBlocks,
	preambles []string,
	globalvars []string,
	seed *int,
) error {
	var (
		err  error
		text string
	)
	text = setup.TemplatePre(map[string]interface{}{
		"imports":      strings.Join(imports.GenerateCode(0), "\n"),
		"rootDir":      appconfig.Parameters.PathRoot.GetValue(),
		"outputFile":   appconfig.Parameters.FileOutput.GetValue(false),
		"outputName":   appconfig.Parameters.FileOutput.GetValueBase(),
		"insertBib":    appconfig.Parameters.OptionInsertBib.GetValue(),
		"compileLatex": appconfig.Parameters.OptionCompileLatex.GetValue(),
		"lengthMax":    appconfig.Parameters.MaxLength.GetValue(),
		"seed":         utils.ExpandPtrToInt(seed),
		"indentSymb":   appconfig.Parameters.IndentCharacter.GetValue(),
		"censorSymb":   appconfig.Parameters.CensorSymbol.GetValue(),
		"mainFct":      templates.FUNCTION_NAME_MAIN,
	})
	text += "\n"
	text += "\n" + strings.Join(documents.GenerateCode(0, preambles, globalvars), "\n")
	text += "\n"
	text += "\n" + setup.TemplatePost()

	err = utils.WriteTextFile(appconfig.Parameters.FileTranspiled.GetValue(false), text)
	return err
}

/* ---------------------------------------------------------------- *
 * SECONDARY METHODS
 * ---------------------------------------------------------------- */

func displayTreeBranch(
	path string,
	anon bool, // false,
	prefix string, // "",
	indentSymb string, // "    ",
	branchSymb string, // "  |____",
	depth int, // 0
) string {
	n := depth - 1
	if depth == 0 {
		n = 0
		branchSymb = ""
	}
	if anon {
		path = appconfig.Parameters.CensorSymbol.GetValue()
	}
	return fmt.Sprintf(`%[1]s%[2]s%[3]s %[4]s`,
		prefix,
		strings.Repeat(indentSymb, n),
		branchSymb,
		path,
	)
}
