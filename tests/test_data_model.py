from pydantic import ValidationError
import pytest

from .src import DataModel


def test_dynamic_model_creation():
    schema = {
        'email': {'type': 'email'},
        'balance': {'type': 'decimal', 'constraints': {'gt': 0}}
    }
    
    UserModel = DataModel.build_model(schema)
    instance = UserModel(email="test@example.com", balance=100.5)
    assert instance.email == "test@example.com"
    assert float(instance.balance) == 100.5
    
    with pytest.raises(ValidationError):
        UserModel(email="invalid", balance=-10)