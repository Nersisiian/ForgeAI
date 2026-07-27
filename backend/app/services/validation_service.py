import subprocess
import tempfile
import os
from typing import Tuple, List
import structlog

logger = structlog.get_logger(__name__)


class ValidationService:
    @staticmethod
    async def lint_code(file_path: str, content: str) -> Tuple[bool, List[str]]:
        """Run ruff on the given file content."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            tmp_path = f.name
        try:
            result = subprocess.run(  # noqa: ASYNC221
                ["ruff", "check", "--select=E,F,W", tmp_path],
                capture_output=True,
                text=True,
            )
            errors = result.stdout.splitlines()
            return result.returncode == 0, errors
        finally:
            os.unlink(tmp_path)

    @staticmethod
    async def type_check(file_path: str, content: str) -> Tuple[bool, List[str]]:
        """Run mypy on the file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            tmp_path = f.name
        try:
            result = subprocess.run(  # noqa: ASYNC221
                ["mypy", "--strict", tmp_path], capture_output=True, text=True
            )
            errors = result.stdout.splitlines()
            return result.returncode == 0, errors
        finally:
            os.unlink(tmp_path)
