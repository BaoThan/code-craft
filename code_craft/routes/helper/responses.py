from dataclasses import dataclass

from flask import jsonify
from flask import Response


@dataclass
class ExecutionResult:
    stdout: str | None
    stderr: str | None
    exit_code: int | None
    time_out: bool

    def to_flask_response(self) -> tuple[Response, int]:
        success = not self.time_out
        data = (
            {
                "stdout": self.stdout,
                "stderr": self.stderr,
                "exit_code": self.exit_code,
            }
            if not self.time_out
            else None
        )
        return (
            jsonify(
                {
                    "success": success,
                    "time_out": self.time_out,
                    "data": data,
                }
            ),
            200,
        )


@dataclass
class FailureResult:
    error_messsage: str

    def to_flask_response(self) -> tuple[Response, int]:
        return jsonify({"success": False, "error_message": self.error_messsage}), 400
