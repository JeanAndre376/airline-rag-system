"""Airline RAG System - Core Query Functions

A Retrieval-Augmented Generation system for answering questions about 
airline pricing using Databricks Vector Search and Foundation Model API.
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
import json

# Configuration
INDEX_NAME = "airlines.silver_gold.rag_knowledge_index"
LLM_ENDPOINT = "databricks-meta-llama-3-3-70b-instruct"

# Initialize Databricks client
w = WorkspaceClient()


def search_knowledge_base(question: str, num_results: int = 3) -> list:
    """
    Search the vector index for relevant knowledge chunks.
    
    Args:
        question (str): Natural language question to search for
        num_results (int): Number of chunks to retrieve (default: 3)
    
    Returns:
        list: List of dicts with keys 'id', 'title', 'content'
    
    Example:
        >>> chunks = search_knowledge_base("Why is Business class expensive?")
        >>> print(f"Found {len(chunks)} chunks")
    """
    print(f"\n🔍 Searching knowledge base for: '{question}'")
    
    # Query the vector search index
    results = w.vector_search_indexes.query_index(
        index_name=INDEX_NAME,
        query_text=question,
        columns=["id", "title", "content"],
        num_results=num_results
    )
    
    # Extract and format results
    chunks = []
    if results.result and results.result.data_array:
        for row in results.result.data_array:
            chunks.append({
                "id": row[0],
                "title": row[1],
                "content": row[2]
            })
    
    print(f"✓ Found {len(chunks)} relevant chunks")
    return chunks


def generate_answer(question: str, context_chunks: list) -> str:
    """
    Generate an answer using the LLM with retrieved context.
    
    Args:
        question (str): The question to answer
        context_chunks (list): List of knowledge chunks from search
    
    Returns:
        str: Generated answer from the LLM
    
    Example:
        >>> chunks = search_knowledge_base("Why are direct flights cheaper?")
        >>> answer = generate_answer("Why are direct flights cheaper?", chunks)
    """
    # Build context from chunks
    context_text = "\n\n".join([
        f"[Chunk {c['id']}: {c['title']}]\n{c['content']}" 
        for c in context_chunks
    ])
    
    # Construct the prompt
    prompt = f"""You are an airline pricing expert. Answer the question based on the provided context.

Context from knowledge base:
{context_text}

Question: {question}

Answer the question using ONLY the information in the context above. If the context doesn't contain enough information, say so. Include which chunks you used."""

    print(f"\n🤖 Generating answer with {LLM_ENDPOINT}...")
    
    # Call the Foundation Model API
    response = w.serving_endpoints.query(
        name=LLM_ENDPOINT,
        messages=[ChatMessage(role=ChatMessageRole.USER, content=prompt)],
        max_tokens=500,
        temperature=0.1
    )
    
    answer = response.choices[0].message.content
    print("✓ Answer generated")
    
    return answer


def ask_rag(question: str) -> dict:
    """
    Complete RAG pipeline: retrieve relevant chunks and generate an answer.
    
    This is the main entry point for the RAG system. It combines semantic search
    with LLM generation to produce cited answers.
    
    Args:
        question (str): Natural language question about airline pricing
    
    Returns:
        dict: Contains 'question', 'answer', and 'sources' keys
    
    Example:
        >>> result = ask_rag("Why is Business class more expensive?")
        >>> print(result["answer"])
        >>> print(f"Used {len(result['sources'])} sources")
    """
    print("\n" + "=" * 60)
    print(f"QUESTION: {question}")
    print("=" * 60)
    
    # Step 1: Retrieve relevant chunks
    chunks = search_knowledge_base(question, num_results=3)
    
    if not chunks:
        return {
            "question": question,
            "answer": "No relevant information found in the knowledge base.",
            "sources": []
        }
    
    # Step 2: Generate answer with context
    answer = generate_answer(question, chunks)
    
    # Display results
    print("\n" + "=" * 60)
    print("ANSWER:")
    print("=" * 60)
    print(answer)
    print("\n" + "=" * 60)
    print("SOURCES:")
    print("=" * 60)
    for chunk in chunks:
        print(f"• Chunk {chunk['id']}: {chunk['title']}")
    print("=" * 60)
    
    return {
        "question": question,
        "answer": answer,
        "sources": chunks
    }


if __name__ == "__main__":
    # Example usage
    print("Airline RAG System - Example Queries")
    print("=" * 60)
    
    # Test with a sample question
    result = ask_rag("Why is Business class more expensive than Economy?")
    
    print("\n" + "=" * 60)
    print("RAG System Ready!")
    print("=" * 60)
    print("\nTry these functions:")
    print("  - ask_rag('your question')")
    print("  - search_knowledge_base('your question')")
    print("  - generate_answer('question', chunks)")
