package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

/* ---------------------------------------------------------------- *
 * METHODS serialisation of basic types
 * ---------------------------------------------------------------- */

func (c *ConfigString) Serialise() interface{} {
	if c == nil || c.Ptr == nil {
		return nil
	}
	return *(c.Ptr)
}

func (c *ConfigBool) Serialise() interface{} {
	if c == nil || c.Ptr == nil {
		return nil
	}
	return *(c.Ptr)
}

func (c *ConfigInt) Serialise() interface{} {
	if c == nil || c.Ptr == nil {
		return nil
	}
	return *(c.Ptr)
}

func (c *ConfigPath) Serialise() interface{} {
	if c == nil || c.Ptr == nil {
		return nil
	}
	return *(c.Ptr)
}

func (c *ConfigFile) Serialise() interface{} {
	if c == nil || c.Ptr == nil {
		return nil
	}
	return *(c.Ptr)
}
