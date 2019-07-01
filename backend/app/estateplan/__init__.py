# coding=utf-8

from app import components
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


class Module (components.Module):
    from app.estateplan.controller import AssetController, AssetListController
    from app.estateplan.controller import BudgetController, BudgetListController
    name = "estateplan"
    services = [assetService, budgetService]
    models = [Budget, Asset, LastAssetCalculationCache]
    controllers = [AssetController, AssetListController, BudgetController, BudgetListController]


module = Module()
