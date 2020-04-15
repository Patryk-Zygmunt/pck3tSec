from abc import ABC, abstractmethod


class AnalyzerBase(ABC):

    @abstractmethod
    def analyze(self, packet):
        pass
