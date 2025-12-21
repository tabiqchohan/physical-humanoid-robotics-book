"""
OpenAI Agent Integration Example

This example demonstrates how to integrate the RAG Chatbot Backend with OpenAI Agent SDK.
It shows how to call the backend API from an OpenAI agent function.
"""

import openai
import requests
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class KnowledgeBaseSearchTool(BaseModel):
    """
    Pydantic model for the knowledge base search tool.
    """
    query: str = Field(
        ...,
        description="The natural language query to search for in the knowledge base"
    )
    top_k: int = Field(
        default=5,
        description="Number of results to return (default: 5)",
        ge=1,
        le=10
    )


def search_knowledge_base(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Search the knowledge base for information related to the query.
    This function can be registered as a tool with the OpenAI Agent SDK.

    Args:
        query: The natural language query to search for
        top_k: Number of results to return (default: 5)

    Returns:
        Dictionary containing search results
    """
    # In a real implementation, you would call your backend API here
    # For this example, we'll simulate the API call
    backend_url = "https://tabiqchohan-rag-chatbot.hf.space/retrieval/search"

    payload = {
        "query": query,
        "top_k": top_k,
        "similarity_threshold": 0.3
    }

    try:
        # Make request to the RAG backend
        response = requests.post(
            backend_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            return {
                "query": result.get("query", query),
                "results": result.get("results", []),
                "total_results": result.get("total_results", 0),
                "processing_time": result.get("processing_time", 0)
            }
        else:
            return {
                "error": f"API request failed with status {response.status_code}",
                "details": response.text
            }

    except Exception as e:
        return {
            "error": f"Failed to call knowledge base API: {str(e)}"
        }


def register_knowledge_base_tool(agent_client: openai.OpenAI) -> str:
    """
    Register the knowledge base search tool with the OpenAI Agent.

    Args:
        agent_client: OpenAI client instance

    Returns:
        Tool ID for the registered tool
    """
    tool_definition = {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the knowledge base for information related to the user's query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The natural language query to search for in the knowledge base"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["query"]
            }
        }
    }

    # In the actual OpenAI Assistants API, you would register the tool like this:
    # assistant = client.beta.assistants.create(
    #     name="Knowledge Base Assistant",
    #     instructions="You are a helpful assistant that can search a knowledge base for relevant information.",
    #     model="gpt-4-turbo",
    #     tools=[tool_definition]
    # )

    print("Tool registered with definition:")
    print(json.dumps(tool_definition, indent=2))

    # Return a mock tool ID for this example
    return "knowledge_base_search_tool_123"


def example_usage():
    """
    Example usage of the knowledge base integration with OpenAI Agent.
    """
    print("=== OpenAI Agent Integration Example ===\n")

    # Example 1: Direct API call
    print("Example 1: Direct API call to knowledge base")
    query = "What are the benefits of renewable energy?"
    results = search_knowledge_base(query, top_k=3)

    print(f"Query: {query}")
    print(f"Number of results: {results.get('total_results', 0)}")
    if 'results' in results:
        for i, result in enumerate(results['results'][:2], 1):  # Show first 2 results
            print(f"  Result {i}: Score {result.get('score', 0):.2f}")
            print(f"    Content: {result.get('content', '')[:100]}...")
            print(f"    Source: {result.get('source', 'Unknown')}")
    print()

    # Example 2: Tool registration (simulated)
    print("Example 2: Tool registration with OpenAI Agent")
    # In a real implementation, you would use the OpenAI client:
    # client = openai.OpenAI(api_key="your-api-key")
    # tool_id = register_knowledge_base_tool(client)

    print("Simulating tool registration...")
    tool_definition = {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the knowledge base for information related to the user's query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The natural language query to search for in the knowledge base"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["query"]
            }
        }
    }
    print("Tool registered successfully!")
    print(f"Tool definition: {json.dumps(tool_definition, indent=2)}")
    print()

    # Example 3: Simulated agent interaction
    print("Example 3: Simulated agent interaction")
    print("User: 'Can you tell me about renewable energy sources?'")
    print("Agent: 'I'll search our knowledge base for information about renewable energy sources.'")

    # Agent calls the tool
    agent_results = search_knowledge_base("renewable energy sources", top_k=2)
    print(f"Agent: 'I found {agent_results.get(\"total_results\", 0)} relevant documents:'")

    for i, result in enumerate(agent_results.get('results', [])[:2], 1):
        print(f"  - Document {i}: {result.get('content', '')[:150]}...")


if __name__ == "__main__":
    example_usage()