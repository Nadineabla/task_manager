# from .db import read_db, write_db


# def execute(action, mode = "read"):
#     if mode != "write" and mode != "read" :
#         print("wrong mode")
#         return False
#     if mode == "read" :
#         tasks = read_db()
#         return action(tasks)
#     else:
#         tasks = read_db()
#         updated_tasks = action(tasks)
#         return write_db(updated_tasks)