from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def is_allowed_user(user, allowed_roles=[]):
    if user.groups.exists():
        user_groups = user.groups.values_list('name', flat=True)
        return any(group in allowed_roles for group in user_groups)
    return False
