class Query:
    """ Класс запроса """

    def __init__(self, path):
        self.path = path
        self._command = {
            "filter": self._filter,
            "map": self._map,
            "unique": self._unique,
            "sort": self._sort,
            "limit": self._limit
        }

    def prepared_data(self):
        """ Подготовка данных из файла """
        with open(self.path) as file:
            return list(map(lambda x: x.strip(), file))

    def get_query(self, params):
        """ Возвращает данные по параметрам запроса """

        data = self.prepared_data()
        for param in params:
            data = self._command[param["cmd"]](param=param["value"], data=data)
        return data

    def _filter(self, param, data):
        return list(filter(lambda x: param in x, data))

    def _map(self, param, data):
        column_number = int(param)
        return list(map(lambda v: v.split()[column_number], data))

    def _unique(self, data, *args, **kwargs):
        return list(set(data))

    def _sort(self, param, data):
        reverse = False if param == "asc" else True
        return sorted(data, reverse=reverse)

    def _limit(self, param, data):
        limit = int(param)
        return list(data)[:limit]
