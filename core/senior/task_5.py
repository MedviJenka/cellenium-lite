import json
import time
import httpx
import asyncio
from typing import List
from settings import Logfire
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


log = Logfire(name="async-health")


class Config(BaseSettings):
    USERS: str = "https://jsonplaceholder.typicode.com/users"
    POSTS: str = "https://jsonplaceholder.typicode.com/posts"
    ERROR: str = "https://httpstat.us/503"


Config = Config()


class ServiceReport(BaseModel):
    service: str
    status: int
    latency_ms: float
    result: str = Field(description="healthy/unhealthy")


@dataclass
class AsyncAPIManager:

    timeout: int = 5
    retries: int = 3
    backoff_factor: float = 0.5

    async def fetch(self, client: httpx.AsyncClient, name: str, url: str) -> ServiceReport:
        """Fetch a single service with retry + exponential backoff."""
        for attempt in range(1, self.retries + 1):
            start = time.perf_counter()
            try:
                response = await client.get(url, timeout=self.timeout)
                latency = (time.perf_counter() - start) * 1000
                status = response.status_code
                result = "healthy" if status < 400 else "unhealthy"
                log.fire.info(f"{name}: {status} in {latency:.2f} ms ({result})")
                return ServiceReport(service=name, status=status, latency_ms=latency, result=result)

            except (httpx.RequestError, httpx.TimeoutException) as e:
                delay = self.backoff_factor * (2 ** attempt)
                log.fire.warning(f"{name} attempt {attempt} failed ({e}); retrying in {delay:.1f}s")
                await asyncio.sleep(delay)

        # All retries failed
        log.fire.error(f"{name} timed out after {self.retries} retries")
        return ServiceReport(service=name, status=0, latency_ms=0, result="unhealthy")

    async def run_all(self, urls: dict[str, str]) -> List[ServiceReport]:
        """Run health checks for all services concurrently."""
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch(client, name, url) for name, url in urls.items()]
            return await asyncio.gather(*tasks)

    @staticmethod
    def save_report(reports: List[ServiceReport], path: str = "async_report.json") -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([r.model_dump() for r in reports], f, indent=2)
        log.fire.info(f"Report saved to {path}")

    @staticmethod
    def summarize(reports: List[ServiceReport]) -> None:
        healthy = sum(r.result == "healthy" for r in reports)
        total = len(reports)
        print(f"Total services: {total} | Healthy: {healthy} | Unhealthy: {total - healthy}")
        for r in reports:
            print(f"{r.service.upper()}: {r.status} ({r.result}) - {r.latency_ms:.1f} ms")


# -------------------- Main Entry --------------------
async def main():
    api = AsyncAPIManager()
    urls = {
        "users": Config.USERS,
        "posts": Config.POSTS,
        "error": Config.ERROR,
    }
    reports = await api.run_all(urls)
    api.save_report(reports)
    api.summarize(reports)

if __name__ == "__main__":
    asyncio.run(main())
