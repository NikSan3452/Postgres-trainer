from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


class DbConnection:
    async def run_select_queries(self, query: str, db_url: str) -> Optional[tuple]:
        """Отвечает за обработку SELECT - запросов к БД

        Args:
            query (str): Запрос
            db_url (str): url базы данных

        Returns:
            Optional[tuple]: Кортеж в виде имен столбцов и результатов
        """
        engine = create_async_engine(db_url, echo=True)
        try:
            async with engine.connect() as conn:
                result = await conn.execute(text(query))
                tuple_result = [tuple(row) for row in result]
                headers = result.keys()
                return headers, tuple_result
        except Exception as exc:
            return f"Ошибка: {exc}"

    async def get_other_queries(self, query: str, db_url: str) -> Optional[str]:
        """Отвечает за обработку CREATE, UPDATE, INSERT, DELETE запросов к БД

        Args:
            query (str): Запрос
            db_url (str): url базы данных

        Returns:
            Optional[None]: None
        """
        engine = create_async_engine(db_url, echo=True)
        try:
            async with engine.connect() as conn:
                await conn.execute(text(query))
                await conn.commit()
                return "Выполнено"
        except Exception as exc:
            return f"Ошибка: {exc}"


db = DbConnection()
