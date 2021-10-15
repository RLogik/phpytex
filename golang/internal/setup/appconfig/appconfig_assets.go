package appconfig

import (
	"embed"
	"fmt"
	"log"
)

var Res embed.FS
var Assets map[string]string

func ReadAsset(key string) string {
	var found bool
	if _, found = Assets[key]; !found {
		log.Fatal(fmt.Sprintf("Key \033[1m%s\033[0m not found in dictionary!", key))
	}
	data, err := Res.ReadFile(Assets[key])
	if err != nil {
		log.Fatal(err)
	}
	text := string(data)
	return text
}
