from rest_framework.exceptions import ValidationError
from urllib.parse import urlparse

def validate_youtube_url(value):
    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()
    if 'youtube.com' not in domain and 'youtu.be' not in domain:
        raise ValidationError('Ссылка должна быть на youtube.com или youtu.be')
