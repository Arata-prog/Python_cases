import requests
import bs4

# функция для определения смайлика по текст погоды, возвращает его
def getSmile(description):
    if "без осадков" in description:
        if "пасмурно" in description:
            return "☁️"
        if "облачно" in description:
            return "⛅"
        elif "ясно" in description:
            return "☀️"
    elif "дождь" in description:
        return "🌧️"
    return ""

# получение погоды на текущую дату (изначально для Москвы)
def getWeather(url="https://pogoda7.ru/prognoz/gorod134242-Russia-g_Moskva-Moskva"):
    try:
        # для ответа
        result = ""
        # выполняем запрос, получаем ответ в response
        response = requests.get(url)
        print("Выполняется запрос... Ожидайте...")

        # если результат успешный (статусный код == 200)
        if response.status_code == 200:
            # получаем весь контент
            content = bs4.BeautifulSoup(response.text, "lxml")
            # "парсим" название города как последний элемент li (-1) в элементе div с классом breadcrumb
            city = content.find("div", class_="breadcrumb").find_all("li")[-1]
            result += f"ПОГОДА В {city.text}\n\n"

            # получаем данные о текущем дне
            currentData = content.find("div", class_="current_data").find("div", class_="precip").find_all("div")

            # текущая температура
            currentTemperature = currentData[0].text

            # собираем данные об осадках (для этого берём все div, кроме первого и последнего)
            weatherType = ""
            for i in range(1, len(currentData)-1):
                weatherType += currentData[i].text.strip() + " "
            weatherType = getSmile(weatherType) + " " + weatherType

            result += f"СЕГОДНЯ:\n{currentTemperature}\n{weatherType}\n"

            # другие дни
            # берём все блоки div с классом dayline, начиная с 1
            days = content.find_all("div", class_="dayline")[1:]

            # для дня day в следующих днях days
            for day in days:
                # получаем дату
                date = day.find("div", class_="dayweek").text.strip().split("\n")[0].upper()
                result += f"\n{date}\n"

                # получаем все части дня day
                mainBlock = day.find_all("div", class_="table-row-time")

                # для всех частей дня (их будет по 4)
                for i in range(len(mainBlock)):
                    allData = mainBlock[i].find_all("div")
                    # часть дня
                    dayPartParts = allData[0].find_all("div")
                    dayPart = dayPartParts[0].text + " " + dayPartParts[1].text
                    # температура
                    temperature = allData[3].text
                    # осадки
                    weatherType = getSmile(allData[6].text) + " " + allData[6].text
                    result += dayPart + ": " + temperature + "\n" + weatherType + "\n"

            print(result)

        else:
            print(f"Произошла ошибка при получении запроса: код {response.status_code}")

    except Exception as ex:
        print(f"Произошла ошибка при получении запроса: {ex}")


getWeather()

