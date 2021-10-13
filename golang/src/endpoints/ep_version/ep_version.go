package ep_version

import (
	"fmt"
	"phpytex/setup/appconfig"
)

func Endpoint() {
	fmt.Println(appconfig.VERSION)
}
