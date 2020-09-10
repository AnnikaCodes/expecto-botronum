"""Translations for Expecto Botronum"""

from typing import Union, Dict
import psclient # type: ignore

def getLanguageID(roomid: str) -> str:
    """Gets a language

    Args:
        roomid (str): [description]

    Returns:
        str: [description]
    """
    if roomid == 'portugus': return 'pt'
    return 'en'

def translate(room: Union[str, psclient.Room], text: str) -> str:
    """Translates a message

    Args:
        room (Union[str, psclient.Room]): the room the text is being translated for
        text (str): the text to translate

    Returns:
        str: the translated text
    """
    roomid = psclient.toID(room) if isinstance(room, str) else room.id
    translations = STRINGS.get(getLanguageID(roomid))
    if not translations: return text
    return translations.get(text) or text

# Dict[language ID, Dict[english, translated]]
STRINGS: Dict[str, Dict[str, str]] = {
    'pt': {
        "do not abuse bold formatting": "não abuse de negrito",
        "do not abuse capital letters": "não abuse de letras maiúsculas",
        "do not flood the chat": "não faça flood no chat",
    }
}
