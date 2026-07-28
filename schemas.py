from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    image_filename: str

    class Config:
        from_attributes = True
