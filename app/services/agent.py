from app.tools.hxm import HXM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_qdrant import Qdrant
from datetime import datetime
from app.services.azure_services import AzureServices
from app.services.qdrant_service import QdrantService

class CustomAgent:
    def __init__(self):
        azure_service = AzureServices()
        self.llm = azure_service.define_llm()
        self.embedding = azure_service.define_embedding()
        self.client = QdrantService().qdrant_client

    def agent_exec(self, user_input, collection):
        today = datetime.utcnow().strftime('%Y-%m-%d')
        current_time = datetime.utcnow().strftime('%H:%M:%S')

        context = ""
        try:
            qdrant = Qdrant(self.client, collection, self.embedding)
            search_results = qdrant.similarity_search(query=user_input, k=10)
            
            if search_results:
                context = "\n\n".join(f"{i}\n{res.page_content}" for i, res in enumerate(search_results))
            else:
                context = "No relevant information found."
        except Exception as e:
            print(f"Error during similarity search: {e}")
            context = "There was an error processing your request."
        
        print(context)
        prompt = ChatPromptTemplate.from_messages([
            ('system', f'''Today is {today} and the current time is {current_time}.
                           Information obtained from searches in RAG is provided here and may help answer the user's question: {context}.
                           Consume Tools answers if it makes sense with the user's question.
                           The user must be answered with the one that has the greatest correlation with their question.
                           When possible, try to combine the information provided from the additional context with the results from the tools prioritizing the specific information returned from the tool, however, only do this if it makes sense.
                        '''), 
            MessagesPlaceholder(variable_name='char_history', optional=True),
            ('user', user_input), 
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        tools = [HXM()]
        agent_executor = AgentExecutor(agent=create_openai_tools_agent(llm=self.llm, tools=tools, prompt=prompt),
                                       tools=tools, verbose=True)
        self.agent_executor = agent_executor
        
        response = self.agent_executor.invoke(input={"input": user_input})
        
        return response.get('output', "No output received.")