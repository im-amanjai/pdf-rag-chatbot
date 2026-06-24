import os
import time

from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "gemini"
).lower()

# Gemini

if LLM_PROVIDER == "gemini":

    from langchain_google_genai import (
        ChatGoogleGenerativeAI
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv(
            "GOOGLE_API_KEY"
        ),
        temperature=0.1
    )

# Ollama

elif LLM_PROVIDER == "ollama":

    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0.1
    )

# Invalid Provider

else:

    raise ValueError(
        f"Unsupported provider: {LLM_PROVIDER}"
    )


def generate_answer(question, docs):

    question = question.strip().lower()

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # Cleanup
    context = context.replace("|", " ")

    summary_keywords = [
        "summary",
        "summarize",
        "summarise",
        "overview",
        "resume summary",
        "give me summary"
    ]

    is_summary_query = any(
        keyword in question
        for keyword in summary_keywords
    )

    # Summary Mode

    if is_summary_query:

        prompt = f"""
You are an expert document summarizer.

Rules:

1. Use ONLY information explicitly present in the context.
2. Never invent information.
3. Never assume missing values.
4. Give exactly 5 bullet points.
5. Keep bullets concise.
6. Do not repeat information.
7. Never convert percentages into CGPA.
8. Never convert CGPA into percentage.
9. Use values exactly as written.

For resumes focus on:
- Candidate Name
- Education
- Skills
- Experience
- Projects
- Certifications/Achievements

For technical documents focus on:
- Main topic
- Important concepts
- Architecture/components
- Features
- Applications

Context:
{context}

Summary:
"""

    # Q&A Mode

    else:

        prompt = f"""
You are an expert document assistant.

Answer ONLY using the provided context.

Rules:

1. Carefully analyze all retrieved chunks.
2. Use information from multiple chunks if needed.
3. Connect related information when clearly linked.

Examples:

If context contains:
"Master of Computer Applications ... CGPA: 9/10"

Question:
"What is the MCA CGPA?"

Answer:
"9/10"

If context contains:
"Bachelor of Computer Applications ... Overall 74%"

Question:
"What is the BCA percentage?"

Answer:
"74%"

If context contains:
"AMAN JAISWAL"

Question:
"Candidate name?"

Answer:
"Aman Jaiswal"

4. Return short direct answers whenever possible.
5. Do not hallucinate.
6. Use only information present in the context.
7. Only respond with:

"I could not find this information in the uploaded PDF."

when the information truly does not exist.

Context:
{context}

Question:
{question}

Answer:
"""

    # Retry Logic    

    for attempt in range(3):

        try:

            response = llm.invoke(prompt)

            content = response.content

            # Normal string response
            if isinstance(content, str):
                return content

            # Structured Gemini response
            if isinstance(content, list):

                result = []

                for item in content:

                    if isinstance(item, dict):

                        if item.get("type") == "text":

                            result.append(
                                item.get("text", "")
                            )

                    elif hasattr(item, "text"):

                        result.append(
                            item.text
                        )

                return "\n".join(result)

            return str(content)

        except Exception as e:

            if attempt < 2:

                time.sleep(3)

            else:

                return (
                    f"LLM Error: {str(e)}"
                )

