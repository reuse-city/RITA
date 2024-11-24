# backend/src/services/knowledge_base/service.py
"""
Knowledge Base Service for RITA.

Handles:
- Integration with external repair resources
- Guide retrieval and storage
- Attribution management
- Reference tracking
"""

from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from ...models.knowledge import KnowledgeSource, RepairGuide, Reference
from fastapi import HTTPException
import httpx
import logging

logger = logging.getLogger(__name__)

class KnowledgeBaseService:
    def __init__(self, db: Session):
        self.db = db

    async def get_sources(self) -> List[KnowledgeSource]:
        """Get all registered knowledge sources."""
        return self.db.query(KnowledgeSource).all()

    async def add_source(self, source_data: Dict) -> KnowledgeSource:
        """Register a new knowledge source."""
        source = KnowledgeSource(**source_data)
        self.db.add(source)
        self.db.commit()
        return source

    async def search_guides(self, query: str, source_id: Optional[int] = None) -> List[RepairGuide]:
        """
        Search for repair guides across all sources or a specific source.
        Includes proper attribution and references.
        """
        guides_query = self.db.query(RepairGuide)
        
        if source_id:
            guides_query = guides_query.filter(RepairGuide.source_id == source_id)
        
        # Basic search implementation - can be enhanced with full-text search
        guides = guides_query.filter(RepairGuide.title.ilike(f"%{query}%")).all()
        
        # Load references and attribution data
        for guide in guides:
            guide.references
            guide.source
            
        return guides

    async def get_guide_with_references(self, guide_id: int) -> RepairGuide:
        """Get a repair guide with all its references and attribution info."""
        guide = self.db.query(RepairGuide).get(guide_id)
        if not guide:
            raise HTTPException(status_code=404, detail="Guide not found")
        
        # Load relationships
        guide.steps
        guide.references
        guide.source
        
        return guide

    async def add_guide(self, guide_data: Dict) -> RepairGuide:
        """
        Add a new repair guide with proper attribution.
        Ensures all references are properly tracked.
        """
        try:
            # Create guide with basic info
            guide = RepairGuide(
                title=guide_data["title"],
                description=guide_data["description"],
                device_type=guide_data["device_type"],
                source_id=guide_data["source_id"],
                author=guide_data["author"],
                license=guide_data["license"]
            )
            
            # Add references
            for ref_data in guide_data.get("references", []):
                reference = Reference(
                    source_id=ref_data["source_id"],
                    url=ref_data["url"],
                    description=ref_data["description"],
                    type=ref_data["type"]
                )
                guide.references.append(reference)
            
            self.db.add(guide)
            self.db.commit()
            return guide
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding guide: {str(e)}")
            raise HTTPException(status_code=500, detail="Error adding guide")

    async def update_guide(self, guide_id: int, guide_data: Dict) -> RepairGuide:
        """Update a guide while maintaining attribution and references."""
        guide = self.db.query(RepairGuide).get(guide_id)
        if not guide:
            raise HTTPException(status_code=404, detail="Guide not found")
        
        try:
            # Update basic info
            for key, value in guide_data.items():
                if hasattr(guide, key) and key != "id":
                    setattr(guide, key, value)
            
            # Update references if provided
            if "references" in guide_data:
                # Remove old references
                guide.references = []
                # Add new references
                for ref_data in guide_data["references"]:
                    reference = Reference(**ref_data)
                    guide.references.append(reference)
            
            self.db.commit()
            return guide
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating guide: {str(e)}")
            raise HTTPException(status_code=500, detail="Error updating guide")
