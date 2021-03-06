from typing import List, Optional

from sophie_bot.services.mongo import engine, db
from ..models import RESTRICTED_SYMBOLS, SavedNote


def check_note_names(note_names: List[str]) -> Optional[str]:
    sym = None
    if any((sym := s) in '|'.join(note_names) for s in RESTRICTED_SYMBOLS):
        return sym

    return None


def check_note_group(note_group: str) -> Optional[str]:
    sym = None
    if any((sym := s) in note_group for s in RESTRICTED_SYMBOLS):
        return sym

    return None


async def get_notes_count(chat_id: int) -> int:
    return await engine.count(SavedNote, SavedNote.chat_id == chat_id)


async def get_groups_count(chat_id: int) -> int:
    return len(await db[+SavedNote].distinct('group', SavedNote.chat_id == chat_id))
