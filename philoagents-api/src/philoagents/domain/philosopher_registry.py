import json
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, Field, PrivateAttr

from philoagents.config import settings
from philoagents.domain.philosopher import Philosopher


class PhilosopherRegistry(BaseModel):
    """Registry containing all available philosopher profiles."""

    profiles: List[Philosopher] = Field(default_factory=list)
    # This is a private attribute to speed up Philosopher lookup by id.
    _philosopher_id_map: Dict[str, Philosopher] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        self._philosopher_id_map = {p.id: p for p in self.profiles}

    @classmethod
    def from_json_file(cls, file_path: Path) -> "PhilosopherRegistry":
        """Loads philosopher profiles from a JSON file."""
        assert file_path.exists(), f"File {file_path} does not exist."
        with open(file_path, "r") as f:
            data = json.load(f)
        return cls(profiles=data)

    @property
    def available_philosophers(self) -> List[str]:
        """Returns a list of all available philosopher IDs."""
        return [p.id for p in self.profiles]

    def get_philosopher(self, philosopher_id: str) -> Philosopher:
        """Gets a philosopher's profile by their ID."""
        philosopher = self._philosopher_id_map.get(philosopher_id)
        if philosopher is None:
            raise KeyError(f"Philosopher with ID '{philosopher_id}' not found")

        return philosopher


PHILOSOPHER_REGISTRY = PhilosopherRegistry.from_json_file(
    settings.PROJECT_PATH / settings.PHILOSOPHERS_FILE_PATH
)
