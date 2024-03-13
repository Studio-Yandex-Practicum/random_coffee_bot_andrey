from typing import Optional


async def get_entered_name(text: str) -> Optional[str]:
    """Принимает текст, возвращает отформатированное полное имя или None"""
    name_parts = text.strip().split(' ')

    if len(name_parts) != 2 or not all(part.isalpha() for part in name_parts):
        return None

    return ' '.join(part.capitalize() for part in name_parts)
