import psycopg2
# import configuration.config as cfg
import time
import json


# config = cfg.Config()

# ENDPOINT=config.get_postgres_host()
# PORT=config.get_postgres_host()
# USER=config.get_postgres_user()
# PASSWORD=config.get_postgres_password()
# DBNAME=config.get_postgres_database()

ENDPOINT = "database-ds.cekjcsqlwwiv.ap-northeast-1.rds.amazonaws.com"
PORT = "5432"
USER = "postgres"
PASSWORD = "postgres"
DBNAME = "jobs_2023"


def load_job(conn, cur):

    with open('./data/job_vlt_2022.json') as file:
        # change json.load(file) to file.read()
        data = file.read()

    # cur.execute("truncate table JOB")

    query_sql = """
                insert into JOB select * from
                json_populate_recordset(NULL::JOB, %s) on conflict do nothing;
                """

    cur.execute(query_sql, (data,))
    cur.execute("select count(*) from JOB")
    print(cur.fetchall())


def load_company(conn, cur):

    with open('./data/company_vlt_2022.json') as file:
        # change json.load(file) to file.read()
        data = file.read()
    # cur.execute("truncate table COMPANY")

    query_sql = """
                insert into COMPANY select * from
                json_populate_recordset(NULL::COMPANY, %s) on conflict do nothing;
                """

    cur.execute(query_sql, (data,))
    cur.execute("select count(*) from COMPANY")
    print(cur.fetchall())


conn = None
cur = None

try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD)
    conn.autocommit = True
    cur = conn.cursor()

    # cur.execute("delete from COMPANY where id not in (select company_id from JOB) ")
    # print(cur.fetchall())

    # cur.execute("alter table JOB add updated_time1 timestamp")
    # cur.execute("update JOB set updated_time1 = to_timestamp(updated_time, 'DD/MM/YYYY HH24:MI:SS')")
    # cur.execute("alter table JOB drop column updated_time")
    # cur.execute("alter table JOB rename column updated_time1 to updated_time")
    # load_company(conn, cur)
    # load_job(conn, cur)

except Exception as e:
    print("Database connection failed due to {}".format(e))