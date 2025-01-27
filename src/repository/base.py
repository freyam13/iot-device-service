from typing import Dict, Generic, List, Optional, TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base

T = TypeVar("T", bound=BaseModel)

DATABASE_URL = "postgresql://user:password@localhost:5432/ambient"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# TODO: move to application initialization
Base.metadata.create_all(engine)

class EntityModel(Base):
    """
    Base ORM model.
    """
    id = Column(String, primary_key=True, index=True)

class DB(Generic[T]):
    """
    Generic PostgresSQL storage implementation for entity persistence.

    Type Parameters:
        T: type of entity being stored (Pydantic BaseModel)
    """

    def __init__(self, orm_model: Type[EntityModel]) -> None:
        self.orm_model = orm_model

    def create(self, id: str, item: T) -> T:
        """
        Create a new item in the database.

        Arguments:
            id: unique identifier for the item
            item: item to store

        Returns:
            stored item

        Raises:
            ValueError: if item with id already exists
        """
        with SessionLocal() as session:
            if session.query(self.orm_model).filter_by(id=id).first():
                raise ValueError(f"Item with id {id} already exists.")

            item = self.orm_model(id=id, **item.model_dump())
            session.add(item)
            session.commit()
            session.refresh(item)

        return item

    def get(self, id: str) -> Optional[T]:
        """
        Retrieve an item by its identifier.

        Arguments:
            id: identifier of the item to retrieve

        Returns:
            item if found, None otherwise
        """
        with SessionLocal() as session:
            db_item = session.query(self.orm_model).filter_by(id=id).first()
            return db_item if db_item else None

    def list(self) -> list[Type[EntityModel]]:
        """
        List all items in the database.

        Returns:
            list of all stored items
        """
        with SessionLocal() as session:
            return session.query(self.orm_model).all()

    def update(self, id: str, item: T) -> T:
        """
        Update an existing item.

        Arguments:
            id: identifier of the item to update
            item: new item data

        Returns:
            updated item

        Raises:
            ValueError: if item with id does not exist
        """
        with SessionLocal() as session:
            db_item = session.query(self.orm_model).filter_by(id=id).first()
            if not db_item:
                raise ValueError(f"Item with id {id} not found")

            for key, value in item.dict().items():
                setattr(db_item, key, value)

            session.commit()
            session.refresh(db_item)

            return item

    def delete(self, id: str) -> None:
        """
        Delete an item from the database.

        Arguments:
            id: identifier of the item to delete

        Raises:
            ValueError: if item with id does not exist
        """
        with SessionLocal() as session:
            db_item = session.query(self.orm_model).filter_by(id=id).first()
            if not db_item:
                raise ValueError(f"Item with id {id} not found")

            session.delete(db_item)
            session.commit()
