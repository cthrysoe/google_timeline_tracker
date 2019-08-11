from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz


class TimelineDataTransformer:

    def transform_timeline_data(self, timeline_data_list):
        parsed_days_list = []
        for timeline_data in timeline_data_list:
            parsed_day_list = self.__parse_single_day(timeline_data)
            for parsed_day in parsed_day_list:
                parsed_days_list.append(parsed_day)
        return parsed_days_list

    def __parse_single_day(self, timeline_xml_string):
        placemark_list = []

        timeline_bs_string = BeautifulSoup(timeline_xml_string, 'xml')
        for place in timeline_bs_string.find_all('Placemark'):
            name = self.__extract_name(place)
            address = self.__extract_address(place)
            description = self.__extract_description(place)
            coordinates = self.__extract_coordinates(place)
            time_begin, time_end = self.__extract_time(place)
            category, distance = self.__extract_extended_data(place)

            row_dict = dict(
                name=name,
                address=address,
                description=description,
                coordinates=coordinates,
                category=category,
                distance=distance,
                time_begin=time_begin,
                time_end=time_end
            )

            placemark_list.append(row_dict)
        return placemark_list

    def __extract_description(self, place):
        description = place.find('description').text.strip()
        return description

    def __extract_address(self, place):
        address = place.find('address').text
        return address

    def __extract_name(self, place):
        name = place.find('name').text
        return name

    def __extract_extended_data(self, place):
        extended_data_tags = place.find('ExtendedData').find_all('Data')
        category = extended_data_tags[1].text
        distance = extended_data_tags[2].text
        return category, distance

    def __extract_time(self, place):
        time = place.find('TimeSpan')
        time_begin = self.__convert_timezone(time.find('begin').text)
        time_end = self.__convert_timezone(time.find('end').text)
        return time_begin, time_end

    def __extract_coordinates(self, place):
        if place.find('LineString') is not None:
            coordinates = place.find('LineString').find('coordinates').text
        elif place.find('Point') is not None:
            coordinates = place.find('Point').find('coordinates').text
        else:
            coordinates = None
        return coordinates

    def __convert_timezone(self, date_time):
        """
        Convert datetimes from UTC to localtime zone
        """
        utc_datetime = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        utc_datetime = utc_datetime.replace(tzinfo=tz.tzutc())
        local_datetime = utc_datetime.astimezone(tz.tzlocal())
        return local_datetime.strftime("%Y-%m-%d %H:%M:%S")
