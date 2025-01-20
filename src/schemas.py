from pydantic import BaseModel, Field, constr


class ApplicationIn(BaseModel):
    user_name: constr(max_length=25)
    description: constr(max_length=255)


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Number of page (starts from 1)")
    size: int = Field(default=10, ge=1, le=100, description="Qty of items per page")