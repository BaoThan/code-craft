# Code Craft
![](https://github.com/BaoThan/code-craft/actions/workflows/stylelint-pipeline.yml/badge.svg?branch=main)

Code Craft is a REST API to execute your code in a chosen language.
You can simple send in a POST request with the code you want to run and the language it is written in.
The server will execute it and return the output along with the exit code.

---

<p align="center">
  <img src="https://media.giphy.com/media/JqmupuTVZYaQX5s094/giphy.gif">
</p>

---

#### Base URL: https://code-craft-grso.onrender.com

---

### Execute Code API
POST `/execute`

##### Body Form-Data Arguments:
* __code__ (string): Your beautiful code 💫
* __language__ (string): The language your code is written in. The supported languages are `c`, `cpp`, `csharp`, `go`, `java`, `javascript`, `perl`, `php`, `python`, `ruby`, `rust`.

#### Response Format:
The API will return a JSON with the following fields:
* __success__ (bool): Whether the input was received and executed.
* __time_out__ (bool): Whether the code run time has exceeded 15 seconds. `success` field will be false if `time_out` is true.
* __data__ (map): Null if `success` is false. Otherwise, this field is a map with the following inner fields:
    * __exit_code__ (int): Status code after executing the program
    * __stdout__ (string): Output to stdout
    * __stderr__ (string): Output to stderr

##### Example:
Example calling the API in Python:
```python
import requests

url = "https://code-craft-grso.onrender.com/execute"
payload = {
    'language': 'python',
    'code': 'print("hello world")'
}
response = requests.request("POST", url, headers={}, data=payload)
print(response.json())
# Output:
# {'data': {'exit_code': 0, 'stderr': '', 'stdout': 'hello world\n'}, 'success': True, 'time_out': False}
```

### Languages API
GET `/languages`

Simple GET API returning the supported languages, which are `c`, `cpp`, `csharp`, `go`, `java`, `javascript`, `perl`, `php`, `python`, `ruby`, `rust`.
