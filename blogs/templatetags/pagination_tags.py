from django import template

# This creates a "library" where we register our custom tags
register = template.Library()


# @register.simple_tag means: "Hey Django, this is a custom tag!"
# takes_context=True means: "Give me access to the request object"
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    This tag preserves existing URL parameters and updates with new ones.

    Example:
    Current URL: /blogs/?q=django&category=tech&page=3
    Call: {% url_replace page=5 %}
    Result: /blogs/?q=django&category=tech&page=5

    It keeps 'q' and 'category', but replaces 'page' with 5!
    """
    # Get a copy of all current URL parameters
    query = context['request'].GET.copy()

    # Update/add the new parameters we passed in
    for key, value in kwargs.items():
        query[key] = value

    # Convert back to URL format: "q=django&page=5"
    return query.urlencode()