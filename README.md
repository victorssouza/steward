# Mr. Steward
A python voice assistant (under development) for several minor tasks

## Features

- Weather forecasting
  - Mr. Steward will handle the boring stuff for you, it will say the weather based on your geolocation  ;) 

## Requirements

- Python 3.5 +

- Tested on: 
  - Ubuntu 14.02 +
  - Mac OS Leopard +

- `mpg123` for audio processing (https://www.mpg123.de/)
  - For Mac OS users: `brew install mpg123`
  - For Ubuntu users: `apt-get install mpg123`   

## Hacking

To hack this app, just:
- `pip3 install -r requirements.txt`
- (install mpg123 audio player)

If you want to run locally, just:
- `python3 weather_mod.py`

Otherwise, if you want to install it as a pypi package just:
- `pip3 install .`

In this case, you have to set manually the path for the configuration files:
- `export WEATHER_LOG_CONFIG='SOME/PATH/FILE.ini'`
- `export WEATHER_APP_CONFIG='SOME/PATH/FILE.ini'`

## Additional configuration

- If needed, you can set the log levels to DEBUG in `conf/logging_config.ini`
- You will be using a mocked api_token to get the data from openweathermap.org, so changing to your own should be a good practice. It can be done changing `conf/app_config.ini`
- Try using a different language, for example: pt-br

## Next Steps
- Support for raspberry pi 2+
- Support under docker containers
- Mr. Steward will handle the news
- Voice interactive menu instead of `python3 module.py`