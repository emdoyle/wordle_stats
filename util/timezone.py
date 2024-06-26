from datetime import datetime
from itertools import islice
from typing import List, Optional, Tuple
from zoneinfo import ZoneInfo

from slack_bolt import App

from app.constants import TIMEZONE_CUSTOM_KEY

PACIFIC_TIMEZONE_NAME = "America/Los_Angeles"
PACIFIC_TIME = ZoneInfo("America/Los_Angeles")


ALL_TIMEZONES = [
    "America/Martinique",
    "Pacific/Saipan",
    "Asia/Shanghai",
    "Asia/Oral",
    "Europe/Volgograd",
    "Antarctica/Mawson",
    "Antarctica/Davis",
    "Europe/Stockholm",
    "Africa/Algiers",
    "Pacific/Apia",
    "Pacific/Wake",
    "Etc/GMT-14",
    "America/Denver",
    "America/Cayman",
    "Europe/Zurich",
    "Asia/Yerevan",
    "Asia/Tbilisi",
    "CET",
    "Antarctica/Palmer",
    "Europe/Minsk",
    "Africa/Lagos",
    "Europe/Astrakhan",
    "America/Nome",
    "America/Maceio",
    "America/Argentina/Buenos_Aires",
    "America/Thunder_Bay",
    "Pacific/Norfolk",
    "Asia/Macau",
    "America/Indiana/Petersburg",
    "Pacific/Guam",
    "Asia/Samarkand",
    "Africa/Johannesburg",
    "Atlantic/Reykjavik",
    "America/Chicago",
    "Asia/Riyadh",
    "Asia/Krasnoyarsk",
    "Europe/Chisinau",
    "America/North_Dakota/Beulah",
    "Etc/GMT+8",
    "Europe/Podgorica",
    "Factory",
    "Atlantic/Cape_Verde",
    "Europe/Zaporozhye",
    "Africa/Tripoli",
    "Pacific/Auckland",
    "PST8PDT",
    "America/Indiana/Tell_City",
    "Europe/London",
    "Pacific/Chuuk",
    "America/Atikokan",
    "Africa/Lusaka",
    "America/Indiana/Marengo",
    "America/Argentina/Jujuy",
    "America/Tortola",
    "Asia/Aqtobe",
    "America/Hermosillo",
    "GMT",
    "America/Recife",
    "America/Resolute",
    "America/Caracas",
    "Asia/Tokyo",
    "Africa/Kinshasa",
    "Indian/Antananarivo",
    "Australia/Lindeman",
    "Europe/Bucharest",
    "America/Managua",
    "Pacific/Rarotonga",
    "America/Grenada",
    "Etc/GMT+11",
    "Etc/GMT+1",
    "Europe/Bratislava",
    "Asia/Kathmandu",
    "America/Panama",
    "America/Cambridge_Bay",
    "America/Sitka",
    "America/Kentucky/Louisville",
    "Asia/Urumqi",
    "America/Indiana/Winamac",
    "Europe/Copenhagen",
    "Africa/Cairo",
    "America/Noronha",
    "Asia/Singapore",
    "Antarctica/Syowa",
    "America/St_Kitts",
    "America/Guayaquil",
    "Australia/Lord_Howe",
    "Europe/Ljubljana",
    "Africa/Nouakchott",
    "Europe/Sofia",
    "Africa/Ouagadougou",
    "Europe/Simferopol",
    "Europe/Mariehamn",
    "Africa/El_Aaiun",
    "Indian/Comoro",
    "Australia/Darwin",
    "Europe/Samara",
    "America/Manaus",
    "Africa/Douala",
    "Asia/Qostanay",
    "Indian/Maldives",
    "Europe/Warsaw",
    "Australia/Adelaide",
    "Antarctica/Vostok",
    "Africa/Brazzaville",
    "Africa/Lubumbashi",
    "Pacific/Niue",
    "Asia/Kuching",
    "America/Chihuahua",
    "Etc/GMT-5",
    "Australia/Perth",
    "Europe/Istanbul",
    "Etc/GMT-11",
    "America/North_Dakota/New_Salem",
    "America/Merida",
    "America/Toronto",
    "Europe/Athens",
    "Asia/Amman",
    "Europe/Oslo",
    "Asia/Gaza",
    "America/Argentina/Rio_Gallegos",
    "Pacific/Fiji",
    "Europe/Kirov",
    "America/Miquelon",
    "Africa/Banjul",
    "Asia/Irkutsk",
    "Asia/Nicosia",
    "Asia/Jerusalem",
    "WET",
    "Atlantic/Azores",
    "America/Rainy_River",
    "America/Monterrey",
    "Africa/Bujumbura",
    "America/Yakutat",
    "Pacific/Pohnpei",
    "Asia/Vladivostok",
    "Asia/Jakarta",
    "America/Curacao",
    "America/Argentina/Mendoza",
    "America/Lima",
    "Africa/Tunis",
    "America/Nipigon",
    "America/St_Vincent",
    "America/Bahia",
    "Africa/Monrovia",
    "America/Menominee",
    "Pacific/Midway",
    "Etc/GMT-1",
    "Europe/Vilnius",
    "Europe/Vatican",
    "Pacific/Pitcairn",
    "Europe/Saratov",
    "Asia/Bahrain",
    "Asia/Dili",
    "America/La_Paz",
    "America/Indiana/Vevay",
    "America/Iqaluit",
    "America/Argentina/Cordoba",
    "Pacific/Funafuti",
    "Europe/Kiev",
    "America/Boise",
    "Pacific/Easter",
    "America/Metlakatla",
    "Asia/Yangon",
    "Pacific/Kosrae",
    "Asia/Yakutsk",
    "Antarctica/Rothera",
    "Asia/Bishkek",
    "America/Argentina/Salta",
    "Asia/Qatar",
    "Australia/Melbourne",
    "America/Indiana/Vincennes",
    "America/Adak",
    "Pacific/Kiritimati",
    "Asia/Sakhalin",
    "Etc/GMT-2",
    "Etc/UTC",
    "Europe/Skopje",
    "Indian/Mauritius",
    "Asia/Dushanbe",
    "Asia/Chita",
    "Asia/Kuwait",
    "Europe/Luxembourg",
    "Africa/Dakar",
    "Europe/Guernsey",
    "America/Lower_Princes",
    "Europe/Malta",
    "America/Barbados",
    "Asia/Aqtau",
    "America/Kralendijk",
    "Pacific/Marquesas",
    "America/Bahia_Banderas",
    "Atlantic/South_Georgia",
    "America/Anguilla",
    "America/Danmarkshavn",
    "Asia/Ashgabat",
    "MST7MDT",
    "Asia/Dubai",
    "Europe/Lisbon",
    "Europe/Jersey",
    "Asia/Srednekolymsk",
    "America/Thule",
    "America/St_Thomas",
    "Pacific/Kwajalein",
    "EST",
    "Etc/GMT+12",
    "Asia/Tashkent",
    "Africa/Mogadishu",
    "America/Winnipeg",
    "Pacific/Tongatapu",
    "Australia/Hobart",
    "Africa/Malabo",
    "America/New_York",
    "Europe/Amsterdam",
    "Asia/Pontianak",
    "America/Inuvik",
    "Indian/Christmas",
    "Europe/Tirane",
    "America/Paramaribo",
    "America/Santarem",
    "America/Montevideo",
    "Etc/GMT-4",
    "Etc/Greenwich",
    "Atlantic/Canary",
    "Pacific/Palau",
    "America/Grand_Turk",
    "Pacific/Fakaofo",
    "America/Asuncion",
    "Etc/Zulu",
    "Asia/Yekaterinburg",
    "Asia/Kabul",
    "America/Nuuk",
    "Australia/Eucla",
    "America/Phoenix",
    "America/Santiago",
    "America/Dominica",
    "Etc/GMT0",
    "Asia/Anadyr",
    "America/North_Dakota/Center",
    "Asia/Damascus",
    "Etc/GMT+10",
    "Europe/Vaduz",
    "America/Rankin_Inlet",
    "Etc/Universal",
    "Africa/Kigali",
    "Asia/Choibalsan",
    "Africa/Maseru",
    "Africa/Libreville",
    "Pacific/Guadalcanal",
    "America/Guatemala",
    "Europe/Zagreb",
    "America/Juneau",
    "Asia/Karachi",
    "Pacific/Kanton",
    "America/Creston",
    "America/Santo_Domingo",
    "America/Whitehorse",
    "Etc/GMT+3",
    "America/Sao_Paulo",
    "Africa/Nairobi",
    "America/Detroit",
    "Antarctica/McMurdo",
    "Etc/GMT+7",
    "Etc/GMT-3",
    "Asia/Baku",
    "America/Argentina/Catamarca",
    "Etc/GMT-0",
    "America/Yellowknife",
    "Africa/Windhoek",
    "America/Fortaleza",
    "America/Blanc-Sablon",
    "America/Dawson_Creek",
    "America/El_Salvador",
    "Europe/Andorra",
    "Indian/Chagos",
    "Africa/Harare",
    "Asia/Ust-Nera",
    "Asia/Dhaka",
    "Asia/Seoul",
    "America/Mexico_City",
    "America/Cayenne",
    "Europe/Berlin",
    "Europe/Dublin",
    "Africa/Mbabane",
    "Indian/Cocos",
    "Asia/Hovd",
    "Pacific/Majuro",
    "Europe/Budapest",
    "America/Marigot",
    "Europe/Madrid",
    "Asia/Kamchatka",
    "America/Argentina/Ushuaia",
    "Etc/GMT+4",
    "Etc/GMT-6",
    "Africa/Kampala",
    "Europe/San_Marino",
    "America/Indiana/Indianapolis",
    "MET",
    "Pacific/Tarawa",
    "America/Nassau",
    "America/Eirunepe",
    "Etc/GMT-10",
    "America/Goose_Bay",
    "Asia/Jayapura",
    "Etc/GMT-9",
    "America/Swift_Current",
    "America/Edmonton",
    "America/Argentina/San_Luis",
    "Europe/Belgrade",
    "Asia/Barnaul",
    "HST",
    "America/Campo_Grande",
    "Asia/Almaty",
    "Pacific/Port_Moresby",
    "America/Punta_Arenas",
    "Asia/Novokuznetsk",
    "Asia/Vientiane",
    "Etc/GMT+5",
    "Indian/Mahe",
    "Europe/Brussels",
    "Atlantic/Bermuda",
    "America/Cuiaba",
    "Africa/Bamako",
    "America/Cancun",
    "America/Havana",
    "America/Costa_Rica",
    "America/St_Johns",
    "Europe/Uzhgorod",
    "Africa/Ndjamena",
    "Africa/Khartoum",
    "Asia/Omsk",
    "Europe/Isle_of_Man",
    "Atlantic/St_Helena",
    "Antarctica/DumontDUrville",
    "Atlantic/Faroe",
    "Africa/Juba",
    "EET",
    "Asia/Baghdad",
    "Antarctica/Troll",
    "Africa/Freetown",
    "Africa/Djibouti",
    "America/Puerto_Rico",
    "Africa/Niamey",
    "Europe/Gibraltar",
    "Europe/Tallinn",
    "America/Araguaina",
    "Etc/GMT-8",
    "Asia/Magadan",
    "CST6CDT",
    "America/Anchorage",
    "Etc/GMT-13",
    "Europe/Rome",
    "EST5EDT",
    "America/Scoresbysund",
    "America/Vancouver",
    "Etc/GMT+2",
    "Pacific/Bougainville",
    "Pacific/Tahiti",
    "Africa/Bangui",
    "Africa/Accra",
    "America/Mazatlan",
    "America/St_Lucia",
    "Pacific/Noumea",
    "America/Antigua",
    "Asia/Novosibirsk",
    "America/Belem",
    "Africa/Casablanca",
    "Africa/Conakry",
    "Asia/Tomsk",
    "Africa/Dar_es_Salaam",
    "Australia/Broken_Hill",
    "America/Indiana/Knox",
    "America/Halifax",
    "Asia/Muscat",
    "Africa/Luanda",
    "MST",
    "Asia/Famagusta",
    "Pacific/Nauru",
    "America/Port-au-Prince",
    "America/Los_Angeles",
    "Asia/Kuala_Lumpur",
    "America/Ojinaga",
    "Africa/Blantyre",
    "Asia/Taipei",
    "America/Fort_Nelson",
    "America/Jamaica",
    "Asia/Qyzylorda",
    "Pacific/Wallis",
    "Europe/Helsinki",
    "Africa/Maputo",
    "America/Boa_Vista",
    "America/Dawson",
    "America/Regina",
    "Europe/Moscow",
    "Africa/Abidjan",
    "Africa/Bissau",
    "Europe/Ulyanovsk",
    "Asia/Hebron",
    "Atlantic/Madeira",
    "Pacific/Galapagos",
    "Asia/Ho_Chi_Minh",
    "America/Kentucky/Monticello",
    "Asia/Phnom_Penh",
    "Europe/Vienna",
    "Asia/Atyrau",
    "America/Glace_Bay",
    "Antarctica/Casey",
    "Etc/GMT+0",
    "Australia/Sydney",
    "Africa/Gaborone",
    "Asia/Beirut",
    "Pacific/Efate",
    "Asia/Thimphu",
    "Antarctica/Macquarie",
    "Africa/Sao_Tome",
    "Etc/GMT-12",
    "America/Bogota",
    "Indian/Kerguelen",
    "Africa/Lome",
    "America/St_Barthelemy",
    "America/Montserrat",
    "America/Aruba",
    "Asia/Colombo",
    "America/Guadeloupe",
    "Asia/Hong_Kong",
    "Indian/Mayotte",
    "Africa/Porto-Novo",
    "Pacific/Pago_Pago",
    "Asia/Pyongyang",
    "Europe/Busingen",
    "Asia/Khandyga",
    "Europe/Prague",
    "Europe/Monaco",
    "Europe/Paris",
    "America/Porto_Velho",
    "Arctic/Longyearbyen",
    "Etc/GMT+9",
    "Pacific/Chatham",
    "Asia/Istanbul",
    "Europe/Kaliningrad",
    "America/Argentina/La_Rioja",
    "Europe/Nicosia",
    "Asia/Kolkata",
    "Europe/Sarajevo",
    "Australia/Brisbane",
    "America/Argentina/Tucuman",
    "Asia/Brunei",
    "Indian/Reunion",
    "Africa/Ceuta",
    "America/Tijuana",
    "Asia/Tehran",
    "America/Belize",
    "America/Guyana",
    "Etc/GMT-7",
    "Asia/Aden",
    "America/Moncton",
    "America/Pangnirtung",
    "Africa/Addis_Ababa",
    "Etc/GMT+6",
    "Africa/Asmara",
    "Atlantic/Stanley",
    "America/Matamoros",
    "America/Argentina/San_Juan",
    "Asia/Manila",
    "America/Tegucigalpa",
    "America/Port_of_Spain",
    "Pacific/Gambier",
    "Europe/Riga",
    "Pacific/Honolulu",
    "Asia/Makassar",
    "Asia/Bangkok",
    "Asia/Ulaanbaatar",
    "America/Rio_Branco",
    "Etc/GMT",
]


def get_hour_offset(timezone: str) -> float:
    now = datetime.now()
    return ZoneInfo(timezone).utcoffset(now).total_seconds() / 3600


def display_timezone(timezone: str) -> str:
    offset = get_hour_offset(timezone)
    if offset > 0:
        return f"(UTC+{offset}) {timezone}"
    return f"(UTC-{abs(offset)}) {timezone}"


def add_display_name_to_timezone(timezone: str) -> Tuple[str, str]:
    return display_timezone(timezone), timezone


def search_timezones(query: str = "", max_results: int = 8) -> List[Tuple[str, str]]:
    timezones_with_display = map(add_display_name_to_timezone, ALL_TIMEZONES)
    if not query:
        return list(islice(timezones_with_display, max_results))
    query = query.lower().strip()
    results = []
    while len(results) < max_results:
        try:
            timezone_display, timezone_value = next(timezones_with_display)
        except StopIteration:
            return results
        if query in timezone_display.lower():
            results.append((timezone_display, timezone_value))
    return results


def get_timezone_for_team(app: "App", team_id: str) -> Optional["ZoneInfo"]:
    installation = app.installation_store.find_installation(
        enterprise_id=None, team_id=team_id
    )
    if installation is None:
        return None
    raw_timezone = installation.get_custom_value(name=TIMEZONE_CUSTOM_KEY)
    return ZoneInfo(raw_timezone) if raw_timezone is not None else PACIFIC_TIME
