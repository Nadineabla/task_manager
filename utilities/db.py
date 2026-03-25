from sqlmodel import Field, Session, SQLModel, create_engine


engine = create_engine("sqlite:///db.sqlite", echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
    
    
def get_session():
    with Session(engine) as session:
        yield session





































# import json

# Read
# def read_db() :
#     with open("database/db.json", "r") as f:
#         data = json.load(f)

#     return data


# Write
# def write_db(data):
    
#     with open("database/db.json", "w") as f:
#      json.dump(data, f)
#     return data