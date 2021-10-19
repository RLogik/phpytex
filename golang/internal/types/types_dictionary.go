package types

/* ---------------------------------------------------------------- *
 * IMPORTS
 * ---------------------------------------------------------------- */

//

/* ---------------------------------------------------------------- *
 * TYPES
 * ---------------------------------------------------------------- */

type Dictionary struct {
	values *map[string]interface{}
}

/* ---------------------------------------------------------------- *
 * METHODS
 * ---------------------------------------------------------------- */

func (kw *Dictionary) Init() {
	kw.values = nil
}

func (kw Dictionary) HasKey(key string) bool {
	if kw.values == nil {
		return false
	}
	_, ok := (*kw.values)[key]
	return ok
}

func (kw Dictionary) GetValues() *(map[string]interface{}) {
	return kw.values
}

func (kw Dictionary) GetValue(key string) *interface{} {
	var values = kw.GetValues()
	if values != nil {
		if value, ok := (*values)[key]; ok {
			return &value
		}
	}
	return nil
}

func (kw *Dictionary) SetValues(values *map[string]interface{}) {
	kw.values = values
}

func (kw *Dictionary) SetValue(key string, value interface{}) {
	var values = kw.GetValues()
	if values != nil {
		(*values)[key] = value
	}
	kw.values = values
}
