package ep_help

import (
	"fmt"
	"phpytex/internal/setup/appconfig"
)

func Endpoint() {
	fmt.Println("")
	print(appconfig.Help())
	fmt.Println("")
}
