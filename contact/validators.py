import re
from django.core.exceptions import ValidationError
def validate_name(value):
        if not re.match("^[a-zA-z\s]*$",value):
            raise ValidationError("Name must contain only the letter and spaces")

        if len(value)<=2:
            raise ValidationError("Name must be more than the 2 characters")


def validate_message(value):
     if len(value)<=10:
          raise ValidationError("Please provide the message longer the 10 characters")