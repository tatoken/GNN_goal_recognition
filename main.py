from PyQt6.QtWidgets import QApplication
import sys
import numpy as np

from Loaders import LoaderMapFirstType
from PathVisualizer import PathVisualizer

if __name__ == "__main__":
    size = 16
    file=88
    file_name = f"dataset/maps_dataset_{size}/maps_dataset_{size}_{file}.json"
    index = 0
    map_info = LoaderMapFirstType.load_map_from_json(file_name, index)

    app = QApplication(sys.argv)
    window = PathVisualizer(
        map_info.size,
        map_info.map_data,
        map_info.source_destination[0],
        map_info.source_destination[1],
        [130,114,98,99,83,84,68,69,53,54,38]
        ,200
    )
    window.show()
    sys.exit(app.exec())
