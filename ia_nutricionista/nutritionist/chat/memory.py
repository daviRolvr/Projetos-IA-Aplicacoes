from langchain_classic.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory

#Guarda o histórico de mensagens do chat em um banco de dados SQLite usando SQLChatMessageHistory. 
#O ConversationBufferMemory é usado para armazenar as mensagens em memória e retornar as mensagens quando necessário. 
#O MEMORY_KEY é a chave usada para acessar o histórico de mensagens no ConversationBufferMemory.

MEMORY_KEY = 'chat_history'


class SqliteMemory(SQLChatMessageHistory):
    def __init__(self, session_id: str, db_path: str = "sqlite:///memory.db"):
        super().__init__(
            session_id=session_id, connection=db_path
        )

        self.history = ConversationBufferMemory(
            memory_key=MEMORY_KEY,
            chat_memory=self,
            return_messages=True
        ) 
