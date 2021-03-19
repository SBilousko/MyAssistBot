import requests, constants, re, bot_token
from bs4 import BeautifulSoup

def check_connection(url):
    if requests.get(url).ok:
        return True
    else:
        return False

def get_soup(url):
    if check_connection(url):
        return BeautifulSoup(requests.get(url).text, "html.parser")
    else:
        return "Помилка " + str(requests.get(url).status_code)


def sinoptik_weather(url=constants.sinoptik_url, city=constants.default_city, n=3):
    parse_url = url + city
    soup = get_soup(parse_url)
    weather = soup.find(id="blockDays")
    date = weather.find(class_="day-link").string + ", " + weather.find(class_="date").string + " " + weather.find(class_="month").string
    weather_describe = weather.find(class_="weatherIco")["title"]
    temperature = "Температура повітря " + weather.find(class_="temperature").find(class_="min").span.string + " " + weather.find(class_="temperature").find(class_="max").span.string
    full_description = weather.find(class_="wDescription").find(class_="description").text.strip()

    weather_for_today = date + "\n" + weather_describe + "\n" + temperature + "\n" + full_description + "\n\n"

    # Погода на наступні n днів
    weather_for_few_days = ""
    if n > 6:
        weather_for_few_days = constants.too_much
    elif n < 1:
        weather_for_few_days = constants.too_few
    else:
        for i in range(2, n+2):
            id_ = "bd" + str(i)
            n_weather = weather.find(id=id_)
            n_date = n_weather.find(class_="day-link").string + ", " + n_weather.find(class_="date").string + " " + n_weather.find(class_="month").string
            n_weather_describe = n_weather.find(class_="weatherIco")["title"]
            n_temperature = "Температура повітря " + n_weather.find(class_="temperature").find(class_="min").span.string + " " + n_weather.find(class_="temperature").find(class_="max").span.string

            weather_for_few_days += n_date + "\n" + n_weather_describe + "\n" + n_temperature + "\n\n"

    return weather_for_today, weather_for_few_days


def minfin_currency(url=constants.minfin_currency_url):
    soup = get_soup(url)
    currency_table = soup.find(class_="mfcur-table-lg-currency")
    curs = currency_table.find("tbody").findAll("td")
    usd = []
    eur = []
    rub = []
    for i in range(1, 4):
        usd.append(curs[i].findAll(text = re.compile("\d")))
    for i in range(5, 8):
        eur.append(curs[i].findAll(text = re.compile("\d")))
    for i in range(9, 12):
        rub.append(curs[i].findAll(text = re.compile("\d")))

    if len(usd[0]) == 0:
        usd_bank = "-"
    else:
        usd_bank = usd[0][0].strip() + "/" + usd[0][-1].strip()

    if len(eur[0]) == 0:
        eur_bank = "-"
    else:
        eur_bank = eur[0][0].strip() + "/" + eur[0][-1].strip()

    if len(rub[0]) == 0:
        rub_bank = "-"
    else:
        rub_bank = rub[0][0].strip() + "/" + rub[0][-1].strip()

    usd_nbu = usd[1][0].strip()
    eur_nbu = eur[1][0].strip()
    rub_nbu = rub[1][0].strip()

    usd_black = usd[2][0].strip() + "/" + usd[2][-1].strip()
    eur_black = eur[2][0].strip() + "/" + eur[2][-1].strip()
    rub_black = rub[2][0].strip() + "/" + rub[2][-1].strip()

    currency_str = constants.currency_title + "\n\n" + constants.usd_title + "\n" + constants.banks_cur + " " + usd_bank + "\n" + constants.nbu_cur + " " + usd_nbu + "\n" + constants.black_cur + " " + usd_black + "\n\n" + constants.eur_title + "\n" + constants.banks_cur + " " + eur_bank + "\n" + constants.nbu_cur + " " + eur_nbu + "\n" + constants.black_cur + " " + eur_black + "\n\n" + constants.rub_title + "\n" + constants.banks_cur + " " + rub_bank + "\n" + constants.nbu_cur + " " + rub_nbu + "\n" + constants.black_cur + " " + rub_black
    return currency_str

def minfin_crypto_currency(url=constants.minfin_crypto_currency_url):
    soup = get_soup(url)
    coin = soup.find(class_="coins--body").findAll(class_="coin", limit=5)
    coin_name = []
    coin_price = []
    coin_changes = []
    for i in coin:
        coin_name.append(i.find(class_="coin-name")["title"])
        coin_price.append(i.find(class_="coin-price")["data-sort-val"])
        coin_changes.append(i.find(class_="coin-changes")["data-sort-val"])

    coin_currency = constants.crypto_currency_title + "\n\n"
    for i in range(5):
        coin_currency += coin_name[i] + " " + coin_price[i] + "USD" + "\n" + constants.coin_changes_title + " " + coin_changes[i] + "%"
        if i !=4:
            coin_currency += "\n\n"
    return coin_currency

# minfin_crypto_currency()
# print(minfin_crypto_currency())

# print(sinoptik_weather(city="чернігів")[0], sinoptik_weather(city="чернігів", n=7)[1])