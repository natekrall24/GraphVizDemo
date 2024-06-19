import os
from openai import OpenAI
import graphviz

#This method makes an API call to gpt-3.5-turbo. It passes in the user-inputted graph along with the system prompt.
#Make sure you have the system prompt graphviz_system_prompt.md stored in a prompts folder in your directory.
def callGPT(graph):
    client = OpenAI()
    
    with open('prompts/graphviz_system_prompt.md', 'r') as f:
            systemPrompt = f.read()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": graph}
        ]
    )
    return completion.choices[0].message.content

#This method will take the Graphviz DOT language code produced by gpt-3.5-turbo and execute it.
#If for some reason there's an error executing GPT's code, an exception will be thrown.
def createGraphviz(graphCode):
    try:
        exec(graphCode)
    except Exception as e:
        print(f"Error executing code: {e}")
        exit(1)

#Takes user input describing a graph.
def takeUserInput():
    print("Enter a representation of a graph in any format:")
    return input().strip()

#Checks to make sure you have an OpenAI API Key stored in an environment variable to enable calls to GPT.
def checkPrereqs():
      if not os.getenv('OPENAI_API_KEY'):
        print('Please set the OPENAI_API_KEY environment variable to your OpenAI API key.')
        return True
      return False

#Main method checks prerequisites, takes user input, calls GPT, then creates the PNG visualization.
def main():
    if checkPrereqs():
         exit(1)
    graph = takeUserInput()
    graphCode = callGPT(graph)
    createGraphviz(graphCode)

if __name__ == "__main__":
    main()