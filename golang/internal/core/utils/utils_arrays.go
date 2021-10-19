package utils

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

import (
	"reflect"
)

/* ---------------------------------------------------------------- *
 * METHOD array contains
 * ---------------------------------------------------------------- */

func ArrayContains(x interface{}, elem interface{}) bool {
	xAsArray := reflect.ValueOf(x)
	if xAsArray.Kind() == reflect.Slice {
		for i := 0; i < xAsArray.Len(); i++ {
			if xAsArray.Index(i).Interface() == elem {
				return true
			}
		}
	}
	return false
}

// func ListComprehension(x interface{}, cond (interface{}) bool) bool {
// 	xAsArray := reflect.ValueOf(x)
// 	if xAsArray.Kind() == reflect.Slice {
// 		for i := 0; i < xAsArray.Len(); i++ {
// 			if xAsArray.Index(i).Interface() == elem {
// 				return true
// 			}
// 		}
// 	}
// 	return false
// }

/* ---------------------------------------------------------------- *
 * METHOD array contains
 * ---------------------------------------------------------------- */

func UniqueListOfStrings(X []string) []string {
	var ok bool
	m := map[string]bool{}
	X_unique := []string{}
	for _, x := range X {
		if _, ok = m[x]; !ok {
			X_unique = append(X_unique, x)
		}
	}
	return X_unique
}

/* ---------------------------------------------------------------- *
 * METHOD get value from array of unknown length
 * ---------------------------------------------------------------- */

func GetArrayStringValue(arr *[]string, index int, Default string) string {
	if arr != nil && len(*arr) > index {
		return (*arr)[index]
	}
	return Default
}

func GetArrayBoolValue(arr *[]bool, index int, Default bool) bool {
	if arr != nil && len(*arr) > index {
		return (*arr)[index]
	}
	return Default
}

func GetArrayIntValue(arr *[]int, index int, Default int) int {
	if arr != nil && len(*arr) > index {
		return (*arr)[index]
	}
	return Default
}

func GetArrayInterfaceValue(arr *[](interface{}), index int, Default interface{}) interface{} {
	if arr != nil && len(*arr) > index {
		return (*arr)[index]
	}
	return Default
}
