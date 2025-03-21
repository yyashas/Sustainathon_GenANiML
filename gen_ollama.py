import ollama

'''
# ollama.pull('llama3.2:1b')
'''


class OllamaChat:
    """
    A class to interact
    with the Ollama chat model.
    """
    def __init__(self, model_name='llama3.2:1b'):
        """
        Initialize the OllamaChat with a model name.    
        """
        self.model_name = model_name

    def chat(self, messages):
        """
        Interact with the Ollama chat model.
        """
        response = ollama.chat(model=self.model_name, messages=messages)
        return response

    def get_response(self, query, context):
        """
        Get a response from the Ollama chat model based on a query and context.
        """
        response = self.chat(messages = [{
            'role': 'system',
            'content': f"""
            You are a Wildlife and Environmental Law assistant specializing in Human-Wildlife Conflict Resolution. You provide legally sound, ethical, and practical advice based on national wildlife laws, environmental regulations.

            **USE THIS CONTEXT FOR ANSWERING THE USER'S QUERY**
            **DO NOT DEVIATE FROM THE CONTEXT**
            **DO NOT ADD ANYTHING NEW APART FROM THE GIVEN CONTEXT**
            CONTEXT START
            {context}
            CONTEXT END
            
            The context provided is crucial for generating accurate and relevant responses. So please ensure to use it effectively.
            Provide a step-by-step approach for the user to follow.

            Include the monetary compensation amount in INR if applicable and available in the context.

            """
                    },
            {
                'role': 'user',
                'content': query
            }])
        return response['message']['content'].replace("**", "").replace("*", "")
    
    def get_state_name_from_user_query(self, query):
        """
        Extract the state name from the user query.
        """
        response = ollama.chat(model=self.model_name, messages=[{'role': 'system', 
                                                                'content': f"""
                                                                You are a Indian State Recognition AI
                                                                I will give you a text that may contain various pieces of information. Your task is to find the name of an Indian state in it and return just the state's name. If no state is mentioned, return 'None'. Here is the text: {query}
                                                                """},
                                                                ])
        
        return response['message']['content'].replace("**", "").replace("*", "")