package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * METHOD serialisation
 * ---------------------------------------------------------------- */

func SerialiseBoolPtr(p *bool) interface{} {
	if p == nil {
		return nil
	}
	return *p
}

func SerialiseStringPtr(p *string) interface{} {
	if p == nil {
		return nil
	}
	return *p
}

func SerialiseIntPtr(p *int) interface{} {
	if p == nil {
		return nil
	}
	return *p
}

func SerialiseInterfacePtr(p *interface{}) interface{} {
	if p == nil {
		return nil
	}
	return *p
}
