import requests

BASE_CURRENCY = "RUB"


def get_rates():
    url = f"https://open.er-api.com/v6/latest/{BASE_CURRENCY}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Ошибка при запросе:", response.status_code)
        return None

    data = response.json()

    if data["result"] != "success":
        print("Ошибка API")
        return None

    return data["rates"]


def show_all_rates(rates):
    print(f"\nКурсы валют относительно {BASE_CURRENCY}:\n")
    print("-" * 25)
    print(f"{'Валюта':<10} | {'Курс':>10}")
    print("-" * 25)

    for currency in sorted(rates):
        print(f"{currency:<10} | {rates[currency]:>10.4f}")

    print("-" * 25)


def search_currency(rates):
    currency = input("Введите код валюты для поиска, например RUB: ").upper()

    if currency in rates:
        print(f"\n1 {BASE_CURRENCY} = {rates[currency]:.4f} {currency}")
    else:
        print("Такая валюта не найдена")


def convert_currency(rates):
    from_currency = input("Из какой валюты: ").upper()
    to_currency = input("В какую валюту: ").upper()

    try:
        amount = float(input("Введите сумму: "))
    except ValueError:
        print("Ошибка: нужно ввести число")
        return

    if from_currency not in rates and from_currency != BASE_CURRENCY:
        print("Исходная валюта не найдена")
        return

    if to_currency not in rates and to_currency != BASE_CURRENCY:
        print("Целевая валюта не найдена")
        return

    if from_currency == BASE_CURRENCY:
        result = amount * rates[to_currency]
    elif to_currency == BASE_CURRENCY:
        result = amount / rates[from_currency]
    else:
        amount_in_usd = amount / rates[from_currency]
        result = amount_in_usd * rates[to_currency]

    print(f"\n{amount} {from_currency} = {result:.2f} {to_currency}")


rates = get_rates()

if rates is not None:
    while True:
        print("\n=== Конвертер валют ===")
        print("1 - Показать все курсы")
        print("2 - Найти валюту")
        print("3 - Конвертировать валюту")
        print("0 - Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_all_rates(rates)

        elif choice == "2":
            search_currency(rates)

        elif choice == "3":
            convert_currency(rates)

        elif choice == "0":
            print("Программа завершена")
            break

        else:
            print("Неверный выбор")