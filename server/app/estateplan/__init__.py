# coding=utf-8

from app from app import components
from app.estateplan.model import Budget, Asset, LastAssetCalculationCache


class BudgetService(components.Service):
    _model_class = Budget
    # TBD
    pass


budgetService = BudgetService()


class AssetService(components.Service):
    _model_class = Asset
    # TBD
    pass


assetService = AssetService()


def init(app, api, models):
    from estateplan.controller import BudgetController, BudgetListController
    from estateplan.controller import AssetController, AssetListController
    components.register_controllers(api, [
        BudgetController, BudgetListController,
        AssetController, AssetListController
    ])
    models.extend([Budget, Asset, LastAssetCalculationCache])
    pass
