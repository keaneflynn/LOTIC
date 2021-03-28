from numpy import ndarray
from dataclasses import dataclass, field
from typing import List
from datetime import datetime
import time
import json

@dataclass
class Item:
    name: str

@dataclass
class Classification:
    frame: 'ndarray'
    items: List[Item] = field(default_factory=list)

class Stats:
    def __init__(self, filename):
        self.filename = filename
        self.start_time = str(datetime.now())
        self._start_time_s = time.time()
        self.duration_seconds = -1
        self._count_mapping = {}

    def observe(self, cfc):
        count_map = {}
        for item in cfc.items:
            count_map[item.name] = count_map.get(item.name, 0) + 1

        for name in count_map:
            if count_map[name] > self._count_mapping.get(name, 0):
                self._count_mapping[name] = count_map[name]

    def finish(self):
        self.duration_seconds = time.time() - self._start_time_s

    """
    {
        filename: "",
        start_time: "",
        duration_seconds: X,
        fish: [
            {
                species_id: "",
                count: X,
            },
            {...}
        ]
    }
    """

    def to_json(self):
        out = {
                "filename": self.filename,
                "start_time": self.start_time,
                "duration_seconds": self.duration_seconds,
                "fish": [],
        } 

        for name in self._count_mapping:
            out['fish'] += [{
                "species_id": name,
                "count": self._count_mapping[name]
            }]
        
        return json.dumps(out)
