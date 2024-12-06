from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.prompt import *
import os
import requests

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')  # For weather API
STOCK_API_KEY = os.environ.get('STOCK_API_KEY')  # For stock prices

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "finalchatbot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Llama3-8b-8192")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("User Input:", msg)

    # Check if the query requires an external API call
    if "weather" in msg.lower():
        city = extract_city_from_query(msg)
        weather_response = fetch_weather(city)
        return jsonify({"answer": weather_response})

    elif "stock" in msg.lower():
        stock_symbol = extract_stock_symbol_from_query(msg)
        stock_price = fetch_stock_price(stock_symbol)
        return jsonify({"answer": stock_price})

    elif "image" in msg.lower():
        image_description = extract_image_description(msg)
        image_url = generate_image(image_description)
        return jsonify({"answer": f"Here is your image: {image_url}"})

    # Fallback to text-based processing
    response = rag_chain.invoke({"input": msg})
    print("Response:", response["answer"])
    return jsonify({"answer": response["answer"]})


def extract_city_from_query(query):
    # Implement logic to extract city name from the query
    return query.split("in")[-1].strip()  # Simplistic example


def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"] - 273.15  # Convert from Kelvin to Celsius
        return f"The weather in {city} is {weather} with a temperature of {temp:.2f}°C."
    return "I couldn't fetch the weather details."


def extract_stock_symbol_from_query(query):
    # Implement logic to extract stock symbol from the query
    return query.split("price of")[-1].strip()  # Simplistic example


def fetch_stock_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={STOCK_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"The current price of {symbol} is ${data['price']}."
    return "I couldn't fetch the stock price."


def extract_image_description(query):
    # Implement logic to extract image description from the query
    return query.replace("image of", "").strip()  # Simplistic example


def generate_image(description):
    url = f"https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {"prompt": description, "n": 1, "size": "1024x1024"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        return image_url
    return "I couldn't generate an image."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
