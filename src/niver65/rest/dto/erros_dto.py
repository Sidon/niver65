from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional

class RestErrorDetails(BaseModel):
    field: str
    issue: str
    location: str


class ResponseError(BaseModel):
    namespace: str
    informationLink: str
    code: str
    correlationId: Optional[str]
    debugId: str
    message: str
    name: str
    details: Optional[RestErrorDetails]