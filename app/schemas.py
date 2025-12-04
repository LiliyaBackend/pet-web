from pydantic import BaseModel


class MathItemSchema(BaseModel):
    id: str
    name: str
    desc: str
    parameterized: int
