from flask import request

from app import components
from app.tags import TagService


class TagAutoCompleteController (components.Controller):
    path = "/autocomplete/"
    _service = TagService()

    def get(self):
        search_query = request.args.get("q")
        result_limit = request.args.get("l")
        result_limit = 0 if not result_limit else int(result_limit)
        return self._fetch_all(search_query, result_limit)
