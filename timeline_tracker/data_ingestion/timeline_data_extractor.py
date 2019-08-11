from timeline_tracker.data_ingestion.google_request_builder import GoogleRequestBuilder
import requests
from datetime import timedelta
import time
import random
import os


class TimelineDataExtractor:
    def __init__(self, start_date, end_date):
        self.google_cookie = self.__get_cookie()
        self.request_builder = GoogleRequestBuilder()
        self.start_date = start_date
        self.end_date = end_date

    def extract_timeline_data(self, processed_dates):
        """
        retrieve raw timeline data between two dates
        :return: list of raw timeline data
        """
        interval_dates = self.__get_interval_dates(self.start_date, self.end_date, processed_dates)
        xml_files = []
        for interval_date in interval_dates:
            xml_files.append(self.__load_single_day(interval_date))
        return xml_files, interval_dates

    def __get_interval_dates(self, start_date, end_date, processed_dates):
        """
        get all dates between a start_date and end_date
        :return: list of dates in the interval
        """
        date_list = []

        for x in range((end_date - start_date).days + 1):
            date = start_date + timedelta(days=x)
            if date not in processed_dates:
                date_list.append(date)

        return date_list

    def __get_cookie(self):
        """
        retrieve google timeline cookie from the specified cookie folder
        :return: dictionary, specifying the cookie
        """
        dir = os.path.dirname(__file__)
        file_dir = os.path.join(dir, '../utils/.google_maps_cookie')
        cookie_content = open(file_dir, 'r').read()
        return dict(cookie=cookie_content)

    def __load_single_day(self, single_day):
        """
        retrieve raw google timeline data for a single date
        :return: raw data
        """
        time.sleep(random.uniform(5, 20))
        request = self.request_builder.build_google_request(single_day.day, single_day.month - 1, single_day.year)
        reply = requests.get(request, cookies=self.google_cookie)
        if reply.status_code == 200:
            return reply.text
        else:
            raise ConnectionError('Could not extract timeline data')
