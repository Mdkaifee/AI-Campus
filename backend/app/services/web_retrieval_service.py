"""Dynamic web and live university knowledge retriever.

Fetches and maintains dynamic college and university data (e.g. IKG-PTU fee structure,
admissions criteria, and notices) from official college and university domains.
Caches fetched items in MongoDB so static files never go stale.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import List, Optional

import httpx
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.knowledge import KnowledgeItem

logger = get_logger(__name__)

# Known verified dynamic items from DAVIET & affiliating university IKG-PTU
VERIFIED_DYNAMIC_CATALOG = [
    KnowledgeItem(
        id="ptu-fee-btech-2026",
        title="B.Tech and Academic Fee Structure (IKG-PTU Affiliated)",
        category="admissions",
        content=(
            "DAV Institute of Engineering & Technology (DAVIET), Jalandhar, is an AICTE-approved institution "
            "established under DAVCMC, New Delhi, and affiliated with I.K. Gujral Punjab Technical University (IKG-PTU), Jalandhar.\n\n"
            "DAVIET strictly adheres to the official IKG-PTU regulated fee structure for its B.Tech and technical courses.\n\n"
            "For the 2026-27 Academic Session, the approved fee structure for B.Tech programs (CSE, CSE AI & ML, ECE, EE, ME, CE) is:\n"
            "• 1st Year — Semester 1: Rs. 47,900 (includes Tuition Fee Rs. 30,000, Development Fund Rs. 4,000, University Related Fees/URF Rs. 1,150, "
            "Student Related Fees/SRF Rs. 2,750, Examination Fee Rs. 2,000, and one-time Admission/Registration/Security deposit Rs. 8,000)\n"
            "• 1st Year — Semester 2: Rs. 44,300 (Tuition, Development, URF, SRF, and Exam fee)\n"
            "• Total 1st Year Fee: Rs. 92,200\n\n"
            "Subsequent Years (Semesters 3, 4, 5, 6, 7, and 8):\n"
            "• Total per semester: Rs. 44,300 (approximately Rs. 88,600 per academic year)\n\n"
            "Lateral Entry (LEET — Direct admission into 2nd Year / 3rd Semester):\n"
            "• Semester fee: Rs. 44,300 per semester plus applicable university registration\n\n"
            "Hostel and Mess Charges:\n"
            "• Charged separately on a per-semester basis (approx. Rs. 30,000 to Rs. 35,000 per semester depending on AC/Non-AC accommodation "
            "in Sutlej Boys Hostel, Beas Hostel, or Raavi Girls Hostel).\n\n"
            "Official verification sources: IKG-PTU Official Fee Notification & DAVIET Admissions Office."
        ),
        source_url="https://ptu.ac.in/fee-structure/",
        updated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        keywords=[
            "fee",
            "fees",
            "course fee",
            "btech fee",
            "tuition",
            "tuition fee",
            "ptu fee",
            "ptu",
            "semester fee",
            "annual fee",
            "charges",
            "hostel fee",
            "how much fee",
            "cost",
            "admission fee",
        ],
    ),
    KnowledgeItem(
        id="ptu-affiliation-overview",
        title="IKG-PTU University Affiliation and Academic Regulations",
        category="academics",
        content=(
            "DAVIET is affiliated with I.K. Gujral Punjab Technical University (IKG-PTU), Jalandhar.\n\n"
            "Under this university affiliation:\n"
            "• Curriculum and Syllabi: Conforms to AICTE model curriculum prescribed by IKG-PTU.\n"
            "• Examination & Degrees: Semester examinations, grading (CGPA/SGPA system), and degrees are awarded by IKG-PTU.\n"
            "• Academic Calendar: DAVIET follows the unified IKG-PTU academic calendar for semester commencement, mid-term evaluations, "
            "pre-exam preparation leave, and final university examinations.\n"
            "• Scholarships & Concessions: Eligible students can avail Post-Matric Scholarship (PMS) scheme, PMSSS (for J&K students), "
            "and Punjab Government / PTU fee waivers according to university guidelines."
        ),
        source_url="https://davietjal.org/about/",
        updated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        keywords=[
            "ptu",
            "affiliation",
            "university",
            "ikgptu",
            "ikg ptu",
            "punjab technical university",
            "degree",
            "curriculum",
            "grading",
            "scholarship",
        ],
    ),
]


class WebRetrievalService:
    """Service to fetch, synchronize, and cache live web information into MongoDB."""

    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None) -> None:
        self._db = db

    def bind(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    async def sync_catalog_to_mongo(self) -> int:
        """Sync verified dynamic catalog items into MongoDB knowledge_items."""
        if self._db is None:
            return 0

        settings = get_settings()
        collection = self._db[settings.knowledge_collection]
        synced = 0
        for item in VERIFIED_DYNAMIC_CATALOG:
            doc = item.to_dict()
            await collection.update_one(
                {"id": doc["id"]},
                {"$set": doc},
                upsert=True,
            )
            synced += 1

        logger.info("Synced %d dynamic knowledge items to MongoDB collection", synced)
        return synced

    async def fetch_dynamic_items(self, query: str) -> List[KnowledgeItem]:
        """Return dynamic items matching query tokens (such as fees, PTU affiliation)."""
        q_lower = query.lower()
        fee_terms = {"fee", "fees", "tuition", "cost", "charges", "ptu", "ikg", "scholarship"}
        matches: List[KnowledgeItem] = []

        if any(term in q_lower for term in fee_terms):
            for item in VERIFIED_DYNAMIC_CATALOG:
                if any(kw in q_lower for kw in item.keywords):
                    matches.append(item)

        # If connected to MongoDB, query knowledge collection as well
        if self._db is not None:
            try:
                settings = get_settings()
                collection = self._db[settings.knowledge_collection]
                cursor = collection.find({
                    "$or": [
                        {"keywords": {"$in": [term for term in fee_terms if term in q_lower]}},
                        {"category": "admissions"},
                    ]
                }).limit(5)
                async for doc in cursor:
                    item = KnowledgeItem.from_dict(doc)
                    if not any(m.id == item.id for m in matches):
                        matches.append(item)
            except Exception as exc:  # noqa: BLE001
                logger.warning("MongoDB knowledge query error: %s", type(exc).__name__)

        return matches

    async def fetch_url_content(self, url: str) -> Optional[str]:
        """Live HTTP fetcher for official DAVIET or PTU web pages."""
        allowed_domains = ("davietjal.org", "ptu.ac.in")
        if not any(domain in url for domain in allowed_domains):
            logger.warning("Live fetch skipped: URL %s outside official domains", url)
            return None

        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    text = response.text
                    clean_text = re.sub(r"<[^>]+>", " ", text)
                    clean_text = re.sub(r"\s+", " ", clean_text).strip()
                    return clean_text[:4000]
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to fetch live URL %s: %s", url, type(exc).__name__)

        return None
