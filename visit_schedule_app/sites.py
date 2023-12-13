from edc_sites.single_site import SingleSite
from edc_sites.site import sites

suffix = "clinicedc.org"
language_codes = ["en"]
sites.register(
    SingleSite(
        10,
        "mochudi",
        title="Mochudi",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        domain=f"mochudi.bw.{suffix}",
    ),
    SingleSite(
        20,
        "molepolole",
        title="Molepolole",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        domain=f"molepolole.bw.{suffix}",
    ),
    SingleSite(
        30,
        "lobatse",
        title="Lobatse",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        domain=f"lobatse.bw.{suffix}",
    ),
    SingleSite(
        40,
        "gaborone",
        title="Gaborone",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        domain=f"gaborone.bw.{suffix}",
    ),
    SingleSite(
        50,
        "karakobis",
        title="Karakobis",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        domain=f"karakobis.bw.{suffix}",
    ),
    SingleSite(
        60,
        "windhoek",
        title="Windhoek",
        country="namibia",
        country_code="na",
        language_codes=language_codes,
        domain=f"windhoek.bw.{suffix}",
    ),
)
