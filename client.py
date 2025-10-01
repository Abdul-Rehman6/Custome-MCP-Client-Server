from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "Math":{
                "command":"python",
                "args":["mathserver.py"], ## correct absolute path
                "transport":"stdio",
            
            },
            "Weather": {
                "command":"python",
                "args":["weather.py"],
                "transport": "stdio",
            }

        }
    )

    tools=await client.get_tools()
    model=ChatOpenAI(model="gpt-4o-mini")
    agent=create_react_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is 3 plus 5and then multilpy with 12?"}]}
    )

    print("\nMath response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in Lahore Pakistan?"}]}
    )
    print("\nWeather response:", weather_response['messages'][-1].content)

asyncio.run(main())
