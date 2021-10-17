package appconfig

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"fmt"
	"path/filepath"

	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * TYPES config params
 * ---------------------------------------------------------------- */

type ConfigString struct {
	Name  string
	value *string
}

type ConfigBool struct {
	Name  string
	value *bool
}

type ConfigInt struct {
	Name  string
	value *int
}

type ConfigPath ConfigString

type ConfigFile ConfigString

/* ---------------------------------------------------------------- *
 * METHODS config string
 * ---------------------------------------------------------------- */

func (c *ConfigString) SetValue(x string) {
	c.value = &x
}

func (c *ConfigString) SetValueFromPtr(x *string) {
	c.value = nil
	if x != nil {
		c.SetValue(*x)
	}
}

func (c *ConfigString) HasValue() bool {
	return (c.value != nil)
}

func (c ConfigString) GetValue() string {
	if c.value != nil {
		return *(c.value)
	}
	raiseParameterError(c.Name)
	return ""
}

/* ---------------------------------------------------------------- *
 * METHODS config path
 * ---------------------------------------------------------------- */

func (c *ConfigPath) SetValue(x string) {
	if utils.CheckPathExists(x) {
		c.value = &x
	} else {
		logging.LogFatal("Cannot use \033[1m%[1]s\033[0m as path for parameter \033[1m%[2]s\033[0m", x, c.Name)
	}
}

func (c *ConfigPath) SetValueFromPtr(x *string) {
	c.value = nil
	if x != nil {
		c.SetValue(*x)
	}
}

/* ---------------------------------------------------------------- *
 * METHODS config file
 * ---------------------------------------------------------------- */

func (c ConfigFile) GetValue(rel bool) string {
	var file string
	var err error
	if c.value != nil {
		file = *(c.value)
	} else {
		raiseParameterError(c.Name)
		return ""
	}
	file, err = filepath.Abs(file)
	if rel && err == nil {
		dir, err := utils.GetCwd()
		if err == nil {
			file, err = filepath.Rel(dir, file)
		}
	}
	if err != nil {
		raiseParameterError(c.Name)
	}
	return file
}

/* ---------------------------------------------------------------- *
 * METHODS config bool
 * ---------------------------------------------------------------- */

func (c *ConfigBool) SetValue(x bool) {
	c.value = &x
}

func (c *ConfigBool) SetValueFromPtr(x *bool) {
	c.value = nil
	if x != nil {
		c.SetValue(*x)
	}
}

func (c *ConfigBool) HasValue() bool {
	return (c.value != nil)
}

func (c ConfigBool) GetValue() bool {
	if c.value != nil {
		return *(c.value)
	}
	raiseParameterError(c.Name)
	return false
}

/* ---------------------------------------------------------------- *
 * METHODS config int
 * ---------------------------------------------------------------- */

func (c *ConfigInt) SetValue(x int) {
	c.value = &x
}

func (c *ConfigInt) SetValueFromPtr(x *int) {
	c.value = nil
	if x != nil {
		c.SetValue(*x)
	}
}

func (c *ConfigInt) HasValue() bool {
	return (c.value != nil)
}

func (c ConfigInt) GetValue() int {
	if c.value != nil {
		return *(c.value)
	}
	raiseParameterError(c.Name)
	return 0
}

/* ---------------------------------------------------------------- *
 * AUXILIARY METHODS
 * ---------------------------------------------------------------- */

func raiseParameterError(name string) {
	logging.LogFatal(fmt.Sprintf("Neither a value nor default value of \033[1m%[1]s\033[0m has been set.", name))
}
