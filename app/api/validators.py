import requests
from fastapi import HTTPException

YANDEX_SPELLER_URL = "https://speller.yandex.net/services/spellservice.json/checkText"
MISTAKE = "В слове '{}' орфографическая ошибка. Возможные варианты: {}"

async def check_yandex_spelling(text: str):
    response = requests.post(YANDEX_SPELLER_URL, data={'text': text})
    response.raise_for_status()
    if mistakes:=response.json():
        result = []
        for mistake in mistakes:
            result.append(MISTAKE.format(mistake['word'], mistake['s']))
        raise HTTPException(
            status_code=422,
            detail=result
        )
