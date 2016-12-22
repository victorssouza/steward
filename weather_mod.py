from gtts import gTTS
import configparser
import logging
from logging.config import fileConfig
import subprocess
import requests
import datetime
import json
import os, sys

class Weather(object):
	# Configuring log and application configuration properties from local file
	def __init__(self):

		app_configuration_path = 'conf/app_config.ini'
		log_configuration_path = 'conf/logging_config.ini'

		if os.path.exists(log_configuration_path) == False:
			print ('[ERROR]: Configuration file not found. Expecting: {}'.format(log_configuration_path))
			sys.exit(1)
		else:
			fileConfig(log_configuration_path)
			self.logger = logging.getLogger()
			self.logger.debug('Setting log configuration')

		if os.path.exists(app_configuration_path) == False:
			self.logger.error('Configuration file not found. Expecting: {}'.format(app_configuration_path))
			sys.exit(1)
		else:
			self.config = configparser.ConfigParser()
			self.config.read(app_configuration_path)

			try:
				self.logger.debug('Setting application configuration')
				self.config.get('weather_api','api_token')
				self.config.get('voice','language')
			except Exception as e:
				self.logger.error('{}'.format(e))
				sys.exit(1)

		return None

	def get_ip_geolocation(self):
		self.logger.debug('Getting external IP address')
		ipyfy_url = 'https://api.ipify.org?format=json'
		ip_response = requests.get(ipyfy_url).json()
		external_ip = ip_response['ip']

		self.logger.debug('Getting geolocation information')
		freegeoip_url = 'https://freegeoip.net/json/'
		geolocation_ip_info = requests.get('https://freegeoip.net/json/{}'.format(external_ip)).json()
		return geolocation_ip_info

	def get_date_time(self):
		self.logger.debug('Parsing current timestamp')
		d_date = datetime.datetime.now()
		format_date = d_date.strftime("%Y-%m-%d")
		format_time = d_date.strftime("%Y-%m-%d %I:%M %p")
		if d_date.strftime("%p") == 'AM':
			format_period = 'AM'
		elif d_date.strftime("%p") == 'PM':
			format_period = 'PM'
		return format_date, format_time, format_period

	def get_weather_data(self, geolocation_ip_info):
		# Getting attributes from configuration.ini
		self.logger.debug('Getting weather information')
		weather_api_token = self.config.get('weather_api','api_token')
		country = geolocation_ip_info['country_name']
		state = geolocation_ip_info['region_name']
		city = geolocation_ip_info['city']

		weather_url='http://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'.format(country, state, weather_api_token)

		weather_json = {
			'city':city,
			'main':'',
			'description':'',
			'temp':'',
			'temp_min':'',
			'temp_max':''
		}

		with requests.Session() as r:
			response = r.get(weather_url)
			if response.status_code == 401:
				self.logger.error("Permission denied. Check your api_token")
				sys.exit(1)
			else:
				response_data = response.json()
				for g in response_data['weather']:
					weather_json['main'] = g['main']
					weather_json['description'] = g['description']
				weather_json['temp'] = str(response_data['main']['temp']).split('.')[0]
				weather_json['temp_min'] = response_data['main']['temp_min']
				weather_json['temp_max'] = response_data['main']['temp_max']

		return weather_json

	def say_weather(self):
		self.logger.debug('Starting voice assistant')
		voice_language = self.config.get('voice','language')

		if voice_language == 'pt-br':
			weather_phrase = 'A temperatura atual na cidade de {} é de {} graus celcius, com temperatura mínima de {} e máxima de {}. \
							'.format(weather_json['city'],weather_json['temp'],weather_json['temp_min'],weather_json['temp_max'])
		else:
			weather_phrase = 'The weather for today in {} city is: {} degrees celcius, with minimum temperature of {} and max of {}. \
							'.format(weather_json['city'],weather_json['temp'],weather_json['temp_min'],weather_json['temp_max'])
		try:
			tts = gTTS(text=weather_phrase,lang=voice_language)
			audio_name = 'weather.mp3'
			tts.save(audio_name)
			return_code = subprocess.call(["mpg123", "-q", audio_name]) # brew install mpg123
			os.remove(audio_name)
			self.logger.debug('Shuting down voice assistant')
			return True
		except Exception as e:
			if e.args[0] == 'Language not supported: {}'.format(voice_language):
				self.logger.error('{}'.format(e))
				sys.exit(1)
			return False

if __name__ == '__main__':
	weather = Weather()
	format_date, format_time, format_period = weather.get_date_time()
	geolocation_ip_info = weather.get_ip_geolocation()
	weather_json = weather.get_weather_data(geolocation_ip_info)
	weather.say_weather()