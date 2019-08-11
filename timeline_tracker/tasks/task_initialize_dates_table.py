from timeline_tracker.data_ingestion.database_interface import TimelineDataInterface


def initialize_dates_table():
    TimelineDataInterface().initialize_timeline_dates()


if __name__ == '__main__':
    initialize_dates_table()
