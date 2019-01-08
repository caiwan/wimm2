from flask import request
import components

from estateplan import budgetService, assetService


class BudgetListController(components.Controller):
    path = "/budget/"
    _service = budgetService

    def get(self):
        return self._fetch_all()
    
    def post(self):
        return self._create(request.json)


class BudgetController(components.Controller):
    path = "/estate/budget/<int:budget_id>/"
    _service = budgetService

    def get(self, category_id):
        return self._read(category_id)

    def put(self, category_id):
        return self._update(category_id, request.json)

    def delete(self, category_id):
        return self._delete(category_id)


class AssetListController(components.Controller):
    path = "/estate/assets/"
    _service = assetService

    def get(self):
        return self._fetch_all()
    
    def post(self):
        return self._create(request.json)


class AssetController(components.Controller):
    path = "/estate/assets<int:category_id>/"
    _service = assetService

    def get(self, category_id):
        return self._read(category_id)

    def put(self, category_id):
        return self._update(category_id, request.json)

    def delete(self, category_id):
        return self._delete(category_id)
