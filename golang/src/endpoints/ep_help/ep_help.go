package ep_help

import (
	"fmt"
	// "github.com/lithammer/dedent"
)

func Endpoint() {
	fmt.Println("")
	fmt.Println("Usage of \033[32;1m(PH(p)y)tex\033[0m")
	fmt.Println("~~~~~~~~~~~~~~~~~~~~")
	fmt.Println("")
	fmt.Println("- Version and help:")
	fmt.Println("")
	fmt.Println("    phpytex \033[1mversion\033[0m")
	fmt.Println("    phpytex \033[1mhelp\033[0m")
	fmt.Println("")
	fmt.Println("- To run the transpiler within a project, call one of:")
	fmt.Println("")
	fmt.Println("    phpytex \033[1mrun\033[0m")
	fmt.Println("    phpytex \033[1mrun\033[0m [\033[1mfile\033[0m=\033[2m<name of config file>\033[0m]")
	fmt.Println("")
	fmt.Println("  If the optional flag is left empty, the programme searches for the first yaml-file")
	fmt.Println("  in the directory which matches")
	fmt.Println("")
	fmt.Println("    \033[1m*.(phpytex|phpycreate).(yml|yaml)\033[0m")
	fmt.Println("")
	/* NOTE: Does not work, as characters are not properly escaped.
	message := dedent.Dedent(`")
	Usage of \033[32;1m(PH(p)y)tex\033[0m
	~~~~~~~~~~~~~~~~~~~~

	- Version and help:

	    phpytex \033[1mversion\033[0m
	    phpytex \033[1mhelp\033[0m

	- To run the transpiler within a project, call one of:

	    phpytex \033[1mrun\033[0m
	    phpytex \033[1mrun\033[0m [\033[1mfile\033[0m=\033[2m<name of config file>\033[0m]

	  If the optional flag is left empty, the programme searches for the first yaml-file
	  in the directory which matches

	    \033[1m*.(phpytex|phpycreate).(yml|yaml)\033[0m
	`)
	fmt.Println(fmt.Sprintf(message)) */
}
