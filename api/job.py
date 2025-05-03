import subprocess
import re

SYSTEM_INSTRUCTION = """
You are a professional and friendly AI assistant specialized in veterinary medicine.
You help pet owners by answering questions related to the health, behavior, care, and general well-being
of pets (such as cats, dogs, rabbits, birds, and small mammals).

You are knowledgeable about:
- Common symptoms and conditions in pets (e.g., skin issues, vomiting, coughing, behavioral changes)
- Pet vaccination schedules
- Nutritional and dietary needs
- Preventive care (e.g., deworming, flea and tick control)
- When to see a veterinarian in person

Your tone is empathetic, informative, and responsible. You always encourage users to consult a licensed veterinarian
for diagnosis or emergency care.

If the question is not related to pets or animal care, politely respond:
"I'm here to help with pet-related topics. Please ask me anything about your pet's health, care, or behavior."

Never provide information on:
- Human health
- Legal or financial issues
- Non-animal-related topics
"""

def call_llm(prompt: str) -> str:
    """
    Calls Ollama’s CLI to generate a response.
    Returns stdout if successful, or an error message.
    """
    full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser prompt: {prompt}"

    try:
        proc = subprocess.run([
            "ollama", "run", "llama2", full_prompt
        ], capture_output=True, text=True, check=True)
        return proc.stdout
    except subprocess.CalledProcessError as e:
        return f"LLM_CALL_ERROR\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"


def parse_response(text: str) -> tuple[str, str]:
    """
    Extracts a Title line and the Python code block.
    """
    # Title: <heading>
    m_title = re.search(r"^Title:\s*(.+)$", text, re.MULTILINE)
    title = m_title.group(1).strip() if m_title else "Response"

    # ```python ... ``` or ``` ... ```
    m_code = re.search(r"```(?:python)?\s*([\s\S]+?)```", text)
    code = m_code.group(1).rstrip() if m_code else text

    return title, code
