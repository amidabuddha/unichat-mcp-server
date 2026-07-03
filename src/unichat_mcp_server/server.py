import asyncio
import logging
import os

from mcp import LoggingLevel
import mcp.server.stdio
import mcp.types as types
import unichat
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Set up logging
logger = logging.getLogger("unichat-mcp-server")
logger.setLevel(logging.INFO)

# Initialize the server
server = Server("unichat-mcp-server")

# API configuration
MODEL = os.getenv("UNICHAT_MODEL")
if not MODEL:
    logger.error("UNICHAT_MODEL environment variable not found")
    raise ValueError("UNICHAT_MODEL environment variable required")

UNICHAT_BASE_URL = os.getenv("UNICHAT_BASE_URL") or None
if UNICHAT_BASE_URL:
    logger.info("Using custom OpenAI-compatible base URL for Unichat")
elif not any(MODEL in models_list for models_list in unichat.MODELS_LIST.values()):
    logger.error(f"Invalid model specified: {MODEL}")
    raise ValueError(f"Unsupported model: {MODEL}")

UNICHAT_API_KEY = os.getenv("UNICHAT_API_KEY")
if not UNICHAT_API_KEY:
    logger.error("UNICHAT_API_KEY environment variable not found")
    raise ValueError("UNICHAT_API_KEY environment variable required")

chat_api = unichat.UnifiedChatApi(api_key=UNICHAT_API_KEY, base_url=UNICHAT_BASE_URL)

def validate_messages(messages):
    logger.debug(f"Validating messages: {len(messages)} messages received")
    if len(messages) != 2:
        logger.error(f"Invalid number of messages: {len(messages)}")
        raise ValueError("Exactly two messages are required: one system message and one user message")

    if messages[0]["role"] != "system":
        logger.error("First message has incorrect role")
        raise ValueError("First message must have role 'system'")

    if messages[1]["role"] != "user":
        logger.error("Second message has incorrect role")
        raise ValueError("Second message must have role 'user'")

def format_response(response: str) -> types.TextContent:
    logger.debug("Formatting response")
    try:
        formatted = {"type": "text", "text": response.strip()}
        logger.debug("Response formatted successfully")
        return formatted
    except Exception as e:
        logger.error(f"Error formatting response: {str(e)}")
        return {"type": "text", "text": f"Error formatting response: {str(e)}"}

PROMPTS = {
    "code_review": types.Prompt(
        name="code_review",
        description="Review code for best practices, potential issues, and improvements",
        arguments=[
            types.PromptArgument(
                name="code",
                description="The code to review",
                required=True
            )
        ]
    ),
    "document_code": types.Prompt(
        name="document_code",
        description="Generate documentation for code including docstrings and comments",
        arguments=[
            types.PromptArgument(
                name="code",
                description="The code to document",
                required=True
            )
        ]
    ),
    "explain_code": types.Prompt(
        name="explain_code",
        description="Explain how a piece of code works in detail",
        arguments=[
            types.PromptArgument(
                name="code",
                description="The code to explain",
                required=True
            )
        ]
    ),
    "code_rework": types.Prompt(
        name="code_rework",
        description="Apply requested changes to the provided code",
        arguments=[
            types.PromptArgument(
                name="changes",
                description="The changes to apply",
                required=False
            ),
            types.PromptArgument(
                name="code",
                description="The code to rework",
                required=True
            )
        ]
    )
}
@server.set_logging_level()
async def set_logging_level(level: LoggingLevel) -> types.EmptyResult:
    logger.setLevel(level.upper())
    await server.request_context.session.send_log_message(
        level="info",
        data=f"Log level set to {level}",
        logger="unichat-mcp-server"
    )
    return types.EmptyResult()

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return list(PROMPTS.values())

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    prompt_templates = {
        "code_review": """You are a senior software engineer conducting a thorough code review.
            Review the following code for:
            - Best practices
            - Potential bugs
            - Performance issues
            - Security concerns
            - Code style and readability

            Code to review:
            {code}
            """,
        "document_code": """You are a technical documentation expert.
            Generate comprehensive documentation for the following code.
            Include:
            - Overview
            - Function/class documentation
            - Parameter descriptions
            - Return value descriptions
            - Usage examples

            Code to document:
            {code}
            """,
        "explain_code": """You are a programming instructor explaining code to a beginner level programmer.
            Explain how the following code works:

            {code}

            Break down:
            - Overall purpose
            - Key components
            - How it works step by step
            - Any important concepts used
            """,
        "code_rework": """You are a software architect specializing in code optimization and modernization.
            With a foucs on:
            - Modernizing syntax and approaches
            - Improving structure and organization
            - Enhancing maintainability
            - Optimizing performance
            - Applying current best practices
            Do: {changes}

            Code to transform:
            {code}
            """
    }
    if name not in prompt_templates:
        logger.error(f"Prompt not found: {name}")
        raise ValueError(f"Unknown prompt: {name}")

    if not arguments or "code" not in arguments:
        logger.error("Missing required code argument")
        raise ValueError("Missing required argument: code")

    logger.debug("Formatting prompt template")
    # Format the template with provided arguments
    system_content = prompt_templates[name].format(**arguments)

    try:
        response = chat_api.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": "Please provide your analysis."}
            ],
            stream=False
        )
        response = format_response(response.choices[0].message.content)

        return types.GetPromptResult(
            description=f"Requested code manipulation",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=response,
                )
            ],
        )
    except Exception as e:
        logger.error(f"Error getting prompt completion: {str(e)}")
        raise Exception(f"An error occurred: {e}")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="unichat",
            description="""Chat with an assistant.
                        Example tool use message:
                        Ask the unichat to review and evaluate your proposal.
                        """,
            inputSchema={
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {
                                    "type": "string",
                                    "description": "The role of the message sender. Must be either 'system' or 'user'",
                                    "enum": ["system", "user"]
                                },
                                "content": {
                                    "type": "string",
                                    "description": "The content of the message. For system messages, this should define the context or task. For user messages, this should contain the specific query."
                                },
                            },
                            "required": ["role", "content"],
                        },
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "Array of exactly two messages: first a system message defining the task, then a user message with the specific query"
                    },
                },
                "required": ["messages"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name != "unichat":
        logger.error(f"Unknown tool requested: {name}")
        raise ValueError(f"Unknown tool: {name}")

    try:
        logger.debug("Validating messages")
        validate_messages(arguments.get("messages", []))

        response = chat_api.chat.completions.create(
            model=MODEL,
            messages=arguments["messages"],
            stream=False
        )

        response = format_response(response.choices[0].message.content)

        return [response]
    except Exception as e:
        logger.error(f"Error calling tool: {str(e)}")
        raise Exception(f"An error occurred: {e}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="unichat-mcp-server",
                server_version="0.2.21",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
