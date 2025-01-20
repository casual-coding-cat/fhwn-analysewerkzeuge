import pandas as pd
from pathlib import Path

class Data:
    def __init__(self):
        # das aktuelle Verzeichnis holen
        self.project_path= Path(__file__).resolve().parent.parent

        # den Pfad des input-Ordners abrufen
        self.data_path= self.project_path.joinpath("data")

        self.file_path = self.data_path.joinpath("shopping_trends.csv")

        self.data = pd.read_csv(self.file_path)

    def get_data(self):
        return self.data

    # show basic information about the dataset
    def basic_info(self):
        data.info()
        data.head()
        summary_stats = data.describe(include='all')
        print(summary_stats)