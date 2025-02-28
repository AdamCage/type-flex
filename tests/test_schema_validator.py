from .src import SchemaValidator


def test_simple_validation():
    validator = SchemaValidator()
    schema = {'age': {'type': 'int', 'constraints': {'ge': 18}}}
    
    assert validator.validate({'age': 20}, schema)['valid']
    result = validator.validate({'age': 15}, schema)
    assert not result['valid']
    assert result['errors'][0]['error'] == "Input should be greater than or equal to 18"


def test_nested_validation():
    schema = {
        'user': {
            'type': 'nested',
            'schema': {
                'email': {'type': 'email'},
                'score': {'type': 'float', 'constraints': {'le': 100}}
            }
        }
    }
    
    data_valid = {'user': {'email': 'test@example.com', 'score': 95.5}}
    data_invalid = {'user': {'email': 'invalid', 'score': 150}}
    
    validator = SchemaValidator()
    assert validator.validate(data_valid, schema)['valid']
    result = validator.validate(data_invalid, schema)
    assert len(result['errors']) == 2


def test_category_type_validation():
    schema = {'status': {'type': 'category', 'allowed_values': ['active', 'inactive']}}
    validator = SchemaValidator()
    
    assert validator.validate({'status': 'active'}, schema)['valid']
    result = validator.validate({'status': 'unknown'}, schema)
    assert not result['valid']
    assert "Input should be 'active' or 'inactive'" in result['errors'][0]['error']