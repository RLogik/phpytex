package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

/* ---------------------------------------------------------------- *
 * METHOD serialisation of basic types
 * ---------------------------------------------------------------- */

func BoolPtr(p *bool) interface{} {
	if p == nil {
		return nil
	}
	return *p
}

func StringPtr(p *string) interface{} {
	if p == nil {
		return nil
	}
	return *p
}

func IntPtr(p *int) interface{} {
	if p == nil {
		return nil
	}
	return *p
}

func InterfacePtr(p *interface{}) interface{} {
	if p == nil {
		return nil
	}
	return *p
}
