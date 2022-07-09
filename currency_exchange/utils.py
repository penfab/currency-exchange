import httpx


async def make_request(url):
    """
    return the response body as JSON
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()
