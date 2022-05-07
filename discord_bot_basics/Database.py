from typing import List
import peewee
from dataclasses import dataclass


@dataclass
class TableColumn:
    name: str
    type: peewee.Field


class Database:
    def __init__(self, dbFilePath: str):
        self.dbFilePath = dbFilePath
        self._db = peewee.SqliteDatabase(self.dbFilePath)
        self.BaseModel = self._createBaseModel()
        self._models = []

    def close(self):
        self._db.close()

    def _createBaseModel(self):
        return type(
            "BaseModel",
            (peewee.Model,),
            {
                'Meta': type('Meta', (), {'database': self._db})
            }
        )

    def _addModel(self, model):
        self._models.append(model)
        self._db.create_tables([model])

    def createModel(self, modelName: str, tableColumns: List[TableColumn]):
        model = type(
            modelName,
            (self.BaseModel,),
            {**{tableColumn.name: tableColumn.type for tableColumn in tableColumns}}
        )
        self._addModel(model)
        return model


if __name__ == "__main__":
    db = Database('./test.db')
    model = db.createModel('test', [
        TableColumn('name', peewee.CharField(max_length=20)),
        TableColumn('age', peewee.IntegerField())
    ])
