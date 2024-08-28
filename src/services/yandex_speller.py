from aiohttp import ClientSession


async def check_text(text: str):
    url: str = "https://speller.yandex.net/services/spellservice.json/checkText"
    payload = {
        "text": text,
    }
    async with ClientSession() as session:
        async with session.post(url=url, data=payload) as response:
            response_json = await response.json()
            return response_json