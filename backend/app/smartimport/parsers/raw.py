import csv
from dateutil.parser import parse as parse_date

from smartimport.parsers import BaseParser


class RawParser(BaseParser):
    def __init__(self):
        pass
    pass

    def _predict_tags(self, row):
        # Here comes the magic
        return row

    def _read_csv(self, utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.DictReader(utf8_data, dialect=dialect, **kwargs)
        for row in csv_reader:
            yield {
                "date": parse_date(row["date"]),
                "price": float(row["price"]),
                "text": row["tags"].strip(),
                "tags": []
            }

    def preprocess(self, payload):
        dialect = csv.Sniffer().sniff(payload.read(1024))
        payload.seek(0)
        reader = self._read_csv(payload, dialect=dialect)
        return [self._predict_tags(row) for row in reader]
    pass


def dispatch():
    return RawParser()
