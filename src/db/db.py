from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import text


class DbConnection:
    def __init__(self) -> None:
        self.engine: AsyncEngine = None

    async def create_connection(self, db_url: str) -> AsyncEngine:
        """Отвечает за создание подключения к БД

        Args:
            db_url (str): url базы данных

        Returns:
            AsyncEngine: Объект движка БД
        """
        self.engine = create_async_engine(db_url, echo=True)
        return self.engine

    async def run_select_queries(self, query: str) -> Optional[tuple]:
        """Отвечает за обработку SELECT - запросов к БД

        Args:
            query (str): Запрос

        Returns:
            Optional[tuple]: Кортеж в виде имен столбцов и результатов
        """
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(text(query))
                tuple_result = [tuple(row) for row in result]
                headers = result.keys()
                return headers, tuple_result
        except Exception as exc:
            return f"Ошибка: {exc}"

    async def get_other_queries(self, query: str) -> Optional[str]:
        """Отвечает за обработку CREATE, UPDATE, INSERT, DELETE запросов к БД

        Args:
            query (str): Запрос

        Returns:
            Optional[str]: None
        """
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text(query))
                await conn.commit()
                return "Выполнено"
        except Exception as exc:
            return f"Ошибка: {exc}"


