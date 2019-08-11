from timeline_tracker.data_ingestion.database_interface import TimelineDataInterface


def initialize_target_table():
    TimelineDataInterface().initialize_timeline_table()


if __name__ == '__main__':
    initialize_target_table()
