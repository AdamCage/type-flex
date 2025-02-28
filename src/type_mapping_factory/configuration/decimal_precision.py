class DecimalPrecision:
    """Precision configuration for decimal types."""
    
    def __init__(self, max_digits: int = 20, decimal_places: int = 4):
        self.max_digits = max_digits
        self.decimal_places = decimal_places
