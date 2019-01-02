# coding=utf-8

import components
from budget.model import Budget, Saving

class BudgetService(components.Service):
    _model_class = Budget
    # TBD
    pass

budgetService = BudgetService()

class SavingService(components.Service):
    _model_class = Saving
    # TBD
    pass

savingService = SavingService()

def init(app, api, models):
    from budget.controller import BudgetController, BudgetListController
    from budget.controller import SavingController, SavingListController
    components.register_controllers(api, [
        BudgetController, BudgetListController, 
        SavingController, SavingListController
    ])
    models.extend([Budget, Saving])
    pass
