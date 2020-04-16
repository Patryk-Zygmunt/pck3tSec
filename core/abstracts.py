from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, content):
        pass


class IObservable(ABC):

    @abstractmethod
    def register_observer(self, observer: Observer):
        pass

    def remove_observer(self, observer: Observer):
        pass


class AnalyzerBase(ABC):

    @abstractmethod
    def analyze(self, packet):
        pass
