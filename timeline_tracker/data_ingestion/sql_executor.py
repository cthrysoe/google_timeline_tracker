import os
from contextlib import contextmanager


def read_sql_from_file(path):
    with open(path, 'r') as of:
        sql = of.read()
    return sql


class SQLExecutor:
    """SQLExecutor
    Executor base class, should not be used directly, but implemented by child
    classes. Exposes fetchall and fetch_n.
    """

    def __init__(self,
                 server,
                 database,
                 username,
                 port,
                 password=None):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.conn = None
        self.cursor = None

    def fetch_all(self):
        return self._fetch_all()

    def fetch_n(self, n):
        return self._fetch_n(n)

    def execute(self, sql, sql_params={}, adapter_params=()):
        sql = self._format_sql(sql, sql_params)
        self._execute(sql, adapter_params)

    def _format_sql(self, sql, sql_params):
        return sql.format(**sql_params)

    # TODO fetch first n !
    @contextmanager
    def cursor_context(self, n=1000, single_fetch=False):
        """cursor_context
        :param path: Path to sql files.
        :param sql_params: Strings in the sql file of the form:
        {replacement-field}, is replaced. sql_params should be a dictionary,
        mapping replace-field to a string.
        :param adapter_params: Values given to the database adapter. In
        psycopg2, they have the form '%s'
        :param rows_to_fetch: Number of rows fetched
        """
        with self._conection_context() as connection:
            with connection.cursor() as cursor:
                self.connection, self.cursor = connection, cursor
                yield connection, cursor

    @contextmanager
    def _conection_context(self):
        """_conection_context
        Returns a database connection context, because the connections should
        only ever be active, when SQL is executing, to limit the number of
        active connections.
        """
        pass

    # TODO: Must be implemented by subclass
    def _fetch_all(self):
        pass

    # TODO: Must be implemented by subclass
    def _fetch_n(self, n):
        pass

    # TODO: Must be implemented by subclass
    def _execute(self, sql, adapter_params=None):
        pass


class PostgresExecutor(SQLExecutor):
    """PostgresExecutor"""

    def __init__(self, server, database, username, password=None):
        super().__init__(server,
                         database,
                         username,
                         port=5432,
                         password=None)

    @contextmanager
    def _conection_context(self):
        import psycopg2
        connection = psycopg2.connect(host=self.server,
                                      user=self.username,
                                      database=self.database)
        try:
            yield connection
        finally:
            connection.close()

    def _execute(self, sql, adapter_params):
        self.cursor.execute(sql, adapter_params)
        self.connection.commit()

    def _fetch_all(self):
        return self.cursor.fetchall()

    def _fetch_n(self, n):
        return self.cursor.fetchmany(n)

    def create_colmap_from_description(self):
        list_cols = [desc[0] for desc in self.cursor.description]

        out_dict = {}

        for i in range(len(list_cols)):
            out_dict[list_cols[i]] = i

        return out_dict
