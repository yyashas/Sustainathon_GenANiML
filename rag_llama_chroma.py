from gen_ollama import OllamaChat
from vector_store import VectorStore


def get_response(user_query):
    """
    Get a response from the AI model based on user input.
    """
    # Initialize the vector store and Ollama model
    state_list = ["kerala", "karnataka","telangana"]

    ollama_model = OllamaChat(model_name='gemma2:2b')
    state_name = ollama_model.get_state_name_from_user_query(user_query).lower()
    for i in state_list:
        if i in state_name:
            state_name = i
            break
    if state_name not in state_list: state_name = "karnataka"
    
    print(f"State name extracted from user query: {state_name}")
    collection_base_name = state_name + "_knowledge_base"

    vector_store = VectorStore(collection_name=collection_base_name)
    
    # Query the vector store for relevant documents
    ans = vector_store.query_db(user_query, n_res=10).get('documents', [])
    
    if not ans:
        return "No relevant information found in the database."

    context = " ".join(ans[0])
    # print(f"Context retrieved: {context}")

    # Get the AI model's response based on the query and context
    chat_response = ollama_model.get_response(query=user_query, context=context)
    
    return chat_response