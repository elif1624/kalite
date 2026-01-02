# backend/metrics/base_metric.py

from abc import ABC, abstractmethod

class BaseMetric(ABC):
    @abstractmethod
    def calculate(self, raw_data: dict) -> dict:
        """
        Her AI test aracı çıktısını
        standart metrik formatına çevirir
        """
        pass
