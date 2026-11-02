from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def file_size_validator(max_size_mb: int):
    max_size = max_size_mb * 1024 * 1024

    def validator(file):
        if file.size > max_size:
            raise ValidationError(f"File size cannot exceed {max_size_mb}MB.")

    return validator


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size_mb: int):
        self.max_size_mb = max_size_mb
        self.max_size = max_size_mb * 1024 * 1024

    def __call__(self, file):
        if file.size > self.max_size:
            raise ValidationError(f"File size cannot exceed {self.max_size_mb}MB.")
