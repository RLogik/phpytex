package customtypes

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"github.com/akamensky/argparse"
)

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

type CliArguments struct {
	Help    *argparse.Command
	Version *argparse.Command
	Run     *argparse.Command
	Quiet   *bool
	File    *string
}
