from typing import List, Dict, Any, Optional
import instructor
from pydantic import BaseModel
import ollama
from ollama import AsyncClient
import json
import logging
import re
import asyncio
from pathlib import Path
from functools import partial
from app.tools.search_web_ddg import search_web_ddg
from app.tools.search_web_serp import search_web_serp
from app.tools.get_page_content import get_page_content
from app.tools.extract_vocabulary import extract_vocabulary
from app.tools.generate_song_id import generate_song_id
from app.tools.save_results import save_results

# Configure logging
logger = logging.getLogger('song_vocab')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

class Action(BaseModel):
    """Model for LLM actions."""
    tool: str
    tool_input: Dict[str, Any]
    thought: str

class AgentResponse(BaseModel):
    """Model for LLM responses."""
    thought: str
    action: Optional[Action] = None
    final_answer: Optional[Dict[str, Any]] = None

class ToolRegistry:
    """Registry for managing available tools."""
    def __init__(self):
        self.tools = {
            'search_web_serp': search_web_serp,
            'search_web_ddg': search_web_ddg,
            'get_page_content': get_page_content,
            'extract_vocabulary': extract_vocabulary,
            'generate_song_id': generate_song_id,
            'save_results': save_results
        }
    
    def get_tool(self, name: str):
        """Get a tool by name."""
        return self.tools.get(name)

class SongLyricsAgent:
    def __init__(self, stream_llm: bool = True):
        """Initialize the Song Lyrics Agent.
        
        Args:
            stream_llm: Whether to stream LLM responses
        """
        logger.info("Initializing SongLyricsAgent")
        self.base_path = Path(__file__).parent
        self.prompt_path = self.base_path / "prompts" / "Lyrics-Agent.md"
        self.stream_llm = stream_llm
        
        # Initialize Ollama client
        logger.info("Initializing Ollama client and tool registry")
        try:
            self.client = AsyncClient(host='http://localhost:11434')
            self.tools = ToolRegistry()
            logger.info("Initialization successful")
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise

    async def execute_tool(self, tool_name: str, args: Dict[str, Any], max_retries: int = 2) -> Any:
        """Execute a tool with retry logic."""
        tool = self.tools.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        logger.info(f"🔧 Executing tool {tool_name} with args: {args}")
        
        retries = 0
        last_error = None
        
        while retries <= max_retries:
            try:
                result = await tool(**args) if asyncio.iscoroutinefunction(tool) else tool(**args)
                logger.info(f"✅ Tool {tool_name} execution successful")
                return result
            except Exception as e:
                last_error = e
                retries += 1
                logger.warning(f"❌ Tool {tool_name} execution failed (attempt {retries}/{max_retries}): {e}")
                if retries <= max_retries:
                    await asyncio.sleep(1)  # Wait before retrying
        
        logger.error(f"❌ Tool {tool_name} failed after {max_retries} retries")
        raise last_error

    async def process_request(self, message: str) -> Dict[str, Any]:
        """Process a user request using the ReAct framework."""
        logger.info("="*50)
        logger.info(f"Starting new request: {message}")
        logger.info("="*50)
        
        # Initialize conversation with system prompt and user message
        try:
            system_prompt = self.prompt_path.read_text()
        except Exception as e:
            logger.error(f"Failed to read prompt file: {e}")
            system_prompt = """You are a reAct agent for finding Japanese lyrics and extracting vocabulary.
            Your goal is to find accurate lyrics and create a vocabulary list for language learners."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        max_turns = 10
        current_turn = 0
        context = []
        
        while current_turn < max_turns:
            try:
                logger.info(f"\n[Turn {current_turn + 1}/{max_turns}]")
                logger.info("-"*30)
                
                # Get LLM's next action
                logger.info("🤔 Getting next action from LLM...")
                response = await self.client.chat(
                    model="mistral",
                    messages=messages
                )
                
                # Parse the response into AgentResponse format
                try:
                    response_text = response['message']['content']
                    logger.info(f"Raw response: {response_text}")
                    
                    # Extract thought, action, and final_answer from the response
                    thought = ""
                    action = None
                    final_answer = None
                    
                    # Look for FINAL ANSWER first
                    if "FINAL ANSWER:" in response_text:
                        final_answer_text = response_text.split("FINAL ANSWER:")[1].strip()
                        try:
                            final_answer = json.loads(final_answer_text)
                            logger.info(f"Found final answer: {final_answer}")
                            return final_answer
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse final answer: {final_answer_text}")
                            logger.error(f"JSON decode error: {e}")
                    
                    # Extract thought
                    if "THOUGHT:" in response_text:
                        thought_parts = response_text.split("THOUGHT:")
                        if len(thought_parts) > 1:
                            thought = thought_parts[1].split("ACTION:")[0].strip()
                            logger.info(f"Found thought: {thought}")
                    
                    # Extract action
                    if "ACTION:" in response_text:
                        action_parts = response_text.split("ACTION:")
                        if len(action_parts) > 1:
                            action_text = action_parts[1].strip()
                            # Find the first occurrence of a JSON object
                            match = re.search(r'\{.*\}', action_text)
                            if match:
                                action_text = match.group(0)
                                try:
                                    action_data = json.loads(action_text)
                                    action = Action(
                                        tool=action_data.get("tool"),
                                        tool_input=action_data.get("tool_input", {}),
                                        thought=thought
                                    )
                                    logger.info(f"Found action: {action}")
                                except json.JSONDecodeError as e:
                                    logger.error(f"Failed to parse action: {action_text}")
                                    logger.error(f"JSON decode error: {e}")
                    
                    # Create AgentResponse object
                    agent_response = AgentResponse(
                        thought=thought,
                        action=action,
                        final_answer=final_answer
                    )
                    
                    # If we have an action, execute it
                    if agent_response.action:
                        try:
                            result = await self.execute_tool(
                                agent_response.action.tool,
                                agent_response.action.tool_input
                            )
                            logger.info(f"Tool execution result: {result}")
                            
                            # Add the result to the context
                            context.append({
                                "thought": agent_response.thought,
                                "action": agent_response.action.dict(),
                                "result": result
                            })
                            
                            # Update messages with the new context
                            messages.append({
                                "role": "assistant",
                                "content": f"THOUGHT: {agent_response.thought}\nACTION: {json.dumps(agent_response.action.dict())}\nRESULT: {json.dumps(result)}"
                            })
                            
                        except Exception as e:
                            logger.error(f"Failed to execute tool: {e}")
                            messages.append({
                                "role": "assistant",
                                "content": f"THOUGHT: {agent_response.thought}\nACTION: {json.dumps(agent_response.action.dict())}\nERROR: {str(e)}"
                            })
                    
                except Exception as e:
                    logger.error(f"Failed to parse response: {e}")
                    return {"error": f"Failed to parse response: {str(e)}"}
                
                current_turn += 1
                
            except Exception as e:
                logger.error(f"Error in turn {current_turn + 1}: {e}")
                return {"error": f"Error in turn {current_turn + 1}: {str(e)}"}
        
        logger.error("❌ Reached maximum turns without completing the task")
        return {"error": "Reached maximum turns without completing the task"}

async def run_agent(message: str) -> Dict[str, Any]:
    """Run the agent to process a message request.
    
    Args:
        message (str): The user's message request
        
    Returns:
        Dict[str, Any]: The agent's response containing lyrics and vocabulary
    """
    agent = SongLyricsAgent()
    return await agent.process_request(message) 