from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from projectionbench.models import JSONLD_CONTEXT


@dataclass(frozen=True)
class RegistryEntry:
    id: str
    type: str
    name: str
    artifact: dict[str, Any]

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": self.id,
            "@type": ["schema:CreativeWork", "pb:RegistryEntry"],
            "name": self.name,
            "artifactType": self.type,
            "artifact": self.artifact,
        }


class JsonLdRegistry:
    """Simple file-backed JSON-LD registry for benchmark artifacts.

    This keeps the first implementation dependency-free. Later versions can
    replace this with SurrealDB, RDF, graph storage, or a hosted registry API.
    """

    def __init__(self, path: str | Path = "registry/local.registry.jsonld"):
        self.path = Path(path)

    def register(self, artifact: dict[str, Any], artifact_type: str | None = None) -> RegistryEntry:
        registry = self._load()
        entry = RegistryEntry(
            id=f"pb:registry-entry/{artifact.get('@id', artifact.get('name', 'unknown')).replace(':', '/').replace(' ', '-')}",
            type=artifact_type or self._infer_type(artifact),
            name=artifact.get("name", artifact.get("@id", "Unnamed artifact")),
            artifact=artifact,
        )
        entries = [item for item in registry.get("hasPart", []) if item.get("artifact", {}).get("@id") != artifact.get("@id")]
        entries.append(entry.to_jsonld())
        registry["hasPart"] = entries
        self._save(registry)
        return entry

    def list(self, artifact_type: str | None = None) -> list[dict[str, Any]]:
        entries = self._load().get("hasPart", [])
        if artifact_type is None:
            return entries
        return [entry for entry in entries if entry.get("artifactType") == artifact_type]

    def get(self, artifact_id: str) -> dict[str, Any] | None:
        for entry in self._load().get("hasPart", []):
            artifact = entry.get("artifact", {})
            if artifact.get("@id") == artifact_id or entry.get("@id") == artifact_id:
                return artifact
        return None

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {
                "@context": JSONLD_CONTEXT,
                "@id": "pb:registry/local",
                "@type": ["schema:Dataset", "pb:ArtifactRegistry"],
                "name": "Local ProjectionBench Artifact Registry",
                "hasPart": [],
            }
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, registry: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _infer_type(self, artifact: dict[str, Any]) -> str:
        types = artifact.get("@type", [])
        if isinstance(types, str):
            types = [types]
        for item in types:
            if item.startswith("pb:"):
                return item.removeprefix("pb:")
        return "Artifact"
