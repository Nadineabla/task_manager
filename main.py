from fastapi import FastAPI, HTTPException, Depends, Request
from sqlmodel import Session
from fastapi.responses import JSONResponse
from schema import TODOS, TODOUpdate, TODOCreate, StatusUrlChoices
from contextlib import asynccontextmanager
from utilities.db import init_db, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    


app = FastAPI(lifespan=lifespan) 

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},  # This renames 'detail' to 'message'
    )

@app.get("/")
async def root():
    return {"status": 200, "message": "Welcome to the Task Management API!"}


    
@app.post("/add")
async def add_task(task:TODOCreate, session: Session=Depends(get_session)):
    todo = TODOS(name=task.name, status="to-do")
    session.add(todo)
    
    
    session.commit()
    session.refresh(todo)
    return {"status": 200, "message": f"Task '{todo.name}' added successfully!"}

@app.get("/task/{task_id}")
async def get_task(task_id: int, session: Session =Depends(get_session)):
    todo = session.get(TODOS, task_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found.")
    return {"status": 200, "task": todo}



@app.put("/update/{task_id}")
async def update_task(task_id: int, new_task: TODOUpdate, session: Session=Depends(get_session)):
    todo = session.get(TODOS, task_id)
    if todo is None:
        raise HTTPException(status_code=404, detail =f"Task with id {task_id} not found.")
    todo.name = new_task.name
    todo.status = new_task.status
    session.commit()
    session.refresh(todo)
    return {"status": 200, "message": f"Task with id {task_id} updated successfully!"}
    
    
@app.delete("/delete/{task_id}")
async def delete_task(task_id: int, session: Session=Depends(get_session)):
    todo = session.get(TODOS, task_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found.")
    session.delete(todo)
    session.commit()
    return {"status": 200, "message": f"Task with id {task_id} deleted successfully!"}

    
    
@app.get("/all_tasks")
async def list_tasks(status: StatusUrlChoices | None = None, session: Session=Depends(get_session)):
    todo = session.query(TODOS).all()
    if todo is None:
        return {"status": 200, "message": "you have no tasks yet!"}
    if status:
        filtered_tasks = [task for task in todo if task.status.lower() == status.value]
        return {"status": 200, "tasks": filtered_tasks}
    return {"status": 200, "tasks": todo}


@app.delete("/delete")
async def delete_all_task(session: Session=Depends(get_session)):
    todos = session.query(TODOS).all()
    for todo in todos:
        session.delete(todo)
    session.commit()
    return {"status": 200, "message": "All tasks deleted successfully!"}
