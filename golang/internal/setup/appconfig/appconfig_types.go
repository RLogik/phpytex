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
	Name string
	Ptr  *string
}

type ConfigBool struct {
	Name string
	Ptr  *bool
}

type ConfigInt struct {
	Name string
	Ptr  *int
}

type ConfigPath ConfigString

type ConfigFile ConfigString

/* ---------------------------------------------------------------- *
 * METHODS config string
 * ---------------------------------------------------------------- */

func (c *ConfigString) SetValue(x string) {
	c.Ptr = &x
}

func (c *ConfigString) SetValueFromPtr(x *string) {
	c.Ptr = nil
	if x != nil {
		c.SetValue(*x)
	}
}

func (c ConfigString) HasValue() bool {
	return (c.Ptr != nil)
}

func (c ConfigString) GetValue() string {
	if c.Ptr != nil {
		return *(c.Ptr)
	}
	raiseParameterError(c.Name)
	return ""
}

/* ---------------------------------------------------------------- *
 * METHODS config path
 * ---------------------------------------------------------------- */

func (c *ConfigPath) SetValue(x string) {
	if utils.CheckPathExists(x) {
		c.Ptr = &x
	} else {
		logging.LogFatal("Cannot use \033[1m%[1]s\033[0m as path for parameter \033[1m%[2]s\033[0m", x, c.Name)
	}
}

func (c *ConfigPath) SetValueFromPtr(x *string) {
	c.Ptr = nil
	if x != nil {
		c.SetValue(*x)
	}
}

func (c ConfigPath) HasValue() bool {
	return (c.Ptr != nil)
}

func (c ConfigPath) GetValue() string {
	if c.Ptr != nil {
		return *(c.Ptr)
	}
	raiseParameterError(c.Name)
	return ""
}

/* ---------------------------------------------------------------- *
 * METHODS config file
 * ---------------------------------------------------------------- */

func (c *ConfigFile) SetValue(x string) {
	c.Ptr = &x
}

func (c *ConfigFile) SetValueFromPtr(x *string) {
	c.Ptr = nil
	if x != nil {
		c.SetValue(*x)
	}
}

func (c ConfigFile) HasValue() bool {
	return (c.Ptr != nil)
}

func (c ConfigFile) GetValue(rel bool) string {
	var file string
	var err error
	if c.Ptr != nil {
		file = *(c.Ptr)
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

func (c ConfigFile) GetValueBase() string {
	return filepath.Base(c.GetValue(false))
}

/* ---------------------------------------------------------------- *
 * METHODS config bool
 * ---------------------------------------------------------------- */

func (c *ConfigBool) SetValue(x bool) {
	c.Ptr = &x
}

func (c *ConfigBool) SetValueFromPtr(x *bool) {
	c.Ptr = nil
	if x != nil {
		c.SetValue(*x)
	}
}

func (c ConfigBool) HasValue() bool {
	return (c.Ptr != nil)
}

func (c ConfigBool) GetValue() bool {
	if c.Ptr != nil {
		return *(c.Ptr)
	}
	raiseParameterError(c.Name)
	return false
}

/* ---------------------------------------------------------------- *
 * METHODS config int
 * ---------------------------------------------------------------- */

func (c *ConfigInt) SetValue(x int) {
	c.Ptr = &x
}

func (c *ConfigInt) SetValueFromPtr(x *int) {
	c.Ptr = nil
	if x != nil {
		c.SetValue(*x)
	}
}

func (c ConfigInt) HasValue() bool {
	return (c.Ptr != nil)
}

func (c ConfigInt) GetValue() int {
	if c.Ptr != nil {
		return *(c.Ptr)
	}
	raiseParameterError(c.Name)
	return 0
}

/* ---------------------------------------------------------------- *
 * AUXILIARY METHODS
 * ---------------------------------------------------------------- */

func raiseParameterError(name string) {
	logging.LogFatal(fmt.Sprintf("Neither a Ptr nor default Ptr of \033[1m%[1]s\033[0m has been set.", name))
}
