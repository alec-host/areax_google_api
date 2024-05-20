from pydantic import BaseModel

class EmailSearch(BaseModel):
    search_words: str
    email: str

class UserInformation(BaseModel):
    email: str
    reference_number: str