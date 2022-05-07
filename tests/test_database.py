import pytest
import os
import peewee

from discord_bot_basics import database
from discord_bot_basics.Database import Database


class WithWrapperDatabase:
    def __call__(self, path):
        self.path = path
        self.db = database.Database(path)
        return self
    def __enter__(self) -> Database:
        if not hasattr(self, 'db'):
            raise Exception('__call__ must be called before __enter__')
        return self.db
    def __exit__(self, *args):
        self.db.close()
        del self.db
        os.remove(self.path)

dbWrapper = WithWrapperDatabase()

def test_createModel():
    with dbWrapper('./test.db') as db:
        table_name = 'test_model'

        db.createModel(table_name, [
            database.TableColumn('name', peewee.CharField(max_length=20)),
            database.TableColumn('age', peewee.IntegerField())
        ])
        tables = db._db.get_tables()
        assert table_name in tables, "test_model should be in the tables"

        columns = map(lambda x: x.name, db._db.get_columns(table_name))
        assert 'name' in columns, "name should be in the columns"
        assert 'age' in columns, "age should be in the columns"


def test_createmodel_and_double_insert_unique_field():
    with dbWrapper('./test.db') as db:
        test_model = db.createModel('test_model', [
            database.TableColumn('name', peewee.CharField(max_length=20)),
            database.TableColumn('age', peewee.IntegerField(unique=True))
        ])
        row_id = test_model.create(name='test name', age=20)
        assert row_id == 1, "Row id should be 1"

        result = test_model.get(test_model.id==1)
        assert result.name == 'test name', "result.name should be the name we set"
        
        with pytest.raises(peewee.IntegrityError):
            test_model.create(name='test name', age=20)

