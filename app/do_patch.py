import httpx
import json
from openai import AsyncOpenAI

class StripStrictTransport(httpx.AsyncBaseTransport):
    def __init__(self, transport: httpx.AsyncBaseTransport):
        self.transport = transport

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        if request.url.path == '/v1/chat/completions' and request.method == 'POST':
            body = json.loads(request.content)
            changed = False
            
            if 'response_format' in body:
                del body['response_format']
                changed = True
                
            if 'tool_choice' in body:
                del body['tool_choice']
                changed = True
            
            if 'tools' in body:
                for t in body['tools']:
                    if 'function' in t:
                        if 'strict' in t['function']:
                            del t['function']['strict']
                            changed = True
                        if 'parameters' in t['function'] and 'additionalProperties' in t['function']['parameters']:
                            del t['function']['parameters']['additionalProperties']
                            changed = True
            
            if changed:
                new_content = json.dumps(body).encode('utf-8')
                headers = request.headers.copy()
                headers['content-length'] = str(len(new_content))
                request = httpx.Request(
                    method=request.method,
                    url=request.url,
                    headers=headers,
                    content=new_content
                )
                
        return await self.transport.handle_async_request(request)

def get_patched_openai_client(api_key: str, base_url: str) -> AsyncOpenAI:
    base_transport = httpx.AsyncHTTPTransport()
    transport = StripStrictTransport(base_transport)
    http_client = httpx.AsyncClient(transport=transport)
    return AsyncOpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
