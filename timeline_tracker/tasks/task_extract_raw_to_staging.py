from timeline_tracker.data_ingestion.timeline_data_extractor import TimelineDataExtractor
from datetime import datetime, timedelta, date
from timeline_tracker.data_ingestion.database_interface import StagingInterface, TimelineDataInterface


def get_extracted_dates():
    dates = TimelineDataInterface().get_timeline_dates()
    return [x[0] for x in dates]


def extract_data():
    start = date(2019, 4, 1)
    end = date.today() - timedelta(days=1)

    already_processed_dates = get_extracted_dates()

    data_extractor = TimelineDataExtractor(start, end)
    raw_data, parsed_dates = data_extractor.extract_timeline_data(already_processed_dates)

    StagingInterface().insert_into_staging_table(raw_data, parsed_dates)


if __name__ == '__main__':
    extract_data()
