from abc import ABC, abstractmethod

class AIDriver(ABC):
    @abstractmethod
    def initialize(self, config):
        pass

    @abstractmethod
    def generate_response(self, messages):
        """
        Generate a response from the AI model
        :param messages: List of message dictionaries with 'role' and 'content'
        :return: Generated text response
        """
        pass

    @abstractmethod
    def get_default_max_tokens(self):
        """Return the default max tokens for this model"""
        pass