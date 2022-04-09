import mysql.connector as connector


class TodoDB:

    def __init__(self) -> None:
        self._con = connector.connect(user="root", password="Ishu2004*",
                                      host="localhost", port="3306", database="hello")
        self._cursor = self._con.cursor()

    def create_table(self, *, table_name: str) -> None:
        query = f"""CREATE TABLE IF NOT EXISTS `{table_name}`
                ( TaskNo INT(2) NOT NULL,
                TaskName VARCHAR(80) NOT NULL UNIQUE,
                STATUS CHAR(1) NOT NULL DEFAULT 'I',
                PRIMARY KEY (TaskNo));"""

        self._cursor.execute(query)
        self._con.commit()

    def add_task(self, *, table_name: str, task_no: int, task: str, status: str = "I") -> None:
        query = f"INSERT INTO `{table_name}` VALUES (%s, %s, %s);"
        values = (task_no, task, status)
        self._cursor.execute(query, values)
        self._con.commit()

    def update_status(self, *, table_name: str, task_no: int, status: str = "C") -> None:
        query = f"UPDATE `{table_name}` SET STATUS=%s WHERE TaskNo=%s;"
        values = (status, task_no)
        self._cursor.execute(query, values)
        self._con.commit()

    def update_task(self, *, table_name: str, task_no: int, task_name: str) -> None:
        query = f"UPDATE `{table_name}` SET TaskName=%s WHERE TaskNo=%s;"
        values = (task_name, task_no)
        self._cursor.execute(query, values)
        self._con.commit()

    def delete_task(self, *, table_name: str, task_no: int) -> None:
        query = f"DELETE FROM `{table_name}` WHERE TaskNo=%s;"
        self._cursor.execute(query, (task_no,))
        self._con.commit()

    def get_all_tasks(self, *, table_name: str) -> list[tuple[int, str, str]]:
        query = f"SELECT * FROM `{table_name}`;"
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()
        self._con.close()

if __name__ == "__main__":
    db = TodoDB()
    # db.create_table(table_name="2022-apr-11-mon")

    # db.add_task(table_name="2022-apr-11-mon", task_no=1, task="Book Reading")
    # db.add_task(table_name="2022-apr-11-mon", task_no=2, task="Learn Python")
    print(db.get_all_tasks(table_name="2022-apr-11-mon"))

    # db.update_status(table_name="2022-apr-11-mon", task_no=1, status="C")
    print(db.get_all_tasks(table_name="2022-apr-11-mon"))

    # db.update_status(table_name="2022-apr-11-mon", task_no=1, status="I")
    print(db.get_all_tasks(table_name="2022-apr-11-mon"))

    # db.delete_task(table_name="2022-apr-11-mon", task_no=2)
    print(db.get_all_tasks(table_name="2022-apr-11-mon"))

    db.close()
