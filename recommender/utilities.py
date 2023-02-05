from io import StringIO
import csv


class OnMemoryCSVConvertor:
    """
    Convert MusicState or SensorState tables' rows by given session id to CSV tables on memory.
    """

    def convert(self, query_set):
        try:
            self.on_memory = StringIO()
            if query_set:
                on_memory_file = csv.writer(self.on_memory)
                header = list(query_set[0].__dict__.keys())
                header.pop(0)
                on_memory_file.writerow(header)

                for record in query_set:
                    row = list(record.__dict__.values())
                    row.pop(0)
                    on_memory_file.writerow(row)

                return self.on_memory.getvalue()
        except:
            pass
