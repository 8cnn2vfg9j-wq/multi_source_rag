import os
from src.vector_store import query_knowledge_base

STRICT_THRESHOLD = 1.15
RELAXED_THRESHOLD = 1.35


def generate_rag_answer(user_query: str, top_k: int = 1, threshold: float = STRICT_THRESHOLD):
    """Retrieves context with primary thresholding and dynamic fallback recovery."""
    search_results = query_knowledge_base(user_query, top_k=top_k)

    docs = search_results.get('documents', [[]])[0] or []
    distances = search_results.get('distances', [[]])[0] or []
    metadatas = search_results.get('metadatas', [[]])[0] or [{}] * len(docs)

    filtered_sources = []
    if docs and distances:
        # Tier 1: User-defined / Strict threshold matching
        for doc, dist, meta in zip(docs, distances, metadatas):
            if dist <= threshold:
                filtered_sources.append({
                    "text": doc,
                    "distance": round(dist, 4),
                    "metadata": meta
                })

        # Tier 2: Dynamic fallback matching if primary threshold yields no results
        if not filtered_sources:
            for doc, dist, meta in zip(docs, distances, metadatas):
                if dist <= RELAXED_THRESHOLD:
                    filtered_sources.append({
                        "text": doc,
                        "distance": round(dist, 4),
                        "metadata": meta
                    })

    # Out-of-Domain fallback response
    if not filtered_sources:
        fallback = "Sorry, this information is not available. Maybe try after sometime."
        return fallback, []

    retrieved_context = "\n\n".join([item["text"] for item in filtered_sources])
    api_key = os.getenv("GEMINI_API_KEY")

    # Local Extractor Mode (Fallback when GEMINI_API_KEY is not set)
    if not api_key:
        extracted_answers = []
        for src in filtered_sources:
            text = src["text"]
            if "Answer:" in text:
                ans_part = text.split("Answer:")[1].strip()
                if " (Keywords:" in ans_part:
                    ans_part = ans_part.split(" (Keywords:")[0].strip()
                extracted_answers.append(ans_part)
            else:
                extracted_answers.append(text)

        final_answer = "\n\n".join(extracted_answers)
        return final_answer, filtered_sources

    # Gemini LLM Mode
    try:
        from google import genai
        from google.genai import types

        prompt = f"""
        You are an AI community assistant for a university student group. 
        Answer the student's question using ONLY the retrieved context below. 

        --- RETRIEVED CONTEXT ---
        {retrieved_context}
        --- END CONTEXT ---

        Student Question: {user_query}
        Helpful Answer:
        """

        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2)
        )
        return response.text, filtered_sources

    except Exception as e:
        return f"Error executing model generation: {str(e)}", filtered_sources