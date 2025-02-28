# Type Flex 🔄

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PyPI Version](https://img.shields.io/pypi/v/type-mapper.svg)](https://pypi.org/project/type-mapper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Универсальная система типизации и валидации данных для Python с поддержкой кастомных типов и конфигураций.

## Основные возможности 🚀

- 📌 Динамический маппинг типов данных
- ✅ Валидация сложных структур данных
- ⚙️ Поддержка YAML/XML конфигураций
- 🔄 Интеграция с Pydantic моделями
- 🛠️ Расширение через кастомные типы
- 🛡️ Безопасная обработка данных (XML Bomb protection)

## Установка 📦

```bash
pip install type-mapper
```

Требования: Python 3.8+

## Быстрый старт 🏁

### Базовый маппинг типов

```python
from type_mapper import map_types
from decimal import Decimal

# Простые типы
int_type = map_types('int')  # <class 'int'>

# Типы с параметрами
decimal_type = map_types('decimal', gt=0, max_digits=10)  # ConstrainedDecimal

# Специальные форматы
email_type = map_types('email')  # pydantic.EmailStr
```

### Валидация данных

```python
from type_mapper import SchemaValidator

schema = {
    'user': {
        'type': 'nested',
        'schema': {
            'id': {'type': 'uuid'},
            'balance': {'type': 'decimal', 'precision': 'currency'}
        }
    }
}

validator = SchemaValidator()
data = {
    'user': {
        'id': '550e8400-e29b-41d4-a716-446655440000',
        'balance': Decimal('150.75')
    }
}

assert validator.validate(data, schema) is True
```

## Конфигурация ⚙️

### Кастомные типы

```python
from type_mapper import TypeConfig

# Регистрация нового типа
TypeConfig.register_custom_type(
    name='geo_point',
    handler=tuple[float, float]
)

# Использование
point_type = map_types('geo_point')
```

### Загрузка конфигураций

```yaml
# config.yaml
types:
  currency:
    base_type: decimal
    max_digits: 12
    decimal_places: 4

adapters:
  xml:
    security_mode: paranoid
```

```python
TypeConfig.load_config('config.yaml')
```

## Расширенные возможности 🧠

### Динамические модели Pydantic

```python
from type_mapper import DataModel

schema = {
    'email': {'type': 'email'},
    'transactions': {
        'type': 'array',
        'items': {
            'type': 'decimal',
            'precision': 'currency'
        }
    }
}

UserModel = DataModel.build_model(schema)
model = UserModel(email="user@domain.com", transactions=["100.50", "200.75"])
print(model.transactions)  # [Decimal('100.5000'), Decimal('200.7500')]
```

### Безопасная обработка XML

```python
from type_mapper.adapters import XMLAdapter

secure_xml = XMLAdapter.to_dict(xml_data, safe=True)  # Защита от XML-атак
```

## Интеграции 🔗

### Поддерживаемые форматы

| Формат | Адаптер       | Особенности               |
|--------|---------------|---------------------------|
| YAML   | YAMLAdapter   | Безопасный парсинг       |
| XML    | XMLAdapter    | Защита от XML Bomb       |
| JSON   | JSONAdapter   | Стандартная реализация   |

## Контрибьютинг 🤝

Приветствуются пулреквесты и issue! Перед внесением изменений:

1. Установите dev-зависимости:
    ```bash
    pip install -r requirements-dev.txt
    ```

2. Запустите тесты:
    ```bash
    pytest --cov=type_mapper tests/
    ```

3. Проверьте стиль кода:
    ```bash
    flake8 && mypy .
    ```

## ⚠️ Важно
Проект находится в активной разработке. Основные направления:

1. Реализовать адаптеры для:
   - GraphQL схем
   - Protobuf
   - Avro
2. Добавить поддержку:
   - Динамического обновления конфигураций
   - Версионирования схем
   - Миграции типов
3. Внедрить:
   - Тестирование на fuzzing-данных
   - SAST-анализ кода
   - Официальный security audit
4. Разработать:
   - UI для визуализации схем
   - IDE плагины для автодополнения
   - CI/CD шаблоны для безопасного деплоя

## Лицензия 📄

MIT License. Подробнее в файле LICENSE.

---

Разработано с ❤️ для сообщества Python. Автор: Кищак Богдан | yytrby@gmail.com | Telegram: @AdamCage
