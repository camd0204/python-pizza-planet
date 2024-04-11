import pytest
from app.controllers.report import ReportController

def test_get_top_ingredient(app):
    controller=ReportController()
    pytest.assume(controller.get_top_ingredient() is not None)

def test_get_top_customers(app):
    controller=ReportController()
    pytest.assume(controller.get_top_customers() is not None)

def test_get_most_earning_month(app):
    controller=ReportController()
    pytest.assume(controller.get_most_earning_month() is not None)
    
def test_get_report(app):
    controller=ReportController()
    pytest.assume(controller.get_report())