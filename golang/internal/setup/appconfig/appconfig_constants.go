package appconfig

import (
	"embed"
	"log"
	"strings"
)

func Version(res embed.FS, files map[string]string) string {
	data, err := res.ReadFile(files["version"])
	if err != nil {
		log.Fatal(err)
	}
	version := string(data)
	version = strings.TrimSpace(version)
	return version
}
