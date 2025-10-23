import os
import requests
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Union, Type
from contextlib import ExitStack
from pydantic import BaseModel
from backend.utils.logger import Logfire
from backend.settings import Config


type PathLike = Union[str, os.PathLike]

log = Logfire("bini-client")


@dataclass
class BiniClient:

    """
    Minimal HTTP client for the Bini image endpoint.
    TODO: research bini fallback solution
    """

    host: str = Config.HOST
    port: str = Config.PORT
    endpoint: str = "/api/v1/bini"
    timeout: int = 300  # (5 minutes)
    _session: requests.Session | None = None
    chain_of_thought: bool = False
    session = requests.Session()

    # def __post_init__(self) -> None:
    #     # Reuse connections + sane retries for transient failures
    #     if self._session is None:
    #         s = requests.Session()
    #         adapter = HTTPAdapter(max_retries=5, pool_maxsize=10)
    #         s.mount("http://", adapter)
    #         s.mount("https://", adapter)
    #         self._session = s

    def __enter__(self) -> "BiniClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @property
    def __server_url(self) -> str:
        url = f"http://{self.host}:{self.port}{self.endpoint}"
        log.fire.info(f"bini endpoint is: {url}")
        return url

    @staticmethod
    def _content_type(path: PathLike) -> str:
        return mimetypes.guess_type(str(path))[0] or "application/octet-stream"

    def run_image(self, prompt: str, image_path: PathLike, sample_image_paths: Optional[Iterable[PathLike]] = None) -> dict:
        """
        POST multipart/form-data with:
          - prompt (text field)
          - image (single file)
          - sample_images (0..n files, same field name repeated)
        """

        data = {
            "prompt": prompt,
            "chain_of_thought": True,
        }

        files = []
        with ExitStack() as stack:
            # Main image
            main_path = Path(image_path)
            main_f = stack.enter_context(open(main_path, "rb"))
            files.append(("image", (main_path.name, main_f, self._content_type(main_path))))

            # Optional sample images
            if sample_image_paths:
                for p in sample_image_paths:
                    sp = Path(p)
                    fh = stack.enter_context(open(sp, "rb"))
                    files.append(("sample_images", (sp.name, fh, self._content_type(sp))))

            resp = self.session.post(self.__server_url, data=data, files=files, timeout=self.timeout)
            if resp.status_code >= 400:
                log.fire.error(f"Server error {resp.status_code}: {resp.text}")
            resp.raise_for_status()
            log.fire.info(f"Response OK: {resp.status_code}")
            return resp.json()

    def run_chat(self, prompt: str, schema_output: Optional[Type[BaseModel]] = None) -> dict:
        url = f"{self.__server_url}/chat"
        payload = {
            "prompt": prompt,
            "chain_of_thought": self.chain_of_thought,
        }

        if schema_output:
            payload["schema_output"] = schema_output.model_json_schema()

        try:
            response = self.session.post(url=url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            log.fire.error(f"Request timed out after {self.timeout}s to {url}")
            raise

        except requests.exceptions.RequestException as e:
            log.fire.error(f"Request failed: {e}")
            raise

    def run_audio(self) -> ...:
        raise NotImplemented

    def run_video(self) -> ...:
        """use google api"""
        raise NotImplemented

    def close(self) -> None:
        if self._session:
            self._session.close()
            self._session = None
