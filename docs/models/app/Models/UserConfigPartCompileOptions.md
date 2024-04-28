# UserConfigPartCompileOptions
## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**root** | [**String**](string.md) | Filename of start of transpilation   (phpytex) -&gt; py -&gt; tex -&gt; pdf | [optional] [default to root.tex]
**pythonMinuspath** | [**String**](string.md) | User choice of python path (e.g. local venv). | [optional] [default to null]
**transpiled** | [**String**](string.md) | Filename of intermediate transpilation result   phpytex -&gt; (py) -&gt; tex -&gt; pdf | [optional] [default to phpytex_transpiled.py]
**output** | [**String**](string.md) | Filename of end of transpilation result   phpytex -&gt; py -&gt; (tex) -&gt; pdf | [optional] [default to main.tex]
**debug** | [**Boolean**](boolean.md) |  | [optional] [default to false]
**compileMinuslatex** | [**Boolean**](boolean.md) |  | [optional] [default to false]
**insertMinusbib** | [**Boolean**](boolean.md) |  | [optional] [default to false]
**backendMinusbib** | [**String**](string.md) |  | [optional] [default to bibtex]
**comments** | [**EnumCommentsOptions**](EnumCommentsOptions.md) |  | [optional] [default to null]
**censorMinussymbol** | [**String**](string.md) |  | [optional] [default to ########]
**showMinusstructure** | [**Boolean**](boolean.md) |  | [optional] [default to false]
**maxMinuslength** | [**Integer**](integer.md) |  | [optional] [default to 10000]
**tabs** | [**Boolean**](boolean.md) |  | [optional] [default to false]
**spaces** | [**Integer**](integer.md) |  | [optional] [default to 4]
**offset** | [**String**](string.md) |  | [optional] [default to ]
**align** | [**Boolean**](boolean.md) |  | [optional] [default to true]
**seed** | [**Integer**](integer.md) |  | [optional] [default to null]
**legacy** | [**Boolean**](boolean.md) |  | [optional] [default to false]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

