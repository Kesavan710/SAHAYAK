"""
API Routers for Sahayak Backend
"""

from .chat import router as chat_router
from .profile import router as profile_router
from .eligibility import router as eligibility_router
from .documents import router as documents_router
from .application import router as application_router
from .status import router as status_router

__all__ = [
    'chat_router',
    'profile_router',
    'eligibility_router',
    'documents_router',
    'application_router',
    'status_router',
]
