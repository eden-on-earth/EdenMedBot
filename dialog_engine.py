import yaml
from bedrock_llm import analyze_user_input

# Load YAML conversation flow
with open("appointment_flow.yaml", "r") as f:
    flow = yaml.safe_load(f)["nodes"]

# In-memory session store
session_states = {}

def find_node(node_id):
    """Find a node by its ID in the flow."""
    return next(node for node in flow if node["id"] == node_id)

def run_dialog(user_input, session_id):
    """
    Advances the dialog based on user input and session state.
    """
    # Load or initialize session
    session = session_states.get(session_id, {
        "current_node_id": "greet",
        "entities": {}
    })

    current_node = find_node(session["current_node_id"])

    # Analyze user input (intent + entities)
    result = analyze_user_input(user_input)
    intent = result.get("intent")
    new_entities = result.get("entities", {})

    # Update session with newly extracted entities
    session["entities"].update({k: v for k, v in new_entities.items() if v})

    print("DEBUG - Session Entities:", session["entities"])

    # Check for required entities
    required_entities = current_node.get("entities", [])
    if required_entities:
        all_present = all(
            session["entities"].get(entity) for entity in required_entities
        )
        if all_present:
            # Skip current node → go to on_success
            session["current_node_id"] = current_node.get("on_success", session["current_node_id"])
            current_node = find_node(session["current_node_id"])
            prompt = current_node.get("prompt", "...")
        else:
            # Ask for missing entities
            prompt = current_node.get("prompt", "...")
    else:
        prompt = current_node.get("prompt", "...")

    # Handle transitions (intent-based)
    if "transitions" in current_node:
        for transition in current_node["transitions"]:
            if transition["condition"] == intent:
                session["current_node_id"] = transition["target"]
                current_node = find_node(session["current_node_id"])
                prompt = current_node.get("prompt", "...")
                break

    # Replace placeholders in prompt with known entities
    for key, value in session["entities"].items():
        if value:
            prompt = prompt.replace(f"{{{key}}}", value)

    # Save updated session
    session_states[session_id] = session

    return prompt
