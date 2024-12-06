from flask import Flask, request
from openai import OpenAI
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

os.environ['OPENAI_API_KEY'] = ''

# Init the Flask App
app = Flask(__name__)

# Initialize the OpenAI API key

openai.api_key = os.environ.get("OPENAI_API_KEY")


# Define a function to generate answers using GPT-3
def generate_answer(question):
  client = OpenAI()
    
  response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with questions, and your task is to answer those"
    },
    {
      "role": "user",
      "content": question
    }
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
  )
  
  answer = response.choices[0].message.content
    
  return answer


# Define a route to handle incoming requests
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    print("values:",request.values)
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)
    # Generate the answer using GPT-3
    answer = generate_answer(incoming_que)
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
