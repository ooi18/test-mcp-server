import asyncio
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

async def main():
    server = Server("SimpleLowLevelServer")

    # Tool 1: "echo"
    ECHO = Tool(
        name="echo",
        description="Always returns a fixed message.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    )

    # Tool 2: "echo_something"
    ECHO_SOMETHING = Tool(
        name="echo_something",
        description="Returns 'Hello <something>' where <something> is your input.",
        inputSchema={
            "type": "object",
            "properties": {
                "something": {
                    "type": "string",
                    "description": "Text to include in the hello message"
                }
            },
            "required": ["something"]
        }
    )

    @server.list_tools()
    async def list_tools():
        # List both tools
        return [ECHO, ECHO_SOMETHING]

    @server.call_tool()
    async def call_tool(name: str, args: dict):
        if name == "echo":
            return [TextContent(type="text", text="Hello from the simple MCP server!")]
        elif name == "echo_something":
            something = args.get("something", "")
            return [TextContent(type="text", text=f"Hello {something}")]
        else:
            raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

if __name__ == "__main__":
    asyncio.run(main())
