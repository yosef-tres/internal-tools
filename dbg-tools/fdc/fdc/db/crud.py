"""CRUD operations for interacting with the database."""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from fdc.db.models import Collection, CollectionPart


# Collection CRUD operations
def create_collection(db: Session, name: str, description: Optional[str] = None) -> Collection:
    """Create a new collection in the database."""
    db_collection = Collection(name=name, description=description)
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


def get_collection(db: Session, collection_id: int) -> Optional[Collection]:
    """Get a collection by its ID."""
    return db.query(Collection).filter(Collection.id == collection_id).first()


def get_collections(db: Session, skip: int = 0, limit: int = 100) -> List[Collection]:
    """Get all collections with pagination."""
    return db.query(Collection).order_by(Collection.id).offset(skip).limit(limit).all()


def update_collection(db: Session, collection_id: int, data: Dict[str, Any]) -> Optional[Collection]:
    """Update a collection by its ID."""
    db_collection = get_collection(db, collection_id)
    if db_collection:
        for key, value in data.items():
            setattr(db_collection, key, value)
        db.commit()
        db.refresh(db_collection)
    return db_collection


def delete_collection(db: Session, collection_id: int) -> bool:
    """Delete a collection by its ID."""
    db_collection = get_collection(db, collection_id)
    if db_collection:
        db.delete(db_collection)
        db.commit()
        return True
    return False


# CollectionPart CRUD operations
def create_collection_part(
    db: Session, collection_id: int, name: str, content: Optional[str] = None, 
    data: Optional[str] = None, order: Optional[int] = 0
) -> CollectionPart:
    """Create a new collection part in the database."""
    db_part = CollectionPart(
        collection_id=collection_id,
        name=name,
        content=content,
        data=data,
        order=order
    )
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part


def get_collection_part(db: Session, part_id: int) -> Optional[CollectionPart]:
    """Get a collection part by its ID."""
    return db.query(CollectionPart).filter(CollectionPart.id == part_id).first()


def get_collection_parts(
    db: Session, collection_id: int, skip: int = 0, limit: int = 100
) -> List[CollectionPart]:
    """Get all parts for a specific collection with pagination."""
    return db.query(CollectionPart)\
        .filter(CollectionPart.collection_id == collection_id)\
        .order_by(CollectionPart.order)\
        .offset(skip)\
        .limit(limit)\
        .all()


def update_collection_part(db: Session, part_id: int, data: Dict[str, Any]) -> Optional[CollectionPart]:
    """Update a collection part by its ID."""
    db_part = get_collection_part(db, part_id)
    if db_part:
        for key, value in data.items():
            setattr(db_part, key, value)
        db.commit()
        db.refresh(db_part)
    return db_part


def delete_collection_part(db: Session, part_id: int) -> bool:
    """Delete a collection part by its ID."""
    db_part = get_collection_part(db, part_id)
    if db_part:
        db.delete(db_part)
        db.commit()
        return True
    return False
