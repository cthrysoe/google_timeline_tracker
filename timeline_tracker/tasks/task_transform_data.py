from timeline_tracker.data_ingestion.timeline_data_transformer import TimelineDataTransformer
from timeline_tracker.data_ingestion.database_interface import StagingInterface, TimelineDataInterface


def extract_raw_staging_data():
    data = StagingInterface().get_staging_data()

    raw_xml_list = [x[0] for x in data]
    data_list = [x[1] for x in data]
    return raw_xml_list, data_list


def load_to_target(processed_data, dates):
    timeline_interface = TimelineDataInterface()
    timeline_interface.insert_into_timeline_data(processed_data)
    timeline_interface.insert_into_timeline_dates(dates)


def transform_and_load():
    data_transformer = TimelineDataTransformer()
    xml_raw, extracted_dates = extract_raw_staging_data()
    processed_data = data_transformer.transform_timeline_data(xml_raw)
    load_to_target(processed_data, extracted_dates)


if __name__ == '__main__':
    transform_and_load()
