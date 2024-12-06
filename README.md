# End-to-End Chatbot with Generative AI and Voice Input

This is an end-to-end chatbot project leveraging Generative AI, Pinecone, and LangChain, now enhanced with **voice input functionality**. Users can interact with the chatbot via text or voice, and the application also supports weather, stock, and image generation queries.

---

## How to Run?

### **STEPS:**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/midproject.git
   ```

2. Navigate to the repository:
   ```bash
   cd midproject
   ```

3. **STEP 01**: Create a conda environment:
   ```bash
   conda create -n midproject python=3.10 -y
   conda activate midproject
   ```

4. **STEP 02**: Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

5. **STEP 03**: Create a `.env` file in the root directory and add your credentials:
   ```ini
   PINECONE_API_KEY = "your_pinecone_api_key"
   GROQ_API_KEY = "your_groq_api_key"
   OPENAI_API_KEY = "your_openai_api_key"
   WEATHER_API_KEY = "your_weather_api_key"
   STOCK_API_KEY = "your_stock_api_key"
   ```

6. **STEP 04**: Store embeddings to Pinecone:
   ```bash
   python store_index.py
   ```

7. **STEP 05**: Start the chatbot application:
   ```bash
   python app.py
   ```

8. **STEP 06**: Open your browser and navigate to:
   ```bash
   http://localhost:8080
   ```

---

## Features

1. **Interactive Chat**: Users can type questions or use voice input to interact with the chatbot.
2. **Dynamic Responses**: Supports natural language understanding and generative responses using LangChain and GPT.
3. **Integrated APIs**:
   - **Weather API**: Get real-time weather updates.
   - **Stock API**: Fetch stock prices for any symbol.
   - **Image Generation**: Generate images based on prompts using OpenAI's DALLE.
4. **Voice Input**: Uses the Web Speech API to transcribe voice to text.
5. **Deployment Ready**: Easily deployable with AWS using CI/CD pipelines.

---

## Tech Stack

- **Python**: Core programming language
- **LangChain**: For handling conversational AI workflows
- **Flask**: Web framework
- **Pinecone**: Vector database for embedding storage
- **OpenAI GPT**: For generative responses
- **Web Speech API**: For voice-to-text functionality

---

## AWS CI/CD Deployment with GitHub Actions

### **Deployment Process**

1. **Login to AWS Console**.

2. **Create IAM User for Deployment**:
   - **Required Access**:
     1. **EC2 Access**: Virtual Machine.
     2. **ECR Access**: Elastic Container Registry to store Docker images.

3. **Description**:
   - Build Docker image of the source code.
   - Push the Docker image to ECR.
   - Launch EC2 instance.
   - Pull the Docker image from ECR to EC2.
   - Run the Docker container on EC2.

4. **Policies Required**:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonEC2FullAccess`

5. **Create ECR Repository**:
   - Save the URI: `970547337635.dkr.ecr.ap-south-1.amazonaws.com/midproject`.

6. **Create EC2 Machine (Ubuntu)**.

7. **Install Docker in EC2 Machine**:
   ```bash
   sudo apt-get update -y
   sudo apt-get upgrade -y
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```

8. **Configure EC2 as Self-Hosted Runner**:
   - Go to `Settings > Actions > Runners > New self-hosted runner`.
   - Choose the OS and follow the provided commands.

9. **Setup GitHub Secrets**:
   - Add the following secrets in your repository:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`
     - `AWS_DEFAULT_REGION`
     - `ECR_REPO`
     - `PINECONE_API_KEY`
     - `GROQ_API_KEY`
     - `OPENAI_API_KEY`
     - `WEATHER_API_KEY`
     - `STOCK_API_KEY`

---

## Example Chatbot Interface

Here’s a preview of the chatbot interface with **voice input**:

![Example Chatbot](assets/images/example.png)

---

## Voice Input Instructions

1. Click on the **microphone icon** next to the text input field.
2. Speak your question.
3. The chatbot will convert your voice input to text and process your query.

---

This README provides complete steps for setup, usage, and deployment with AWS, now enhanced with voice input functionality.
