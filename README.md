# weather-wise

A Python desktop application that retrieves city forecasts from OpenWeather's `/data/2.5/forecast` endpoint and displays temperature, humidity, and forecast time in a themed Tkinter interface. Requests use metric units; all timestamps are converted from UTC to Indian Standard Time (`Asia/Kolkata`), regardless of the selected city's location.

## Architecture

```text
City input → HTTPS request → forecast JSON → UTC-to-IST conversion → text display
```

`weather_wise/weather_forecast.py` contains the interface, request handler, and time conversion. Tkinter supplies the widgets, `ttkthemes` applies the `elegance` theme, `requests` handles HTTP, and `pytz` performs timezone conversion. The display iterates through the API's returned forecast entries; it does not aggregate daily summaries.

## Setup

Use Python 3 with a working Tkinter installation and a desktop display. No database or backend service is required.

```bash
git clone https://github.com/quixoticalcoder/weather-wise.git
cd weather-wise
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`. Tkinter is supplied by the Python installation or operating system, rather than `requirements.txt`. Run `python -m tkinter` to check that it can open a window. Dependencies are unpinned.

Set an OpenWeather API key with access to the forecast endpoint before launching:

```bash
export OPENWEATHER_API_KEY="your-api-key"
python weather_wise/weather_forecast.py
```

For PowerShell:

```powershell
$env:OPENWEATHER_API_KEY = "your-api-key"
python weather_wise/weather_forecast.py
```

The application reads the environment variable at startup; it does not load `.env` files automatically. Enter a city and click **Fetch Weather**. Each returned entry shows its IST timestamp, temperature in degrees Celsius, and relative humidity percentage. A successful response replaces the previous forecast.

## Error handling and limits

- Blank city input and a missing API key produce a dialog before any request is sent.
- Requests use a 15-second timeout. Connection and timeout failures produce a dialog; non-200 responses display the API's status and response text.
- Networking runs synchronously on Tkinter's UI thread, so the window can become unresponsive while a request is pending. There are no retries, background workers, or response caching.
- The parser expects `list`, `dt_txt`, `main.temp`, and `main.humidity` in a successful response. Malformed JSON or unexpected schemas are not handled explicitly.
- All displayed times are IST. API availability, account access, and usage limits depend on the configured OpenWeather account.

No license file is provided in this repository.
