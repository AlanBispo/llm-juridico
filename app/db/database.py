import aiomysql
from app.core.config import settings

class JuridicoDatabase:
    def __init__(self):
        self.config = {
            'host': settings.DB_HOST,
            'user': 'root',
            'password': settings.MYSQL_ROOT_PASSWORD,
            'db': settings.MYSQL_DATABASE
        }

    async def obter_processo(self, processo_id: int):
        conn = await aiomysql.connect(**self.config)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM processos_judiciais WHERE id = %s", (processo_id,))
                return await cursor.fetchone()
        finally:
            conn.close()