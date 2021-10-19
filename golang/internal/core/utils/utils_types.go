package utils

import "reflect"

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

func ExpandPtrToBool(p *bool) interface{} {
	if p != nil {
		return *p
	}
	return p
}

func PtrToBool(p *bool, Default bool) bool {
	if p != nil {
		return *p
	}
	return Default
}

func ExpandPtrToString(p *string) interface{} {
	if p != nil {
		return *p
	}
	return p
}

func PtrToString(p *string, Default string) string {
	if p != nil {
		return *p
	}
	return Default
}

func ExpandPtrToInt(p *int) interface{} {
	if p != nil {
		return *p
	}
	return p
}

func PtrToInt(p *int, Default int) int {
	if p != nil {
		return *p
	}
	return Default
}

/* ---------------------------------------------------------------- *
 * METHOD interface to (ptr to) array
 * ---------------------------------------------------------------- */

func InterfaceToArray(x interface{}) *[]interface{} {
	if reflect.TypeOf(x).Kind() == reflect.Slice {
		var xSlice []interface{} = []interface{}{}
		var xConverted = reflect.ValueOf(x)
		for i := 0; i < xConverted.Len(); i++ {
			xSlice = append(xSlice, xConverted.Index(i).Interface())
		}
		return &xSlice
	}
	return nil
}
