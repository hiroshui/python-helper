from enum import Enum

class OutlookItems(Enum):
    """
    An enumeration of the possible Outlook item types.
    """
    EMAIL = 0
    """
    An email message.
    """
    APPOINTMENT = 1
    """
    An appointment or meeting request.
    """
    CONTACT = 2
    """
    A contact or address book entry.
    """
    TASK = 3
    """
    A task or to-do item.
    """
    JOURNAL_ENTRY = 4
    """
    A journal entry or log.
    """
    NOTE = 5
    """
    A note or memo.
    """

class OutlookImportance(Enum):
    """
    An enumeration of the possible importance levels for an Outlook item.
    """
    LOW = 0
    """
    Low importance.
    """
    NORMAL = 1
    """
    Normal importance.
    """
    HIGH = 2
    """
    High importance.
    """