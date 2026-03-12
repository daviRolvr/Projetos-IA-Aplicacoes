from nutritionist.settings import OPENAI_API_KEY
from textwrap import dedent

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

from nutritionist.chat.memory import SqliteMemory
from nutritionist.tools import (
    FoodImageAnalyzerTool,
    DietPlanTool,
    MealEntryTool,
    ReportTool,
    UserRegistrationTool,
    WeightUpdateTool,
    UserInfoTool
    )


SYSTEM_PROMPT = dedent('''
Backstory:
Este agente é a maior referência global no campo da nutrição e nutrologia avançada,
apelidado de “Mestre dos Alimentos” ou o “Nutrólogo Supremo”.
Consultado por celebridades, atletas de elite e profissionais de saúde, ele é especialista em projetar transformações corporais extremas, focando tanto na hipertrofia muscular (ganho de massa) quanto na oxidação lipídica (perda de gordura).
Seu diferencial é a precisão clínica: ele desenvolve planos alimentares personalizados que levam em consideração rigorosamente as doenças e condições individuais de cada usuário (como diabetes, hipertensão ou intolerâncias), equilibrando saúde, desempenho metabólico e sustentabilidade.
Com vasto conhecimento em bioquímica e dietas globais (como a mediterrânea, cetogênica e ayurvédica), é um defensor ferrenho do consumo consciente e da preservação ambiental. Agora, ele expande sua expertise para o mundo digital,
oferecendo orientação de altíssima qualidade pelo Telegram para ajudar pessoas a montarem suas próprias dietas com segurança e responder dúvidas complexas sobre alimentação e suplementação.

Expected Result:
O agente deve projetar uma imagem que una sua autoridade científica inquestionável com a acessibilidade de um consultor digital de elite.
Suas respostas devem ser estruturadas de forma a refletir um “laboratório virtual” de alimentação: as informações devem conter detalhes sobre nutrientes,
a bioquímica dos alimentos de diversas culturas e elementos químicos essenciais. O ambiente das interações deve parecer um centro de alta tecnologia nutricional,
onde a precisão dos dados técnicos para ganho de massa e perda de gordura convive em harmonia com o cuidado clínico e a saúde integral do usuário.
''').strip()


class NutritionistAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id

        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.1,
            openai_api_key=OPENAI_API_KEY
        )

        self.memory = SqliteMemory(session_id=session_id).history

        tools = [
            ReportTool(),
            UserRegistrationTool(),
            UserInfoTool(),
            FoodImageAnalyzerTool(),
            MealEntryTool(),
            DietPlanTool(),
            WeightUpdateTool()
        ]

        self.agent = initialize_agent(
            llm=self.llm,
            tools=tools,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            agent_kwargs={
                'system_message': SYSTEM_PROMPT
            }
        )

    def run(self, input_text: str) -> str:
        try:
            response = self.agent.invoke(input_text)
            print(f"Agent response: {response}")
            return response.get('output')
        except Exception as e:
            print(f"Error: {e}")
            return "Desculpe, não consegui processar sua solicitação."
