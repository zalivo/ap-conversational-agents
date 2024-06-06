import json

from pathlib import Path
folder = Path(__file__).parent.absolute().as_posix()

from promptflow.core import tool, Prompty

@tool
def flow_entry(    
      firstName: any,
      context: any,
      question: any
) -> str:
  # path to prompty (requires absolute path for deployment)
  path_to_prompty = folder + "/basic.prompty"

  # load prompty as a flow
  flow = Prompty.load(path_to_prompty)

  image = "https://th.bing.com/th/id/R.842fb9a1885e50a762ef352821d9078d?rik=ykwt7kPK%2f3ngFA&riu=http%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2fe%2fe8%2fVan_Gogh_The_Olive_Trees..jpg&ehk=o8ZPcWcu3H0Vdk%2b2E5YJ63CXJSSHb3BFrzKL3UG5HOU%3d&risl=1&pid=ImgRaw&r=0"
  firstName = "Thomas"
  context = "this is a painting"
  question = "What can you tell me about the painting?"
  # execute the flow as function
  result = flow(
    firstName = firstName,
    context = context,
    question = question,
    image = image
  )

  return result

if __name__ == "__main__":
   json_input = '''{
  "firstName": "Thomas",
  "context": "The Alpine Explorer Tent boasts a detachable divider for privacy,  numerous mesh windows and adjustable vents for ventilation, and  a waterproof design. It even has a built-in gear loft for storing  your outdoor essentials. In short, it's a blend of privacy, comfort,  and convenience, making it your second home in the heart of nature!\\n",
  "question": "What can you tell me about your tents?"
}'''
   args = json.loads(json_input)

   result = flow_entry(**args)
   print(result)
