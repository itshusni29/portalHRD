from django import template

register = template.Library()

@register.filter
def get_manager_status(statuses):
    """Check if 'manager_approved' exists in the statuses."""
    return any(status.status == 'manager_approved' for status in statuses)

@register.filter
def get_gm_status(statuses):
    """Check if 'gm_approved' exists in the statuses."""
    return any(status.status == 'gm_approved' for status in statuses)

@register.filter
def get_hrd_status(statuses):
    """Check if 'hrd_approved' exists in the statuses."""
    return any(status.status == 'hrd_approved' for status in statuses)
