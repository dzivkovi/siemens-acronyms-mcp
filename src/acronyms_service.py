"""
Core service for searching Siemens acronyms with fuzzy matching and file watching.
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

from rapidfuzz import fuzz, process

logger = logging.getLogger(__name__)


class AcronymsService:
    """Service for searching acronyms with fuzzy matching and file watching."""

    _instance: Optional["AcronymsService"] = None
    _lock = asyncio.Lock()

    def __new__(cls, file_path: Optional[str] = None):
        """Implement singleton pattern."""
        # For testing, allow creating new instances with different file paths
        if file_path and (
            cls._instance is None or (hasattr(cls._instance, "file_path") and cls._instance.file_path != file_path)
        ):
            cls._instance = super().__new__(cls)
        elif cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_path: Optional[str] = None):
        """Initialize the service with file path."""
        # Reset if file path has changed (for testing)
        if hasattr(self, "initialized") and file_path and self.file_path != file_path:
            self.initialized = False

        if not hasattr(self, "initialized"):
            self.file_path = file_path or os.getenv("GLOSSARY_FILE_PATH", "siemens_acronyms.json")
            self.data: list[dict[str, Any]] = []
            self.last_mtime: Optional[float] = None
            self.initialized = True
            logger.info(f"AcronymsService initialized with file: {self.file_path}")

    async def load_data(self) -> None:
        """Load or reload data from JSON file if it has changed."""
        try:
            file_path = Path(self.file_path)

            # Check if file exists
            if not file_path.exists():
                logger.warning(f"Acronyms file not found: {self.file_path}")
                self.data = []
                return

            # Check if file has been modified
            current_mtime = file_path.stat().st_mtime
            if self.last_mtime is not None and current_mtime == self.last_mtime:
                return  # File hasn't changed

            # Load the file
            async with self._lock:
                with open(file_path, encoding="utf-8") as f:
                    content = json.load(f)
                    # Handle both formats: {"acronyms": [...]} or direct list
                    if isinstance(content, dict) and "acronyms" in content:
                        self.data = content["acronyms"]
                    elif isinstance(content, list):
                        self.data = content
                    else:
                        logger.error(f"Invalid JSON format in {self.file_path}")
                        self.data = []

                self.last_mtime = current_mtime
                logger.info(f"Loaded {len(self.data)} acronyms from {self.file_path}")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {self.file_path}: {e}")
            self.data = []
        except Exception as e:
            logger.error(f"Error loading acronyms: {e}")
            self.data = []

    async def search(self, query: str, threshold: float = 80.0, limit: int = 10) -> list[dict[str, Any]]:
        """
        Search for acronyms with fuzzy matching.

        Args:
            query: Search query
            threshold: Minimum similarity score (0-100)
            limit: Maximum number of results

        Returns:
            List of matching acronyms with scores
        """
        # Reload data if file has changed
        await self.load_data()

        if not self.data:
            return []

        if not query:
            return []

        results = []

        # Create searchable strings from data
        searchable_items = []
        for item in self.data:
            # Create a searchable string from term and full_name
            search_str = item.get("term", "")
            if "full_name" in item:
                search_str = f"{search_str} {item['full_name']}"
            searchable_items.append((search_str, item))

        # Perform fuzzy search
        matches = process.extract(
            query,
            [item[0] for item in searchable_items],
            scorer=fuzz.WRatio,
            limit=limit,
        )

        for match_str, score, idx in matches:
            if score >= threshold:
                item = searchable_items[idx][1].copy()
                item["score"] = score
                results.append(item)
            elif query.lower() in match_str.lower() and score >= 60:
                # Partial match with lower threshold
                item = searchable_items[idx][1].copy()
                item["score"] = score
                results.append(item)

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:limit]

    async def get_all(self) -> list[dict[str, Any]]:
        """Get all acronyms."""
        await self.load_data()
        return self.data.copy()
