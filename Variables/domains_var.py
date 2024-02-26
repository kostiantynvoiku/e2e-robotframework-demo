from robot.libraries.BuiltIn import BuiltIn

START_URL = BuiltIn().get_variable_value("${START_URL}")
COUNTRY = ""
COUNTRY_CODE = ""
LOCALE = ""
ENV = "sandbox"

DOMAIN_URLS = [
                "https://www.starofservice.be/",
                "https://www.starofservice.ch/",
                "https://www.starofservice.lu/"
]

DOMAIN = {
    "fr_locale": {
        "be": {
            "country": "Belgium",
            "url": "starofservice.be/"
        },
        "ch": {
            "country": "Switzerland",
            "url": "starofservice.ch/"
        },
        "lu": {
            "country": "Luxembourg",
            "url": "starofservice.lu/"
        },
    },
}

for key, dict in DOMAIN.items():
    for subkey, subvalue in dict.items():
        if subvalue["url"] in START_URL:
            COUNTRY_CODE = subkey
            COUNTRY = subvalue["country"]
