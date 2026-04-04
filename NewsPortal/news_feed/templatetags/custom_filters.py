from django import template


register = template.Library()

BAD_WORDS = [
    'Налог',
    'налог',
    'несправедливость',
    'ликвидировать'
]

@register.filter()
def censor(text: str):
    if type(text) != str:
        raise ValueError('Фильтр должен применяться только к переменным строкового типа.')
    censored_text = ''
    for word in text.split(' '):
        _word = word.strip('!.,«»')
        if _word in BAD_WORDS:
            word = word.replace(_word, _word[0] + '*' * (len(_word)-1))
        censored_text += f' {word}'
    return censored_text


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    request = context['request'].GET.copy()
    for key, value in kwargs.items():
        request[key] = value
    return request.urlencode()