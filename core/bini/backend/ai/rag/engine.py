import os
import requests
from fastapi import APIRouter
from dotenv import load_dotenv
from dataclasses import dataclass
from settings import Logfire


load_dotenv()

log = Logfire(name='anything-llm-api')

API = os.getenv("API", "v1")

router = APIRouter(prefix=f"/api/{API}/rag", tags=["bini"])

HOST = os.getenv('RAG_HOST_NAME')


@dataclass
class AnythingLLM:

    api_key = os.getenv("ANYTHING_LLM_API_KEY")
    base_url = f"http://{HOST}:3001"  # for local dev, in .env change host name to localhost

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}",
                                     "Content-Type": "application/json",
                                     "Accept": "application/json"})

    @property
    def workspaces(self) -> dict:
        url = f"{self.base_url}/api/v1/workspaces"
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        log.fire.info(f'{data}')
        return {"workspaces": data} if isinstance(data, list) else data

    def __fetch_query(self, workspace: str, message: str) -> dict:

        """returns all the query metadata which response is taken in the next functions"""

        url = f"{self.base_url}/api/v1/workspace/{workspace.lower()}/chat"
        body = {"message": message, "mode": "query"}

        response = self.session.post(url, json=body, timeout=30)

        try:
            log.fire.info(f'{response.json()}')
            return response.json()
        except ValueError:
            log.fire.error({
                "status_code": response.status_code,
                "content_type": response.headers.get("Content-Type", ""),
                "text": response.text,
                "url": response.url,
            })
            raise

    async def send_query(self, workspace: str, query: str) -> str:
        response = self.__fetch_query(workspace=workspace, message=query).get('textResponse')
        log.fire.info(f'message: {query}\nresponse: {response}')
        return response


if __name__ == "__main__":
    llm = AnythingLLM()
    print(llm.workspaces)
    import asyncio
    print(asyncio.run(llm.send_query(workspace="app", query="on what documents are you based on?")))
