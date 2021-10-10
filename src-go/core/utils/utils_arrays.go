package utils

import (
	"reflect"
)

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
