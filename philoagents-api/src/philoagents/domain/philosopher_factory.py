from philoagents.domain.exceptions import PhilosopherNotFound
from philoagents.domain.philosopher import Philosopher
from philoagents.domain.philosopher_registry import PHILOSOPHER_REGISTRY


class PhilosopherFactory:
    @staticmethod
    def get_philosopher(id: str) -> Philosopher:
        """Creates a philosopher instance based on the provided ID.

        Args:
            id (str): Identifier of the philosopher to create

        Returns:
            Philosopher: Instance of the philosopher

        Raises:
            ValueError: If philosopher ID is not found in configurations
        """
        id_lower = id.lower()

        try:
            philosopher = PHILOSOPHER_REGISTRY.get_philosopher(id_lower)
            return philosopher
        except KeyError as e:
            raise PhilosopherNotFound(id_lower) from e

    @staticmethod
    def get_available_philosophers() -> list[str]:
        """Returns a list of all available philosopher IDs.

        Returns:
            list[str]: List of philosopher IDs that can be instantiated
        """
        return PHILOSOPHER_REGISTRY.available_philosophers
