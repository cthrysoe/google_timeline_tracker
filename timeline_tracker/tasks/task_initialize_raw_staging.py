from timeline_tracker.data_ingestion.database_interface import StagingInterface


def initialize_raw_staging_area():
    StagingInterface().initialize_staging_table()


if __name__ == '__main__':
    initialize_raw_staging_area()
