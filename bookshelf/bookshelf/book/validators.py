from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UpperValueValidator:
    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = "Description must start with an uppercase letter."
        else:
            self.__message = value

    def __call__(self, value: str, *args, **kwargs):
        if value[0] != value[0].upper() and value[0] not in ('"', "'", '“', '”', '‘', '’', '„', '«', '»'):
            raise ValidationError("The text must start with an uppercase letter or an allowed quotation symbol.")
