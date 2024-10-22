from django import template

register = template.Library()

@register.filter
def rupiah_format(value):
    try:
        value = float(value)  # Convert the value to float
        # Format the value as "2.000.000"
        formatted_value = "{:,.0f}".format(value).replace(",", ".")
        return formatted_value
    except (ValueError, TypeError):
        return value  # Return the original value if there's an error
