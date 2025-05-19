"""Data functions for the Fast & Dirty Commit app."""

import random
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session
from fdc.db.models import Collection, CollectionPart
from fdc.db.crud import (
    get_collections, get_collection_parts,
    create_collection, create_collection_part,
)

def get_mock_transactions(count=10):
    """Generate mock transaction data for demonstration."""
    mock_txns = []
    blockchains = ["Ethereum", "Polygon", "Arbitrum", "Optimism", "BSC"]
    status = ["Pending", "Completed", "Failed"]
    
    for i in range(count):
        mock_txns.append({
            "id": f"0x{random.randint(10**30, 10**31):x}",
            "blockchain": random.choice(blockchains),
            "from_address": f"0x{random.randint(10**30, 10**31):x}",
            "to_address": f"0x{random.randint(10**30, 10**31):x}",
            "value": round(random.uniform(0.001, 10.0), 6),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": random.choice(status),
            "gas_used": random.randint(21000, 250000)
        })
    return mock_txns

def get_mock_entities(count=5):
    """Generate mock entity data for demonstration."""
    entity_types = ["Address", "Contract", "Token", "NFT", "Project"]
    tags = ["DEX", "CEX", "Bridge", "Wallet", "Smart Contract", "DeFi", "Gaming"]
    
    entities = []
    for i in range(count):
        entity_type = random.choice(entity_types)
        entities.append({
            "id": f"0x{random.randint(10**30, 10**31):x}",
            "type": entity_type,
            "name": f"{entity_type}-{random.randint(1000, 9999)}",
            "tags": random.sample(tags, random.randint(1, 3)),
            "first_seen": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    return entities

def get_db_tables():
    """Return available database tables for the sidebar."""
    return [
        "collections",
        "collection_parts"
    ]


def get_collections_data(db: Session, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Get all collections with pagination and convert to dict format."""
    collections = get_collections(db, skip=skip, limit=limit)
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "parts_count": len(c.parts),
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None,
            "updated_at": c.updated_at.strftime("%Y-%m-%d %H:%M:%S") if c.updated_at else None
        } for c in collections
    ]


def get_collection_parts_data(db: Session, collection_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Get all parts for a specific collection with pagination and convert to dict format."""
    parts = get_collection_parts(db, collection_id, skip=skip, limit=limit)
    return [
        {
            "id": p.id,
            "collection_id": p.collection_id,
            "name": p.name,
            "content": p.content,
            "data": json.loads(p.data) if p.data else {},
            "order": p.order,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None,
            "updated_at": p.updated_at.strftime("%Y-%m-%d %H:%M:%S") if p.updated_at else None
        } for p in parts
    ]


def create_sample_collection(db: Session, name: str, description: Optional[str] = None) -> Collection:
    """Create a sample collection with some parts."""
    # Create the collection
    collection = create_collection(db, name=name, description=description)
    
    # Create some sample parts
    for i in range(3):
        create_collection_part(
            db,
            collection_id=collection.id,
            name=f"Part {i+1}",
            content=f"Sample content for part {i+1}",
            data=json.dumps({"type": "sample", "version": "1.0"}),
            order=i
        )
    
    return collection
