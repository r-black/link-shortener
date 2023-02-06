from django.test import TestCase

from .forms import URLShortenerForm

URL = 'https://www.google.com/'


class TestURLShortenerFormValidation(TestCase):
    """
    Test form validation of URLShortenerForm. Not testing URL validation
    because URL validation is done by Django.
    """

    def test_alias_validation(self):

        VALID_ALIASES = ('there-you-go', 'this_is_okay', '42',
                         '63as', 'alex42thegreat', 'R2-D2', 'E_D12')
        INVALID_ALIASES = ('stop$', '@asd', '#jgkl', '+hbwler', 'learn&grow', 'easy_peasy/', '/bye', ':huh', '(nope)',
                           '^acute', 'perc%tile', 'a*terisk', '<tag', 'you>', "'cause", '"possible"', '\\back', '=eq',
                           '|pipe', 'an{', 'fg}d', 'back`t', 'til~e', 'polls:index')

        for alias in VALID_ALIASES:
            form = URLShortenerForm(data={'url': URL, 'alias': alias})
            self.assertTrue(form.is_valid())

        for alias in INVALID_ALIASES:
            form = URLShortenerForm(data={'url': URL, 'alias': alias})
            self.assertTrue(not form.is_valid())
