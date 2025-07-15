import asyncio
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

async def main():
    server = Server("SimpleLowLevelServer")

    ECHO = Tool(
        name="echo",
        description="Echo a text message",
        inputSchema={
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"]
        }
    )

    @server.list_tools()
    async def list_tools():
        return [ECHO]

    @server.call_tool()
    async def call_tool(name: str, args: dict):
        if name != "echo":
            raise ValueError(f"Unknown tool: {name}")
        return [TextContent(type="text", text="Hello from the simple MCP server!")]

    # Proper stdio server usage as per the official repo
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

if __name__ == "__main__":
    asyncio.run(main())
