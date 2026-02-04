import os
from dotenv import load_dotenv

# Carica backend/.env durante lo sviluppo (se presente)
here = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(here, ".env"))

DB_ENGINE = os.getenv("DB_ENGINE", "mysql")

if DB_ENGINE == "mysql":
    import mysql.connector

    def get_connection():
        host = os.getenv("DB_HOST")
        port = int(os.getenv("DB_PORT", "3306"))
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")
        ssl_ca = os.getenv("DB_SSL_CA")  # optional path to CA bundle (Aiven)

        # Require minimal config
        if not (host and user and password and database):
            raise RuntimeError("Database credentials not fully configured. Set DB_HOST, DB_USER, DB_PASSWORD, DB_NAME.")

        connect_kwargs = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }

        if ssl_ca:
            connect_kwargs["ssl_ca"] = ssl_ca

        return mysql.connector.connect(**connect_kwargs)
else:
    import sqlite3
    def get_connection():
        """Return a sqlite3 connection-like wrapper where cursor(dictionary=True)
        returns a cursor whose fetchone/fetchall return dicts (to mimic mysql.connector behavior).

        Use DB_NAME from .env as path to sqlite file (relative to backend/).
        """
        db_name = os.getenv("DB_NAME", "dev.db")
        db_path = db_name if os.path.isabs(db_name) else os.path.join(here, db_name)
        raw_conn = sqlite3.connect(db_path, check_same_thread=False)
        raw_conn.row_factory = sqlite3.Row

        class DictCursor:
            def __init__(self, cur):
                self._cur = cur

            def execute(self, *args, **kwargs):
                # Support MySQL-style %s placeholders by converting them to SQLite ?
                if len(args) >= 1 and isinstance(args[0], str):
                    q = args[0]
                    params = args[1] if len(args) > 1 else None
                    if "%s" in q and params is not None:
                        q2 = q.replace('%s', '?')
                        return self._cur.execute(q2, params)
                return self._cur.execute(*args, **kwargs)

            def executemany(self, *args, **kwargs):
                if len(args) >= 1 and isinstance(args[0], str):
                    q = args[0]
                    params = args[1] if len(args) > 1 else None
                    if "%s" in q and params is not None:
                        q2 = q.replace('%s', '?')
                        return self._cur.executemany(q2, params)
                return self._cur.executemany(*args, **kwargs)

            def fetchone(self):
                row = self._cur.fetchone()
                return dict(row) if row is not None else None

            def fetchall(self):
                rows = self._cur.fetchall()
                return [dict(r) for r in rows]

            @property
            def lastrowid(self):
                return self._cur.lastrowid

            def close(self):
                return self._cur.close()

            def __iter__(self):
                for r in self._cur:
                    yield dict(r)

        class ConnWrapper:
            def __init__(self, conn):
                self._conn = conn

            def cursor(self, dictionary=False):
                cur = self._conn.cursor()
                if dictionary:
                    return DictCursor(cur)
                return cur

            def commit(self):
                return self._conn.commit()

            def close(self):
                return self._conn.close()

            @property
            def row_factory(self):
                return self._conn.row_factory

        return ConnWrapper(raw_conn)
