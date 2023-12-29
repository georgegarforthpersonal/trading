from dataclasses import dataclass
from sqlalchemy import create_engine


@dataclass
class DatabaseConnection:
    username: str
    password: str
    host: str
    port: int
    dbname: str

    def create_engine(self):
        connection_string = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        return create_engine(connection_string)
