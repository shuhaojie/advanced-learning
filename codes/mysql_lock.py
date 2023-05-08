import uuid
import MySQLdb
import threading

conn = MySQLdb.connect(host="127.0.0.1",
                       user="haojie",
                       passwd="haojie",
                       db="dg",
                       port=3306)

cur = conn.cursor()


def create():
    cur.execute("create table job(job_id varchar(50), queue int )")
    conn.commit()


def insert():
    for i in range(1, 5):
        cur.execute("INSERT INTO `job`(`job_id`, `queue`) values(%s, %s)",
                    (str(uuid.uuid1()), i))
        conn.commit()


def update_func():
    cur.execute("UPDATE job SET queue = queue - 1")
    # cur.close()
    # conn.close()


def insert_func():
    conn.begin()
    cur.execute("SELECT max(queue) from job")
    max_queue = cur.fetchone()[0]
    job_id, queue = str(uuid.uuid1()), max_queue + 1
    cur.execute("INSERT INTO job VALUES(%s,%s)", (job_id, queue))
    conn.commit()
    # cur.close()
    # conn.close()


if __name__ == '__main__':
    # create()
    # insert()
    t1 = threading.Thread(target=update_func)
    t2 = threading.Thread(target=insert_func)
    t1.start()
    t2.start()
