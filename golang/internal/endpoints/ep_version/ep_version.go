package ep_version

import (
	"fmt"
	"phpytex/internal/setup/appconfig"
)

func Endpoint() {
	fmt.Println(appconfig.Version())
}
