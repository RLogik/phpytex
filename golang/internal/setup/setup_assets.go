package setup

import (
	"embed"
	"fmt"
	"log"

	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * GLOBAL VARIABLES
 * ---------------------------------------------------------------- */

var Res embed.FS
var Assets map[string]string

/* ---------------------------------------------------------------- *
 * METHOD read assets
 * ---------------------------------------------------------------- */

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

/* ---------------------------------------------------------------- *
 * METHODS templates
 * ---------------------------------------------------------------- */

func Version() string {
	return ReadAsset("version")
}

func Help() string {
	contents := ReadAsset("help")
	return utils.DedentAndExpand(contents)
}

func TemplatePre(args map[string]interface{}) string {
	contents := ReadAsset("pre")
	return utils.FormatString(contents, args)
}

func TemplatePost() string {
	emptyargs := map[string]interface{}{}
	contents := ReadAsset("post")
	return utils.FormatString(contents, emptyargs)
}
