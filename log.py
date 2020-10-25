import json
import os.path
import time
import traceback
import bme680
from time import sleep

import requests


class Log:

    def __init__(self):
        self._LOG_FOLDER_PATH = "logs"
        self._BAD_LOG_ENTRY_TEXT = "bad log entry"
        self._DAY_STAMP_FORMAT = "%Y-%m-%d"
        self._TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
        self._NO_CONNECTION_ERROR = "Name or service not known"

        self._external_cache = []

    def _write_to_log(self, file, txt_to_log):
        with open(file, "a+") as f:
            f.write(txt_to_log)

    def _get_log_path(self, name):
        filename = self._LOG_FOLDER_PATH + "/" + name
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return filename

    def _get_log_name(self):
        return self._get_day_timestamp()

    def _get_day_timestamp(self):
        return time.strftime(self._DAY_STAMP_FORMAT)

    def _get_timestamp(self):
        return time.strftime(self._TIME_STAMP_FORMAT)

    def _make_log_entry(self):
        error_vals = json.dumps({
            "temperature": 0,
            "pressure": 0,
            "humidity": 0,
            "gas_index": 0,
            "meas_index": 0,
            "heat_stable": False
        })
        try:
            # https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-bme680-breakout
            sensor = bme680.BME680()

            sensor.set_humidity_oversample(bme680.OS_2X)
            sensor.set_pressure_oversample(bme680.OS_4X)
            sensor.set_temperature_oversample(bme680.OS_8X)
            sensor.set_filter(bme680.FILTER_SIZE_3)

            sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
            sensor.set_gas_heater_temperature(320)
            sensor.set_gas_heater_duration(150)
            sensor.select_gas_heater_profile(0)

            if sensor.get_sensor_data():
                return json.dumps({
                    "temperature": sensor.data.temperature,
                    "pressure": sensor.data.pressure,
                    "humidity": sensor.data.humidity,
                    "gas_index": sensor.data.gas_index,
                    "meas_index": sensor.data.meas_index,
                    "heat_stable": sensor.data.heat_stable
                })
            else:
                return error_vals

        except Exception as e:
            print("Exception: {}".format(e))
            print(traceback.format_exc())

        return error_vals

    def log(self, entry_delimiter="\n", dms=None, auth=None):
        if not dms:
            self._log_local(entry_delimiter)
        else:
            self._log_post(dms, auth=auth)

    def _log_local(self, entry_delimiter):
        text = self._make_log_entry() + entry_delimiter
        file_name = self._get_log_name()
        file = self._get_log_path(file_name)
        self._write_to_log(file, text)

    def _log_post(self, url, auth=None):
        try:
            self._external_cache.append((time.time(), self._make_log_entry()))
            while self._external_cache:
                created, text = self._external_cache[0]
                resp = requests.post(
                    "{}/app/{}".format(url, "home_temperature"),
                    params={'created': created},
                    headers={'Content-type': 'application/json'},
                    data=text,
                    auth=auth
                )
                if resp.status_code is 200:
                    self._external_cache.pop(0)
                else:
                    raise Exception()
        except:
            sleep(2)
