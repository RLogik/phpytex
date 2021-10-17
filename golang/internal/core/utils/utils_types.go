package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * METHOD convert basic types to pointers
 * ---------------------------------------------------------------- */

func StructToPtr(x struct{}) *struct{} {
	return &x
}

func InterfaceToPtr(x interface{}) *interface{} {
	return &x
}

func BoolToPtr(x bool) *bool {
	return &x
}

func StringToPtr(x string) *string {
	return &x
}

func IntToPtr(x int) *int {
	return &x
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
