package endpoints

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"phpytex/internal/core/logging"
	"phpytex/internal/setup"
)

/* ---------------------------------------------------------------- *
 * ENDPOINT version
 * ---------------------------------------------------------------- */

func Version() {
	logging.SetForce(true)
	logging.LogPlain(setup.Version())
}

/* ---------------------------------------------------------------- *
 * ENDPOINT help
 * ---------------------------------------------------------------- */

func Help() {
	logging.SetForce(true)
	logging.LogPlain(
		"",
		setup.Logo(),
		setup.Help(),
		"",
	)
}
