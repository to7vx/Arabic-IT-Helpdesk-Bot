"""ORM models. Importing this package registers every model with the metadata."""

from helpdesk.db.models.ai import AiSuggestion, Embedding
from helpdesk.db.models.audit import AuditLog, TicketEvent
from helpdesk.db.models.consent import Consent, CrossBorderTransfer
from helpdesk.db.models.escalation import EscalationRule, SlaPolicy
from helpdesk.db.models.kb import KbArticle, KbFeedback, KbVersion
from helpdesk.db.models.organization import Organization, Team, TeamMember
from helpdesk.db.models.ticket import Attachment, Category, Ticket, TicketMessage
from helpdesk.db.models.user import OAuthAccount, User, UserRole
from helpdesk.db.models.webhook import Webhook

__all__ = [
    "AiSuggestion",
    "Attachment",
    "AuditLog",
    "Category",
    "Consent",
    "CrossBorderTransfer",
    "Embedding",
    "EscalationRule",
    "KbArticle",
    "KbFeedback",
    "KbVersion",
    "OAuthAccount",
    "Organization",
    "SlaPolicy",
    "Team",
    "TeamMember",
    "Ticket",
    "TicketEvent",
    "TicketMessage",
    "User",
    "UserRole",
    "Webhook",
]
