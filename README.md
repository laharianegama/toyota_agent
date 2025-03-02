# Toyota Chat Assistant

A conversational AI assistant built with LangGraph that helps users with Toyota-related inquiries, includes vehicle availability checks, service appointment bookings, and test drive scheduling.

---

## 🚗 Project Overview

This project demonstrates the use of LangGraph for building a graph-based conversational agent. The assistant consists of a central router that directs user queries to specialized workflows (skills) based on the content of the query.

### Core Components

- **Assistant (Core Brain)**

  - Receives user input
  - Routes requests to the appropriate workflow
  - Aggregates responses and returns them to the user

- **Specialized Workflows ("Skills")**

  - **Vehicle Availability Check:**  
    Checks Toyota inventory for specified models using a simulated dataset. Users can request availability by model.
  - **Service Appointment Booking:**  
    Allows users to book vehicle service appointments. Displays available slots grouped by date and location and lets users select slots using a simple numbering system.
  - **Test Drive Scheduling:**  
    Schedules test drives at nearby Toyota dealerships. Uses an LLM to find the closest dealership to the user's location and provides dealership information including available models.

- Each workflow node processes its task independently.
- The router uses an LLM to determine which workflow should handle the query.
- Special pattern matching ensures follow-up messages are routed correctly.

---

## 📋 Requirements

- Python 3.8+
- FastAPI
- Streamlit
- LangGraph
- LangChain
- Access to LLM providers (e.g., Groq, Fireworks, NVIDIA, Cerebras)

---

## 🚀 Getting Started

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/toyota-agent.git
   cd toyota-agent

   ```

2. **Install Requirements**

```bash
   pip install -r requirements.txt
```

3. **Create an .env file**

- LLM_TO_USE=groq (Options: groq, fireworks, nvidia, cerebras)
- GROQ_API_KEY=your_groq_api_key
- LANGCHAIN_API_KEY=your_langsmith_api_key
- LANGCHAIN_PROJECT=toyota-assistant
- LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

4. **Running the Application**
    - Start the backend server:

    ```bash
    python -m uvicorn orchestration.main:app --reload --port 8000
     ```
    - In a separate terminal, start the Streamlit frontend:
      
    ```bash
    streamlit run app.py
     ```

### Access the application at: http://localhost:8501

