from mimesis import Person, Business, Address, Text, Food
from robot.api.deco import keyword


locales = {
    "cz_locale": "cs",
    "de_locale": "de",
    "gr_locale": "el",
    "es_locale": "es",
    "fr_locale": "fr",
    "hu_locale": "hu",
    "is_locale": "is",
    "it_locale": "it",
    "jp_locale": "ja",
    "nl_locale": "nl",
    "pl_locale": "pl",
    "pt_locale": "pt",
    "br_locale": "pt-br",
    "ru_locale": "ru",
    "se_locale": "sv",
    "tr_locale": "tr",
    "ua_locale": "uk",
    "cn_locale": "zh",
    "eng_locale": "en"
}


def get_locale(sos_locale):
    locale = ""
    for loc in locales:
        if loc == sos_locale:
            locale = locales[loc]
            break
        else:
            locale = locales["eng_locale"]
    return locale


@keyword
def generate_random_text(num=2, sos_locale='en'):
    """

    'num': No of sentences;
    By default "num=2".

    Example:
    ${random_text}   generate random text    5
    input text       css=locator             ${random_text}

    """
    locale = get_locale(sos_locale)
    text = Text(locale)
    return text.text(quantity=int(num)).replace("""'""", """ """).replace('''"''', """ """).replace('''&''', ''' ''')


@keyword
def generate_random_first_name(sos_locale='en'):
    locale = get_locale(sos_locale)
    person = Person(locale)
    return person.first_name().split()[0].title().replace("""'""", """ """).replace('''"''', """ """)


@keyword
def generate_random_last_name(sos_locale='en'):
    locale = get_locale(sos_locale)
    person = Person(locale)
    return person.last_name().split()[0].title().replace("""'""", """ """).replace('''"''', """ """)


@keyword
def generate_random_address(sos_locale='en'):
    locale = get_locale(sos_locale)
    address = Address(locale)
    return address.address()


@keyword
def generate_random_business_name(sos_locale='en'):
    locale = get_locale(sos_locale)
    food, business = Food(locale), Business(locale)
    return f"{food.fruit()} {business.company_type(abbr=True)}".capitalize().replace("""'""", """ """).replace('''"''', """ """).replace('''&''', ''' ''')


@keyword
def generate_job_title(sos_locale='en'):
    locale = get_locale(sos_locale)
    person = Person(locale)
    return person.occupation().replace("""'""", """ """).replace('''"''', """ """)
