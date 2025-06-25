"""Base abstract class for AI chat API drivers."""

from abc import ABC, abstractmethod

class AIDriver(ABC):
    """Abstract base class defining the interface for AI chat API drivers.

    All AI chat providers must implement these methods to ensure consistent behavior."""

    def __init__(self):
        """Initialize base attributes."""
        self.client = None
        self.model = None
        self.max_tokens = None
        self.temperature = None

    @abstractmethod
    def initialize(self, config):
        """Initialize the AI driver with configuration.

        Args:
            config (dict): Configuration dictionary with API keys and settings
        """

    @abstractmethod
    def generate_response(self, messages):
        """Generate a response from the AI model

        Args:
            messages (list): List of message dictionaries with 'role' and 'content'

        Returns:
            str: Generated text response
        """

    @abstractmethod
    def get_default_max_tokens(self):
        """Return the default max tokens for this model"""