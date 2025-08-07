from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide the value by the argument."""
    try:
        return float(value) / float(arg) if float(arg) != 0 else 0
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """Calculate percentage of value relative to total."""
    try:
        if float(total) == 0:
            return 0
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, TypeError):
        return 0

@register.filter
def grade(percentage):
    """Return grade based on percentage."""
    try:
        percent = float(percentage)
        if percent >= 70:
            return 'success'
        elif percent >= 50:
            return 'warning'
        else:
            return 'danger'
    except (ValueError, TypeError):
        return 'secondary'

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return None
