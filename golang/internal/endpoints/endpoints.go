package endpoints

import (
	"fmt"
	"phpytex/internal/setup"
)

/* ---------------------------------------------------------------- *
 * METHOD version
 * ---------------------------------------------------------------- */

func Version() {
	fmt.Println(setup.Version())
}

/* ---------------------------------------------------------------- *
 * METHOD help
 * ---------------------------------------------------------------- */

func Help() {
	fmt.Println("")
	print(setup.Help())
	fmt.Println("")
}

/* ---------------------------------------------------------------- *
 * METHOD run
 * ---------------------------------------------------------------- */

func Run() {
	fmt.Println("[\033[93;1mWARNING\033[0m] End point \033[1mrun\033[0m not yet implemented")
}
