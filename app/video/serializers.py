from pydantic import BaseModel, ValidationError, validator


class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError(
                'must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError(
                'passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert str(v).isalnum(), 'must be alphanumeric'
        return v


class VideoSubResponseSerializer(BaseModel):
    id: str


class VideoResponseSerializer(BaseModel):
    id: str
    body: list[VideoSubResponseSerializer]
