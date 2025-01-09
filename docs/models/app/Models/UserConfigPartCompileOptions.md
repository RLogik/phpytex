# UserConfigPartCompileOptions
## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
| **root** | **String** | Filename of start of transpilation   (phpytex) -&gt; py -&gt; tex -&gt; pdf | [optional] [default to root.tex] |
| **python-path** | **String** | User choice of python path (e.g. local venv). | [optional] [default to null] |
| **transpiled** | **String** | Filename of intermediate transpilation result   phpytex -&gt; (py) -&gt; tex -&gt; pdf | [optional] [default to phpytex_transpiled.py] |
| **output** | **String** | Filename of end of transpilation result   phpytex -&gt; py -&gt; (tex) -&gt; pdf | [optional] [default to main.tex] |
| **debug** | **Boolean** |  | [optional] [default to false] |
| **compile-latex** | **Boolean** |  | [optional] [default to false] |
| **insert-bib** | **Boolean** |  | [optional] [default to false] |
| **backend-bib** | **String** |  | [optional] [default to bibtex] |
| **comments** | [**EnumCommentsOptions**](EnumCommentsOptions.md) |  | [optional] [default to null] |
| **censor-symbol** | **String** |  | [optional] [default to ########] |
| **show-structure** | **Boolean** |  | [optional] [default to false] |
| **max-length** | **Integer** |  | [optional] [default to 10000] |
| **tabs** | **Boolean** |  | [optional] [default to false] |
| **spaces** | **Integer** |  | [optional] [default to 4] |
| **offset** | **String** |  | [optional] [default to ] |
| **align** | **Boolean** |  | [optional] [default to true] |
| **seed** | **Integer** |  | [optional] [default to null] |
| **legacy** | **Boolean** |  | [optional] [default to false] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

