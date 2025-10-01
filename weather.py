from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"It's always raining in {location}"

if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Weather server error: {e}")
