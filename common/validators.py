from django.core.exceptions import ValidationError

def validate_name_length(value):
    min_length=2
    max_length=50
    if len(value)< min_length:
        raise ValidationError(f'Name must be at least {min_length} characters long.')
    if len(value)> max_length:
        raise ValidationError(f'Name must exceed {max_length} characters.')
    


