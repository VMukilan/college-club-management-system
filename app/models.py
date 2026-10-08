"""
Domain Models for College Club Management System (v0.1)

Entities:
- USER
- CLUB
- MEMBERSHIP
- EVENT
- EVENT_REGISTRATION
- ANNOUNCEMENT
- AUDIT_LOG
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    role: str  # 'student', 'coordinator', 'admin'
    full_name: str
    email: str
    club_id: Optional[int] = None  # Relevant for coordinator assignment

@dataclass
class Club:
    id: Optional[int]
    name: str
    description: str
    category: str
    created_at: Optional[str] = None

@dataclass
class Membership:
    id: Optional[int]
    user_id: int
    club_id: int
    status: str  # 'ACTIVE', 'PENDING'
    joined_at: Optional[str] = None

@dataclass
class Event:
    id: Optional[int]
    club_id: int
    title: str
    description: str
    event_date: str
    location: str
    created_by: int
    created_at: Optional[str] = None

@dataclass
class EventRegistration:
    id: Optional[int]
    event_id: int
    user_id: int
    status: str  # 'REGISTERED', 'CANCELLED'
    registered_at: Optional[str] = None

@dataclass
class Announcement:
    id: Optional[int]
    club_id: int
    title: str
    content: str
    created_by: int
    created_at: Optional[str] = None

@dataclass
class AuditLog:
    id: Optional[int]
    user_id: Optional[int]
    action: str
    details: str
    timestamp: Optional[str] = None
