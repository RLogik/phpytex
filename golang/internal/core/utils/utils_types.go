package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * METHOD convert basic types to pointers
 * ---------------------------------------------------------------- */

/****
 * NOTE: these cannot be replaced by inline variants, e.g.
 *    var x string
 *    var xx *string = &x
 * as then the values are tied.
 * These methods create addresses to clones of the original variables,
 * and do not coincide with the addresses of the original variables.
 ****/

func StructToPtr(x struct{}) *struct{} {
	var value = x
	return &value
}

func InterfaceToPtr(x interface{}) *interface{} {
	var value = x
	return &value
}

func BoolToPtr(x bool) *bool {
	var value = x
	return &value
}

func StringToPtr(x string) *string {
	var value = x
	return &value
}

func IntToPtr(x int) *int {
	var value = x
	return &value
}

/* ---------------------------------------------------------------- *
 * METHOD get value from ptr with default
 * ---------------------------------------------------------------- */

func PtrToBool(p *bool, Default bool) bool {
	if p != nil {
		return *p
	}
	return Default
}

func PtrToString(p *string, Default string) string {
	if p != nil {
		return *p
	}
	return Default
}

func PtrToInt(p *int, Default int) int {
	if p != nil {
		return *p
	}
	return Default
}
