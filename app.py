from fastapi import FastAPI, HTTPException, Depends, Query, Path, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import os

# Create FastAPI app
app = FastAPI(
    title="User Management API",
    description="A comprehensive API for managing users with full CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models for request/response
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., description="User's email address")
    age: int = Field(..., ge=0, le=150, description="User's age")
    bio: Optional[str] = Field(None, max_length=500, description="User's biography")

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    email: Optional[str] = Field(None, description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    bio: Optional[str] = Field(None, max_length=500, description="User's biography")

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to convert DB model to response model
def user_db_to_response(user_db: UserDB) -> UserResponse:
    return UserResponse(
        id=user_db.id,
        name=user_db.name,
        email=user_db.email,
        age=user_db.age,
        bio=user_db.bio,
        created_at=user_db.created_at,
        updated_at=user_db.updated_at
    )

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to User Management API", "docs": "/docs"}

@app.post("/users", response_model=UserResponse, status_code=201, tags=["Users"])
async def create_user(
    user: UserCreate = Body(..., description="User data to create"),
    db: Session = Depends(get_db),
    x_api_key: Optional[str] = Header(None, description="API Key for authentication")
):
    """
    Create a new user.
    
    - **name**: User's full name (required)
    - **email**: User's email address (required, must be unique)
    - **age**: User's age (required, between 0-150)
    - **bio**: User's biography (optional)
    - **x_api_key**: API key for authentication (optional header)
    """
    # Check if user with email already exists
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return user_db_to_response(db_user)

@app.get("/users", response_model=List[UserResponse], tags=["Users"])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    name: Optional[str] = Query(None, description="Filter users by name (partial match)"),
    min_age: Optional[int] = Query(None, ge=0, description="Minimum age filter"),
    max_age: Optional[int] = Query(None, ge=0, description="Maximum age filter"),
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None, description="Authorization header")
):
    """
    Get all users with optional filtering and pagination.
    
    - **skip**: Number of users to skip (pagination)
    - **limit**: Maximum number of users to return (pagination)
    - **name**: Filter users by name (partial match)
    - **min_age**: Filter users by minimum age
    - **max_age**: Filter users by maximum age
    - **authorization**: Authorization header (optional)
    """
    query = db.query(UserDB)
    
    # Apply filters
    if name:
        query = query.filter(UserDB.name.contains(name))
    if min_age is not None:
        query = query.filter(UserDB.age >= min_age)
    if max_age is not None:
        query = query.filter(UserDB.age <= max_age)
    
    # Apply pagination
    users = query.offset(skip).limit(limit).all()
    
    return [user_db_to_response(user) for user in users]

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user_by_id(
    user_id: int = Path(..., gt=0, description="The ID of the user to retrieve"),
    db: Session = Depends(get_db),
    x_user_id: Optional[str] = Header(None, description="User ID header for tracking")
):
    """
    Get a specific user by ID.
    
    - **user_id**: The ID of the user to retrieve (path parameter)
    - **x_user_id**: User ID header for tracking (optional header)
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_db_to_response(user)

@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user(
    user_id: int = Path(..., gt=0, description="The ID of the user to update"),
    user: UserCreate = Body(..., description="Complete user data to update"),
    db: Session = Depends(get_db),
    x_api_key: Optional[str] = Header(None, description="API Key for authentication")
):
    """
    Update a user completely (PUT - replaces all fields).
    
    - **user_id**: The ID of the user to update (path parameter)
    - **user**: Complete user data (all fields required)
    - **x_api_key**: API key for authentication (optional header)
    """
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is being changed and if it's already taken
    if user.email != db_user.email:
        existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update all fields
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    
    return user_db_to_response(db_user)

@app.patch("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def partial_update_user(
    user_id: int = Path(..., gt=0, description="The ID of the user to partially update"),
    user: UserUpdate = Body(..., description="Partial user data to update"),
    db: Session = Depends(get_db),
    x_api_key: Optional[str] = Header(None, description="API Key for authentication")
):
    """
    Partially update a user (PATCH - updates only provided fields).
    
    - **user_id**: The ID of the user to update (path parameter)
    - **user**: Partial user data (only fields to update)
    - **x_api_key**: API key for authentication (optional header)
    """
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is being changed and if it's already taken
    if user.email is not None and user.email != db_user.email:
        existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update only provided fields
    user_data = user.dict(exclude_unset=True)
    for field, value in user_data.items():
        setattr(db_user, field, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    
    return user_db_to_response(db_user)

@app.delete("/users/{user_id}", status_code=204, tags=["Users"])
async def delete_user(
    user_id: int = Path(..., gt=0, description="The ID of the user to delete"),
    db: Session = Depends(get_db),
    x_api_key: Optional[str] = Header(None, description="API Key for authentication")
):
    """
    Delete a user by ID.
    
    - **user_id**: The ID of the user to delete (path parameter)
    - **x_api_key**: API key for authentication (optional header)
    """
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    
    return None

@app.get("/users/search/{search_term}", response_model=List[UserResponse], tags=["Users"])
async def search_users(
    search_term: str = Path(..., min_length=1, description="Search term to find users"),
    db: Session = Depends(get_db),
    content_type: Optional[str] = Header(None, description="Content type header")
):
    """
    Search users by name or email containing the search term.
    
    - **search_term**: Search term to find users (path parameter)
    - **content_type**: Content type header (optional header)
    """
    users = db.query(UserDB).filter(
        (UserDB.name.contains(search_term)) | (UserDB.email.contains(search_term))
    ).all()
    
    return [user_db_to_response(user) for user in users]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 