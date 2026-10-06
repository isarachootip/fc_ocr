import pytest
from datetime import datetime
from unittest.mock import MagicMock
from app.services.running_number import generate_vendor_code

def test_generate_vendor_code_empty_db():
    db = MagicMock()
    # Mock scalar_one_or_none returning None
    db.execute.return_value.scalar_one_or_none.return_value = None

    test_date = datetime(2026, 10, 6)
    code = generate_vendor_code(db, target_date=test_date)
    assert code == "V061020260001"

def test_generate_vendor_code_increment():
    db = MagicMock()
    # Mock existing highest code
    db.execute.return_value.scalar_one_or_none.return_value = "V061020260014"

    test_date = datetime(2026, 10, 6)
    code = generate_vendor_code(db, target_date=test_date)
    assert code == "V061020260015"
