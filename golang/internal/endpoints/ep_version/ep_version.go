package ep_version

import (
	"embed"
	"fmt"
	"phpytex/internal/setup/appconfig"
)

func Endpoint(res embed.FS, files map[string]string) {
	version := appconfig.Version(res, files)
	fmt.Println(version)
}
