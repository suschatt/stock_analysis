import math
import numpy as np

def format_metric(value, is_percentage=False, is_currency=False):
    """
    Formats metric values into human-readable strings for GPT.
    
    Args:
        value: numeric value or None
        is_percentage: bool, format as percentage if True
        is_currency: bool, format as currency if True
    
    Returns:
        str: formatted value, or "N/A" if missing
    """
    if value is None or (isinstance(value, float) and math.isnan(value)) or (isinstance(value, np.generic) and np.isnan(value)):
        return "N/A"

    # Percentage formatting
    if is_percentage:
        return f"{value * 100:.2f}%"

    # Currency formatting
    if is_currency:
        abs_val = abs(value)
        if abs_val >= 1e9:
            return f"${value/1e9:.2f}B"
        elif abs_val >= 1e6:
            return f"${value/1e6:.2f}M"
        else:
            return f"${value:,.0f}"

    # Plain number formatting with commas
    if isinstance(value, (int, float)):
        return f"{value:,.2f}"

    return str(value)
