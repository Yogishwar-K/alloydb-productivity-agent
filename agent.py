import os
import pg8000.native
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

load_dotenv()

# --- 1. Database Connection Setup ---
def get_db_connection():
    """Establishes a connection to the AlloyDB instance."""
    db_url = os.getenv("DATABASE_URL")
    parts = db_url.replace("postgresql+pg8000://", "").split("@")
    user_pass = parts[0].split(":")
    host_port_db = parts[1].split("/")
    host_port = host_port_db[0].split(":")
    
    return pg8000.native.Connection(
        user=user_pass[0],
        password=user_pass[1],
        host=host_port[0],
        port=int(host_port[1]),
        database=host_port_db[1]
    )

# --- 2. ADK Tools (AlloyDB Integration) ---
def add_productivity_task(tool_context: ToolContext, task_name: str, task_context: str) -> dict[str, str]:
    """Adds a new task using AlloyDB's native embedding function."""
    conn = get_db_connection()
    try:
        query = """
            INSERT INTO tasks (task_name, task_context, task_vector)
            VALUES (
                :name, :context,
                embedding('text-embedding-005', :name || ' ' || :context)::vector
            )
        """
        conn.run(query, name=task_name, context=task_context)
        return {"status": "success", "message": f"Task '{task_name}' added to your productivity queue."}
    finally:
        conn.close()

def semantic_task_search(tool_context: ToolContext, search_query: str) -> dict[str, str]:
    """Searches for tasks using AlloyDB AI semantic search and Gemini vibe checks."""
    conn = get_db_connection()
    try:
        query = """
            SELECT task_name, task_context,
                   1 - (task_vector <=> embedding('text-embedding-005', :query)::vector) as score
            FROM tasks
            WHERE task_vector IS NOT NULL
              AND ai.if(
                    prompt => 'Does this task context: "' || task_context ||'" relate to the user goal: "' || :query || '"?',
                    model_id => 'gemini-3-flash-preview'
                  )
            ORDER BY score DESC
            LIMIT 3
        """
        results = conn.run(query, query=search_query)
        if not results:
            return {"status": "success", "data": "No matching tasks found."}
        
        formatted_results = [f"Task: {row[0]} | Context: {row[1]}" for row in results]
        return {"status": "success", "tasks": formatted_results}
    finally:
        conn.close()

# --- 3. The Multi-Agent Orchestration ---
root_agent = Agent(
    name="productivity_coordinator",
    model=os.getenv("MODEL", "gemini-3.1-pro-preview"),
    description="The primary agent managing the user's workload.",
    instruction="""
    You are an elite Productivity Assistant. You manage the user's workload by interacting with the database tools.
    - If the user wants to add a task, use the 'add_productivity_task' tool.
    - If the user is looking for advice on what to do next, or asks about existing tasks, use the 'semantic_task_search' tool.
    Always synthesize the tool output into a highly professional, encouraging response.
    """,
    tools=[add_productivity_task, semantic_task_search]
)