from pydantic import BaseModel, Field, validator, root_validator, model_validator


class UserForm(BaseModel):
    login: str = Field(pattern="\\w{2,16}")
    password1: str = Field(pattern="\\w{4,32}")
    password2: str = Field(pattern="\\w{4,32}")
    name: str = Field(pattern="\\w{4,32}")
    email: str = Field(pattern="\\w+@(\\w+[.])+\\w+")
    advertising: str = None

    # Root validator to check if passwords match
    @model_validator(mode='after')
    def check_passwords_match(cls, values) -> dict:
        password = values.password1
        confirm_password = values.password2

        if password != confirm_password:
            raise ValueError('Passwords do not match.')

        return values

