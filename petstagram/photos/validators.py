# from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


# def validate_size(value):
#     if value > 5 * 1024 * 1024:
#         raise ValidationError('File too large')


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size: int, message=None):
        self.max_size = max_size
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"File must be {self.max_size}MB or less."

        self.__message = value

    def __call__(self, value):
        if value > self.max_size * 1024 * 1024:
            raise ValidationError(self.message)
