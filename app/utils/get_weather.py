weather_emojis = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧",
    "drizzle": "🌦",
    "thunderstorm": "⛈",
    "snow": "❄️",
    "mist": "🌫",
    "fog": "🌫",
    "haze": "🌁",
    "smoke": "💨",
    "dust": "🏜",
    "sand": "🏖",
    "ash": "🌋",
    "squall": "🌬",
    "tornado": "🌪",
}


def get_weather(data, city):
    weather = data["weather"][0]
    emoji = weather_emojis.get(weather["main"].lower(), "❓")

    text = (
        f"Прогноз погоды в <b>{city.capitalize()}</b>:\n\n"
        f"<blockquote>"
        f"🌡 Температура: <b>{data['main']['temp']}℃</b>\n"
        f"🤔 Ощущается как: <b>{data['main']['feels_like']}℃</b>\n"
        f"{emoji} <b>{weather['description'].capitalize()}</b>\n"
        f"💨 Ветер: <b>{data['wind']['speed']} м/с</b>"
        f"</blockquote>"
    )

    return text
