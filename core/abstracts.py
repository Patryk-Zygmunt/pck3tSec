from abc import ABC, abstractmethod


class IObserver(ABC):

    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class IObservable(ABC):

    @abstractmethod
    def register_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass


class IAnalyzer(ABC):

    @abstractmethod
    def analyze(self, packet):
        pass
