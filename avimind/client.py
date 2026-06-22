from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

from .exceptions import APIError, AviMindError, ConnectionError, ValidationError


class AviMind:
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health(self) -> Dict[str, Any]:
        return self._request("GET", "/health")

    def remember(
        self,
        user_id: str,
        content: str,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        memory_type: str = "general_memory",
        source: str = "sdk",
        created_by: str = "human",
        tags: Optional[List[str]] = None,
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not user_id:
            raise ValidationError("user_id is required")

        if not content:
            raise ValidationError("content is required")

        payload = {
            "user_id": user_id,
            "agent_id": agent_id,
            "session_id": session_id,
            "memory_type": memory_type,
            "content": content,
            "source": source,
            "created_by": created_by,
            "tags": tags or [],
            "importance": importance,
            "metadata": metadata,
        }

        return self._request("POST", "/memory", json=payload)

    def search(
        self,
        user_id: str,
        query: str,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        limit: int = 5,
    ) -> Dict[str, Any]:
        if not user_id:
            raise ValidationError("user_id is required")

        if not query:
            raise ValidationError("query is required")

        params = {
            "user_id": user_id,
            "query": query,
            "agent_id": agent_id,
            "session_id": session_id,
            "memory_type": memory_type,
            "limit": limit,
        }

        return self._request("GET", "/memory/search", params=params)

    def context(
        self,
        user_id: str,
        query: str,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        limit: int = 5,
        min_score: float = 0.65,
    ) -> List[str]:
        if not user_id:
            raise ValidationError("user_id is required")

        if not query:
            raise ValidationError("query is required")

        params = {
            "user_id": user_id,
            "query": query,
            "agent_id": agent_id,
            "session_id": session_id,
            "memory_type": memory_type,
            "limit": limit,
            "min_score": min_score,
        }

        response = self._request("GET", "/memory/context", params=params)
        return response.get("context", [])

    def delete(self, memory_id: str) -> Dict[str, Any]:
        if not memory_id:
            raise ValidationError("memory_id is required")

        return self._request("DELETE", f"/memory/{memory_id}")

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"

        try:
            response = requests.request(
                method=method,
                url=url,
                params=self._clean_params(params),
                json=json,
                timeout=self.timeout,
            )
        except requests.exceptions.ConnectionError as exc:
            raise ConnectionError(f"Unable to connect to AviMind server: {url}") from exc
        except requests.exceptions.Timeout as exc:
            raise ConnectionError(f"AviMind request timed out: {url}") from exc
        except requests.exceptions.RequestException as exc:
            raise AviMindError(f"AviMind request failed: {exc}") from exc

        if response.status_code >= 400:
            raise APIError(
                f"AviMind API error {response.status_code}: {response.text}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise APIError("AviMind API returned non-JSON response") from exc

    @staticmethod
    def _clean_params(params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not params:
            return {}

        return {key: value for key, value in params.items() if value is not None}