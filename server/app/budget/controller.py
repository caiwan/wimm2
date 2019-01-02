from flask import request
import components

from budget import budgetService, savingService


class BudgetListController(components.Controller):
    path = "/budget/"
    _service = budgetService

    def get(self):
        return self._fetch_all()
    
    def post(self):
        return self._create(request.json)


class BudgetController(components.Controller):
    path = "/budget/<int:budget_id>/"
    _service = budgetService

    def get(self, category_id):
        return self._read(category_id)

    def put(self, category_id):
        return self._update(category_id, request.json)

    def delete(self, category_id):
        return self._delete(category_id)


class SavingListController(components.Controller):
    path = "/savings/"
    _service = savingService

    def get(self):
        return self._fetch_all()
    
    def post(self):
        return self._create(request.json)


class SavingController(components.Controller):
    path = "/savings<int:category_id>/"
    _service = savingService

    def get(self, category_id):
        return self._read(category_id)

    def put(self, category_id):
        return self._update(category_id, request.json)

    def delete(self, category_id):
        return self._delete(category_id)
