package appconfig

import "phpytex/internal/core/utils"

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
