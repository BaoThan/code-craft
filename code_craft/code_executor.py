import os
import random
import shutil
import string
import subprocess
from dataclasses import dataclass
from enum import Enum

DEFAULT_TIMEOUT = 15


class Language(Enum):
    """
    Enum representing programming languages.
    """

    C = "c"
    CPP = "cpp"
    C_SHARP = "csharp"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    RUBY = "ruby"
    PERL = "perl"
    PHP = "php"
    GO = "go"
    RUST = "rust"


# Map a programming language enum to its corresponding file extension.
_LANGUAGE_TO_FILE_EXTENSIONS: dict[Language, str] = {
    Language.C: "c",
    Language.CPP: "cpp",
    Language.C_SHARP: "cs",
    Language.JAVA: "java",
    Language.JAVASCRIPT: "js",
    Language.PYTHON: "py",
    Language.RUBY: "rb",
    Language.PERL: "pl",
    Language.PHP: "php",
    Language.GO: "go",
    Language.RUST: "rs",
}

# Directory where all the temporary directories will be stored.
_TEMPDIR_PREFIX = "/tmp/code-craft/code"
_TEMP_NAME_LEN = 10


@dataclass
class CodeExecutionResult:
    """
    Represents a code execution result.
    """

    stdout: str | None
    stderr: str | None
    exit_code: int | None
    timeout: bool = False


def execute_code(language: Language, code: str) -> CodeExecutionResult:
    """
    Execute a piece of code.

    Args:
        language (Language): The programming language the code is written in.
        code (str): The piece of code to execute.
    """
    dirpath, main_file = __create_tempdir_and_paste_code(language, code)

    # Get the command to run the code based on given language
    run_cmds = __generate_run_command(language, dirpath, main_file)
    result = CodeExecutionResult(None, None, None, False)
    try:
        for i in range(len(run_cmds)):
            process = subprocess.Popen(
                run_cmds[i].split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate(timeout=DEFAULT_TIMEOUT)
            result = CodeExecutionResult(stdout, stderr, process.returncode)
            # Catch compliation failed
            if i == 0 and result.exit_code != 0:
                return result

    except subprocess.TimeoutExpired:
        process.kill()
        # Collect the child process exit status so the process does not become a zombie process
        process.wait()
        result = CodeExecutionResult(None, None, None, True)

    # Remove code temp directory
    shutil.rmtree(dirpath)

    return result


def __generate_run_command(language: Language, dir: str, filename: str) -> list[str]:
    """
    Generate a command to run a file based on the given language and filepath.
    """
    file_name_no_ext = ".".join(filename.split(".")[:-1])

    return {
        language.C: [f"gcc {dir}/{filename} -o {dir}/main", f"{dir}/main"],
        language.CPP: [f"g++ {dir}/{filename} -o {dir}/main", f"{dir}/main"],
        language.C_SHARP: [
            f"mcs -out:{dir}/{file_name_no_ext}.exe {dir}/{filename}",
            f"mono {dir}/{file_name_no_ext}.exe",
        ],
        language.JAVA: [
            f"javac -d {dir} {dir}/{filename}",
            f"java -cp {dir} {file_name_no_ext}",
        ],
        language.JAVASCRIPT: [f"node {dir}/{filename}"],
        language.PYTHON: [f"python3 {dir}/{filename}"],
        language.RUBY: [f"ruby {dir}/{filename}"],
        language.PERL: [f"perl {dir}/{filename}"],
        language.PHP: [f"php {dir}/{filename}"],
        language.GO: [f"go run {dir}/{filename}"],
        language.RUST: [
            f"rustc -o {dir}/{file_name_no_ext} {dir}/{filename}",
            f"{dir}/{file_name_no_ext}",
        ],
    }[language]


def __create_tempdir_and_paste_code(language: Language, code: str) -> tuple[str, str]:
    """
    Create a directory and paste the given code into a temporary file.
    Returns:
        Path to the temporary directory created.
    """
    random_dir = "".join(random.choices(string.ascii_letters, k=_TEMP_NAME_LEN))
    dirpath = f"{_TEMPDIR_PREFIX}/{random_dir}"
    os.makedirs(dirpath)

    main_file = f"main.{_LANGUAGE_TO_FILE_EXTENSIONS[language]}"
    if language == Language.JAVA:
        main_file = "Main.java"

    with open(f"{dirpath}/{main_file}", "x") as f:
        f.write(code)

    return dirpath, main_file
