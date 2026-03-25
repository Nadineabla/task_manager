from enum import Enum
from sqlmodel import SQLModel, Field ,DateTime

class Status(str, Enum):
    TODO = "to-do"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    
class StatusUrlChoices(str, Enum):
    TODO = "to-do"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    
class TODOBase(SQLModel):
    name: str
    
class TODOCreate(TODOBase):
    pass

class TODOUpdate(TODOBase):
    status: Status
class TODOS(TODOBase, table=True):
    id: int = Field(default=None, primary_key=True)
    status: Status 
    
    
    
    
    
    
    
    
    
    
    
    
# class TODO(TODOID):
#     @validator("status", pre=True)
#     def title_case(cls, value):
#         return value.lower()
    
