package customtypes

import (
	"fmt"
	"os"
	"path/filepath"
	"phpytex/internal/core/logging"
	"phpytex/internal/core/utils"
)

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * CLASSES config params
 * ---------------------------------------------------------------- */

type ConfigParameterString struct {
	Name         string
	value        *string
	defaultValue *string
}

type ConfigParameterPath struct {
	Name         string
	value        *string
	defaultValue *string
}

type ConfigParameterFile struct {
	Name         string
	value        *string
	defaultValue *string
}

type ConfigParameterBool struct {
	Name         string
	value        *bool
	defaultValue *bool
}

type ConfigParameterInt struct {
	Name         string
	value        *int
	defaultValue *int
}

/* ---------------------------------------------------------------- *
 * METHODS config parameters string
 * ---------------------------------------------------------------- */

func (c *ConfigParameterString) SetDefault(x string) *ConfigParameterString {
	c.defaultValue = &x
	return c
}

func (c *ConfigParameterString) SetValue(x string) *ConfigParameterString {
	c.value = &x
	return c
}

func (c *ConfigParameterString) HasValue() bool {
	return (c.value != nil)
}

func (c ConfigParameterString) GetValue() string {
	if c.value != nil {
		return *(c.value)
	} else if c.defaultValue != nil {
		return *(c.defaultValue)
	}
	raiseParameterError(c.Name)
	return ""
}

/* ---------------------------------------------------------------- *
 * METHODS config parameters path
 * ---------------------------------------------------------------- */

func (c *ConfigParameterPath) SetDefault(x string) *ConfigParameterPath {
	c.defaultValue = &x
	return c
}

func (c *ConfigParameterPath) SetValue(x string) *ConfigParameterPath {
	if utils.CheckPathExists(x) {
		c.value = &x
	} else {
		logging.LogFatal("Cannot use \033[1m%[1]s\033[0m as path for parameter \033[1m%[2]s\033[0m", x, c.Name)
	}
	return c
}

func (c *ConfigParameterPath) HasValue() bool {
	return (c.value != nil)
}

func (c ConfigParameterPath) GetValue() string {
	if c.value != nil {
		return *(c.value)
	} else if c.defaultValue != nil {
		return *(c.defaultValue)
	}
	raiseParameterError(c.Name)
	return ""
}

/* ---------------------------------------------------------------- *
 * METHODS config parameters file
 * ---------------------------------------------------------------- */

func (c *ConfigParameterFile) SetDefault(x string) *ConfigParameterFile {
	c.defaultValue = &x
	return c
}

func (c *ConfigParameterFile) SetValue(x string) *ConfigParameterFile {
	if !(x == "") {
		c.value = &x
	}
	return c
}

func (c *ConfigParameterFile) HasValue() bool {
	return (c.value != nil)
}

func (c ConfigParameterFile) GetValue(rel bool) string {
	var file string
	var err error
	if c.value != nil {
		file = *(c.value)
	} else if c.defaultValue != nil {
		file = *(c.defaultValue)
	} else {
		raiseParameterError(c.Name)
		return ""
	}
	file, err = filepath.Abs(file)
	if rel && err == nil {
		dir, err := os.Getwd()
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
 * METHODS config parameters bool
 * ---------------------------------------------------------------- */

func (c *ConfigParameterBool) SetDefault(x bool) *ConfigParameterBool {
	c.defaultValue = &x
	return c
}

func (c *ConfigParameterBool) SetValue(x bool) *ConfigParameterBool {
	c.value = &x
	return c
}

func (c *ConfigParameterBool) HasValue() bool {
	return (c.value != nil)
}

func (c ConfigParameterBool) GetValue() bool {
	if c.value != nil {
		return *(c.value)
	} else if c.defaultValue != nil {
		return *(c.defaultValue)
	}
	raiseParameterError(c.Name)
	return false
}

/* ---------------------------------------------------------------- *
 * METHODS config parameters int
 * ---------------------------------------------------------------- */

func (c *ConfigParameterInt) SetDefault(x int) *ConfigParameterInt {
	c.defaultValue = &x
	return c
}

func (c *ConfigParameterInt) SetValue(x int) *ConfigParameterInt {
	c.value = &x
	return c
}

func (c *ConfigParameterInt) HasValue() bool {
	return (c.value != nil)
}

func (c ConfigParameterInt) GetValue() int {
	if c.value != nil {
		return *(c.value)
	} else if c.defaultValue != nil {
		return *(c.defaultValue)
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
