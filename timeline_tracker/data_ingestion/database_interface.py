from timeline_tracker.data_ingestion.sql_executor import PostgresExecutor, read_sql_from_file
import os


class StagingInterface:
    def __init__(self):
        self.pg = PostgresExecutor(server="localhost",
                                   database="timeline",
                                   username="postgres")

        dir = os.path.dirname(__file__)
        self.sql_dir = os.path.join(dir, '../sql/')

    def initialize_staging_table(self):
        q = read_sql_from_file(self.sql_dir + 'staging/initialize_staging.sql')
        with self.pg.cursor_context():
            self.pg.execute(q)

    def insert_into_staging_table(self, xml_data, dates):
        q = read_sql_from_file(self.sql_dir + 'staging/insert_staging.sql')
        with self.pg.cursor_context():
            for i in range(len(xml_data)):
                self.pg.execute(q, adapter_params=(xml_data[i], dates[i]))

    def clear_staging_table(self):
        q = read_sql_from_file(self.sql_dir + 'staging/clear_staging.sql')
        with self.pg.cursor_context():
            self.pg.execute(q)

    def get_staging_data(self):
        q = read_sql_from_file(self.sql_dir + 'staging/get_staging_data.sql')
        with self.pg.cursor_context():
            self.pg.execute(q)
            data = self.pg.fetch_all()
        return data


class TimelineDataInterface:
    def __init__(self):
        self.pg = PostgresExecutor(server="localhost",
                                   database="timeline",
                                   username="postgres")

        dir = os.path.dirname(__file__)
        self.sql_dir = os.path.join(dir, '../sql/')

    def initialize_timeline_table(self):
        q = read_sql_from_file(self.sql_dir + 'timeline/initialize_timeline_data.sql')
        with self.pg.cursor_context():
            self.pg.execute(q)

    def initialize_timeline_dates(self):
        q = read_sql_from_file(self.sql_dir + 'timeline/initialize_timeline_data.sql')
        with self.pg.cursor_context():
            self.pg.execute(q)

    def insert_into_timeline_data(self, transformed_data):
        q = read_sql_from_file(self.sql_dir + 'timeline/insert_timeline_data.sql')
        with self.pg.cursor_context():
            for i in range(len(transformed_data)):
                self.pg.execute(q, adapter_params=(transformed_data[i]['name'],
                                                   transformed_data[i]['address'],
                                                   transformed_data[i]['description'],
                                                   transformed_data[i]['coordinates'],
                                                   transformed_data[i]['category'],
                                                   transformed_data[i]['distance'],
                                                   transformed_data[i]['time_begin'],
                                                   transformed_data[i]['time_end']))

    def insert_into_timeline_dates(self, dates):
        q = read_sql_from_file(self.sql_dir + 'timeline/insert_timeline_dates.sql')

        with self.pg.cursor_context():
            for i in range(len(dates)):
                self.pg.execute(q, adapter_params=([dates[i]]))

    def get_timeline_dates(self):
        q = read_sql_from_file(self.sql_dir + 'timeline/get_timeline_dates.sql')
        with self.pg.cursor_context():
            self.pg.execute(q)
            dates = self.pg.fetch_all()
        return dates
