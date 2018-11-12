from django import template
register = template.Library()


@register.filter(name='get_weights')
def get_weights_filter(person):
    # return person.user.username
    if person.access_token is not None:
        return person.get_weights()
    else:
        return []


@register.filter(name='get_days')
def get_weights_filter(person):
    # return person.user.username
    return person.get_days()
