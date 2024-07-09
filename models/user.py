from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    firstName: str
    lastName: str
    username: str
    email: str
    password: str
    company: str
    companyEmail: str
    role: str
    skills: Optional[List[str]]
    face_encoding: Optional[List[str]]
    profileStatus: str
    profilePicture: Optional[str] = None

class User_login(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    firstName: str
    lastName: str
    username: str
    email: str
    company: str
    role: str
    profileStatus: str
    skills: Optional[List[str]]
    profilePicture: Optional[str] = None
    
class UserSkills(BaseModel):
    profileStatus: str = "Active"
    role: str
    email: str
    companyEmail: str
    python: bool = False  
    javaScript: bool = False  
    java: bool = False  
    html: bool = False  
    c: bool = False  
    c_sharp: bool = False  
    c_plusplus: bool = False  
    php: bool = False  
    ruby: bool = False  
    swift: bool = False  
    go: bool = False  
    typeScript: bool = False  
    css: bool = False  
    experienced_years: int = 0
    level: str = "Starter"
       
    

class UpdateProfileStatusRequest(BaseModel):
    email: str
    profileStatus: str


