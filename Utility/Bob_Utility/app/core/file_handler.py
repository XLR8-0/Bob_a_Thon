"""
Secure file handling utilities for the Enterprise Payload Toolkit
"""

import os
import tempfile
from pathlib import Path
from typing import BinaryIO, Optional, Union

import aiofiles

from app.core.exceptions import FileSizeError, FileTypeError, ResourceError
from app.core.logger import LoggerMixin


class FileHandler(LoggerMixin):
    """
    Handles secure file operations with validation and size limits
    """

    def __init__(
        self,
        max_size_bytes: int = 52428800,  # 50MB default
        allowed_extensions: Optional[list[str]] = None,
        temp_dir: Optional[str] = None,
    ) -> None:
        """
        Initialize FileHandler

        Args:
            max_size_bytes: Maximum allowed file size in bytes
            allowed_extensions: List of allowed file extensions (e.g., ['.xml', '.json'])
            temp_dir: Temporary directory for file operations
        """
        self.max_size_bytes = max_size_bytes
        self.allowed_extensions = allowed_extensions or [
            ".xml",
            ".json",
            ".yaml",
            ".yml",
            ".log",
            ".txt",
            ".env",
            ".conf",
            ".config",
        ]
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self._ensure_temp_dir()

    def _ensure_temp_dir(self) -> None:
        """Ensure temporary directory exists"""
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)

    def validate_file_size(self, file_path: Union[str, Path]) -> None:
        """
        Validate file size against maximum allowed size

        Args:
            file_path: Path to the file

        Raises:
            FileSizeError: If file size exceeds maximum
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise ResourceError(f"File not found: {file_path}")

        file_size = file_path.stat().st_size
        if file_size > self.max_size_bytes:
            raise FileSizeError(
                f"File size ({file_size} bytes) exceeds maximum allowed "
                f"({self.max_size_bytes} bytes)",
                details={
                    "file_size": file_size,
                    "max_size": self.max_size_bytes,
                    "file_path": str(file_path),
                },
            )

    def validate_file_extension(self, file_path: Union[str, Path]) -> None:
        """
        Validate file extension against allowed extensions

        Args:
            file_path: Path to the file

        Raises:
            FileTypeError: If file extension is not allowed
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        if extension not in self.allowed_extensions:
            raise FileTypeError(
                f"File extension '{extension}' is not allowed",
                details={
                    "extension": extension,
                    "allowed_extensions": self.allowed_extensions,
                    "file_path": str(file_path),
                },
            )

    def validate_file(self, file_path: Union[str, Path]) -> None:
        """
        Validate file size and extension

        Args:
            file_path: Path to the file

        Raises:
            FileSizeError: If file size exceeds maximum
            FileTypeError: If file extension is not allowed
        """
        self.validate_file_size(file_path)
        self.validate_file_extension(file_path)
        self.logger.info(f"File validation successful: {file_path}")

    def read_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Read file content with validation

        Args:
            file_path: Path to the file
            encoding: File encoding (default: utf-8)

        Returns:
            File content as string

        Raises:
            ResourceError: If file cannot be read
        """
        file_path = Path(file_path)
        self.validate_file(file_path)

        try:
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
            self.logger.info(f"Successfully read file: {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {e}")
            raise ResourceError(
                f"Failed to read file: {e}",
                details={"file_path": str(file_path), "error": str(e)},
            )

    async def read_file_async(
        self, file_path: Union[str, Path], encoding: str = "utf-8"
    ) -> str:
        """
        Asynchronously read file content with validation

        Args:
            file_path: Path to the file
            encoding: File encoding (default: utf-8)

        Returns:
            File content as string

        Raises:
            ResourceError: If file cannot be read
        """
        file_path = Path(file_path)
        self.validate_file(file_path)

        try:
            async with aiofiles.open(file_path, "r", encoding=encoding) as f:
                content = await f.read()
            self.logger.info(f"Successfully read file async: {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"Failed to read file async {file_path}: {e}")
            raise ResourceError(
                f"Failed to read file: {e}",
                details={"file_path": str(file_path), "error": str(e)},
            )

    def read_file_chunks(
        self, file_path: Union[str, Path], chunk_size: int = 8192, encoding: str = "utf-8"
    ):
        """
        Read file in chunks (generator for large files)

        Args:
            file_path: Path to the file
            chunk_size: Size of each chunk in bytes
            encoding: File encoding (default: utf-8)

        Yields:
            File content chunks

        Raises:
            ResourceError: If file cannot be read
        """
        file_path = Path(file_path)
        self.validate_file(file_path)

        try:
            with open(file_path, "r", encoding=encoding) as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
            self.logger.info(f"Successfully read file in chunks: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to read file chunks {file_path}: {e}")
            raise ResourceError(
                f"Failed to read file: {e}",
                details={"file_path": str(file_path), "error": str(e)},
            )

    def write_file(
        self, file_path: Union[str, Path], content: str, encoding: str = "utf-8"
    ) -> None:
        """
        Write content to file

        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding (default: utf-8)

        Raises:
            ResourceError: If file cannot be written
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(file_path, "w", encoding=encoding) as f:
                f.write(content)
            self.logger.info(f"Successfully wrote file: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to write file {file_path}: {e}")
            raise ResourceError(
                f"Failed to write file: {e}",
                details={"file_path": str(file_path), "error": str(e)},
            )

    async def write_file_async(
        self, file_path: Union[str, Path], content: str, encoding: str = "utf-8"
    ) -> None:
        """
        Asynchronously write content to file

        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding (default: utf-8)

        Raises:
            ResourceError: If file cannot be written
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            async with aiofiles.open(file_path, "w", encoding=encoding) as f:
                await f.write(content)
            self.logger.info(f"Successfully wrote file async: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to write file async {file_path}: {e}")
            raise ResourceError(
                f"Failed to write file: {e}",
                details={"file_path": str(file_path), "error": str(e)},
            )

    def create_temp_file(
        self, content: str, suffix: str = ".tmp", encoding: str = "utf-8"
    ) -> Path:
        """
        Create a temporary file with content

        Args:
            content: Content to write
            suffix: File suffix/extension
            encoding: File encoding (default: utf-8)

        Returns:
            Path to the temporary file

        Raises:
            ResourceError: If temp file cannot be created
        """
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=suffix,
                dir=self.temp_dir,
                delete=False,
                encoding=encoding,
            ) as f:
                f.write(content)
                temp_path = Path(f.name)
            self.logger.info(f"Created temporary file: {temp_path}")
            return temp_path
        except Exception as e:
            self.logger.error(f"Failed to create temp file: {e}")
            raise ResourceError(
                f"Failed to create temporary file: {e}",
                details={"error": str(e)},
            )

    def delete_file(self, file_path: Union[str, Path]) -> None:
        """
        Safely delete a file

        Args:
            file_path: Path to the file

        Raises:
            ResourceError: If file cannot be deleted
        """
        file_path = Path(file_path)
        try:
            if file_path.exists():
                file_path.unlink()
                self.logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to delete file {file_path}: {e}")
            raise ResourceError(
                f"Failed to delete file: {e}",
                details={"file_path": str(file_path), "error": str(e)},
            )

    def get_file_info(self, file_path: Union[str, Path]) -> dict:
        """
        Get file information

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file information

        Raises:
            ResourceError: If file info cannot be retrieved
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise ResourceError(f"File not found: {file_path}")

        try:
            stat = file_path.stat()
            return {
                "path": str(file_path),
                "name": file_path.name,
                "extension": file_path.suffix,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
            }
        except Exception as e:
            self.logger.error(f"Failed to get file info {file_path}: {e}")
            raise ResourceError(
                f"Failed to get file info: {e}",
                details={"file_path": str(file_path), "error": str(e)},
            )

# Made with Bob
