from brain.memory import get_memories
from brain.personality import SYSTEM_PERSONALITY
from tools.calculator import calculate


def detect_tool(user_input):
    """Detect which tool should handle the request."""
    text = user_input.lower().strip()

    if text.startswith("calculate "):
        return "calculator"

    return None


def build_context(user_input):
    """Build context using personality and recent memories."""
    memories = get_memories(limit=10)

    if memories:
        memory_text = "\n".join(
            f"- {memory}" for memory in memories
        )
    else:
        memory_text = "No previous memories."

    return {
        "personality": SYSTEM_PERSONALITY,
        "user_input": user_input,
        "memories": memory_text
    }


def process(user_input):
    """Main JARVIS Brain processing function."""

    if not user_input or not user_input.strip():
        return "Please tell me what you need."

    tool = detect_tool(user_input)

    # Tool execution
    if tool == "calculator":
        expression = user_input[len("calculate "):].strip()
        result = calculate(expression)

        return f"Calculation result: {result}"

    # Build AI context
    context = build_context(user_input)

    return (
        "JARVIS BRAIN V6.0\n\n"
        f"User: {context['user_input']}\n\n"
        f"Recent Memory:\n{context['memories']}\n\n"
        "AI model connection is not configured yet."
    )
