from timeline_tracker.data_ingestion.database_interface import StagingInterface


def clear_staging():
    StagingInterface().clear_staging_table()


if __name__ == '__main__':
    clear_staging()
