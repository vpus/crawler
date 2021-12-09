from abc import ABC, abstractmethod

class AbstrcatWebsite(ABC):
    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def _extract_data(self, article):
        pass