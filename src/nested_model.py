from typing import List, Optional, Date
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    postal_code: str
    
class User(BaseModel):
    id: int
    name: str
    address: Address
    created_at: Date

address = Address(
    street="838 something",
    postal_code="222001"
)

user = User(
    id=1,
    name="Hamza",
    address=address
)

class Comment(BaseModel):
    id: int
    content: str
    replies: Optional[List['Comment']] = None # self -referencing
    
Comment.model_rebuild() #for performance improvement

comment = Comment(
    id=1,
    content="How are you",
    replies=[
        Comment(id=2, content="i am fine"),
        Comment(id=3, content="i am good", replies=[
                Comment(id=4, content="yeah really")
            ]),
        
    ]
)