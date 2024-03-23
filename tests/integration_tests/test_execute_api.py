import subprocess

import requests

from tests.test_data.example_code import *

API_URL = "http://127.0.0.1:5000/execute"


def test_execute_api_working_cases() -> None:
    for lang, code in [
        ("c", C_HELLO_WORLD),
        ("cpp", CPP_HELLO_WORLD),
        ("go", GO_HELLO_WORLD),
        ("java", JAVA_HELLO_WORLD),
        ("javascript", JAVASCRIPT_HELLO_WORLD),
        ("perl", PERL_HELLO_WORLD),
        ("php", PHP_HELLO_WORLD),
        ("python", PYTHON_HELLO_WORLD),
        ("ruby", RUBY_HELLO_WORLD),
        ("rust", RUST_HELLO_WORLD),
    ]:
        print(f"Testing for {lang}")
        data = {"language": lang, "code": code}
        response = requests.post(API_URL, data=data)
        print(response.json())

        assert response.status_code == 200
        assert response.json()["data"]["exit_code"] == 0
        assert response.json()["data"]["stderr"] == ""
        assert response.json()["data"]["stdout"] == "Hello, world!\n"


def test_execute_api_timeout_case() -> None:
    def count_processes() -> int:
        ps_output = subprocess.run(
            "docker exec -it code-craft ps ax --no-header",
            capture_output=True,
            shell=True,
        )
        return len(list(filter(None, ps_output.stdout.decode().split("\n"))))

    ps_count_prerun = count_processes()

    data = {"language": "python", "code": "while True: pass"}
    response = requests.post(API_URL, data=data)

    ps_count_postrun = count_processes()

    assert response.status_code == 200
    assert response.json()["data"] == None
    assert not response.json()["success"]
    assert response.json()["time_out"]
    assert ps_count_prerun == ps_count_postrun
