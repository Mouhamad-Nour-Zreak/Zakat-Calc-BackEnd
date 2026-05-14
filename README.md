# 🕌 Zakat Calculator - Knowledge-Based System Backend

A sophisticated **expert system** for calculating Islamic Zakat (alms tax) using the Experta framework. This backend intelligently gathers user information through a guided Q&A process and accurately computes Zakat obligations across multiple asset categories using classical Islamic jurisprudence rules.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Core Modules](#-core-modules)
- [How It Works](#-how-it-works)
- [Requirements](#-requirements)
- [Contributing](#-contributing)

---

## ✨ Features

- **🤖 Expert System Architecture**: Implements a knowledge-based inference engine using Experta framework for intelligent decision-making
- **💰 Multi-Asset Zakat Calculation**: Handles calculation across:
  - Livestock (Camels, Cows, Sheep/Goats)
  - Crops & Plants (Agricultural produce)
  - Cash & Money
  - Gold & Silver
  - Trade Goods/Merchandise
  - Buried Treasures (Rikaz)
- **❓ Interactive Q&A System**: User-friendly guided questionnaire that collects necessary information step-by-step
- **⚖️ Jurisprudential Accuracy**: Based on Islamic scholarly consensus for Zakat calculations
- **🔄 State Management**: Robust state tracking for multi-step questionnaire flow
- **📡 RESTful API**: FastAPI-based REST endpoints for integration with frontend applications
- **🔐 Async Processing**: Non-blocking asynchronous request handling for better performance

---

## 🎯 Project Overview

This Knowledge-Based System (KBS) implements an **expert system** that guides users through the Islamic Zakat obligation process. Rather than simple form-filling, it uses intelligent rules to:

1. Ask relevant questions based on user's asset ownership
2. Infer which asset categories need Zakat calculation
3. Gather detailed information about each asset type
4. Apply Sharia-compliant rules to compute final Zakat amounts
5. Present comprehensive results to the user

The system respects the complexity of Islamic finance, handling edge cases and different school of thought (Madhab) considerations where applicable.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Frontend (Separate Repository)             │
│                   (Flutter/iOS)                         │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/REST
                  ▼
┌─────────────────────────────────────────────────────────┐
│           FastAPI REST API Layer (link/api.py)          │
│                                                         │
│  GET  /start              - Initialize engine           │
│  POST /submit-answer      - Submit user responses       │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│          State Manager (link/state.py)                  │
│   Manages question flow and engine lifecycle            │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│    Expert System Engine (modules/zakah/MainEngine.py)   │
│                                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Rules Engine (Experta Framework)                  │ │
│  │  - Knowledge Base with 50+ rules                   │ │
│  │  - Inference system for dynamic flow               │ │
│  └────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Sub-Engines for Each Asset Type                   │ │
│  │  - CamelEngine      - MoneyEngine                  │ │
│  │  - CowEngine        - PlantsEngine                 │ │
│  │  - SheepEngine      - TradeOffersEngine            │ │
│  │  - BuriedMoneyEngine                               │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│     Question System (modules/questioning/)              │
│  - Question Engine     - Validator                      │
│  - Answer Processing   - Question & Answer models       │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│     Helper Utilities (modules/helpers/)                 │
│  - Data collection     - Metal price fetching           │
│  - Frozen data conversion                               │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mouhamad-Nour-Zreak/Zakat-Calc-BackEnd.git
   cd Zakat-Calc-BackEnd
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env  # Create from template if available
   # Edit .env with your configuration
   ```

---

## 🚀 Usage

### Running the Expert System Directly

For testing the Zakat calculation engine directly:

```bash
python main.py
```

This will:
1. Initialize the MainEngine with knowledge base
2. Ask interactive questions about your assets
3. Calculate Zakat obligations
4. Display results

### Running the API Server

To start the REST API for frontend integration:

```bash
uvicorn link.api:api --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit `http://localhost:8000/docs` for interactive Swagger documentation.

---

## 📡 API Endpoints

### `GET /start`

**Initialize the Zakat calculation engine and get the first question.**

- **Response**:
  ```json
  {
    "question_id": "cattel_ownership",
    "question_text": "Do you own any livestock?",
    "question_type": "yes_no",
    "options": ["yes", "no"]
  }
  ```

### `POST /submit-answer`

**Submit an answer to a question and receive the next question or final results.**

- **Request Body**:
  ```json
  {
    "answer": "yes"
  }
  ```

- **Response (Intermediate)**:
  ```json
  {
    "question_id": "grazing_cattels",
    "question_text": "Did your livestock graze for most of the year?",
    "question_type": "yes_no",
    "options": ["yes", "no"]
  }
  ```

- **Response (Final - When calculation complete)**:
  ```json
  {
    "status": "complete",
    "zakat_results": {
      "camels": 0,
      "cows": 2,
      "sheep": 0,
      "money": 5000,
      "total_zakat": 425,
      "currency": "USD"
    }
  }
  ```

---

## 📁 Project Structure

```
Zakat-Calc-BackEnd/
├── main.py                      # Entry point for direct execution
├── requirements.txt             # Project dependencies
├── Collector.py                 # Data collection utility
│
├── link/
│   ├── api.py                   # FastAPI REST endpoints
│   └── state.py                 # State management for question flow
│
├── modules/
│   ├── helpers/
│   │   └── helpers.py           # Utility functions (data processing, metal prices)
│   │
│   ├── questioning/
│   │   ├── Question.py          # Question model
│   │   ├── Answer.py            # Answer model
│   │   ├── QuestionEngine.py    # Q&A engine
│   │   └── Validator.py         # Input validation
│   │
│   └── zakah/
│       ├── MainEngine.py        # Primary expert system with rules
│       ├── CamelEngine.py       # Camel Zakat calculation
│       ├── CowEngine.py         # Cow Zakat calculation
│       ├── SheepEngine.py       # Sheep/Goat Zakat calculation
│       ├── PlantsEngine.py      # Agricultural produce Zakat
│       ├── MoneyEngine.py       # Cash & Money Zakat
│       ├── TradeOffersEngine.py # Trade goods Zakat
│       ├── BuriedMoneyEngine.py # Buried treasure (Rikaz) Zakat
│       └── facts.py             # Zakah fact model
│
├── Data/
│   ├── questions.py             # Question definitions
│   └── questionswithLine.py     # Extended question set
│
└── README.md                    # This file
```

---

## 🧠 Core Modules

### **MainEngine** (`modules/zakah/MainEngine.py`)

The heart of the system - an Experta KnowledgeEngine with 50+ inference rules:

- **Rule Priority System**: Salience values (8 to -3) control question order
- **Fact Tracking**: Maintains Zakah and UserState facts
- **Sub-Engine Orchestration**: Sequentially invokes specialized engines
- **Flow Control**: Halts when all calculations complete

**Key Rules**:
```python
@Rule(AS.user_state << UserState(has_cattels=L(True), ...))
def cattel_details(self, user_state, zakah):
    # Process livestock sequentially: Camels → Cows → Sheep
```

### **Individual Asset Engines**

Each specialized engine handles one asset category:

| Engine | Calculates | Rules |
|--------|-----------|-------|
| **CamelEngine** | Camel Zakat (1 camel per 5-25 depending on count) | Age, count, grazing period |
| **CowEngine** | Cattle Zakat (1 cow per 30 head) | Age, count, grazing status |
| **SheepEngine** | Sheep/Goat Zakat (1 per 40 head) | Age, count, condition |
| **MoneyEngine** | Cash, Savings, Investments | Nisab threshold, growth calculations |
| **PlantsEngine** | Crops & Agricultural Produce | Harvest quantity, crop type, irrigation |
| **TradeOffersEngine** | Merchandise & Trade Goods | Inventory value, market price |
| **BuriedMoneyEngine** | Buried Treasure (Rikaz) | Found amount, ownership rules |

### **Question System** (`modules/questioning/`)

Manages the interactive questionnaire:

- **QuestionEngine**: Runs individual questions
- **Question/Answer Models**: Data structures for Q&A
- **Validator**: Ensures input correctness
- **Collector**: Stores user responses for fact building

---

## 🔄 How It Works

### Execution Flow

```
1. User starts engine via /start endpoint
   ↓
2. MainEngine initializes with Zakah & UserState facts
   ↓
3. Rules fire in salience order (highest priority first)
   ↓
4. First rule asks: "Do you have trade offers?"
   ↓
5. User answers via /submit-answer
   ↓
6. Answer triggers QuestionEngine
   ↓
7. Fact updated, next highest-priority rule fires
   ↓
8. Process repeats until all facts gathered
   ↓
9. Sub-engines (Camel/Cow/Sheep/Money/etc.) run sequentially
   ↓
10. Each engine performs calculations and updates Zakah fact
    ↓
11. When no more questions needed, finish() rule halts engine
    ↓
12. Results returned to frontend with final Zakat amount
```

### Example: Livestock Flow

```
"Do you own livestock?" → YES
  ↓
"Do they graze most of the year?" → YES
  ↓
[CamelEngine runs]
"How many camels?" → 10
"What age?" → Adult
  ↓
[CowEngine runs]
"How many cows?" → 5
  ↓
[SheepEngine runs]
"How many sheep?" → 20
  ↓
Result: Camel zakat + Cow zakat + Sheep zakat calculated ✓
```

---

## 📋 Requirements

```
experta          # Expert system framework
fastapi          # Web API framework
uvicorn          # ASGI web server
pydantic         # Data validation
python-dotenv    # Environment variable management
requests         # HTTP requests for external APIs
```

For exact versions, see `requirements.txt`

---

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/zakat-improvements`
3. **Commit changes**: `git commit -am 'Add new Zakat calculation rule'`
4. **Push to branch**: `git push origin feature/zakat-improvements`
5. **Submit a Pull Request**

### Areas for Enhancement
- [ ] Add support for cryptocurrency Zakat
- [ ] Implement multiple Madhab (school of thought) support
- [ ] Add debt obligation deductions
- [ ] Create comprehensive test suite
- [ ] Add multilingual question support
- [ ] Implement gold/silver price API integration
- [ ] Add calculation history/export features

---

## 📚 Islamic Reference

This system is built on classical Islamic jurisprudence principles regarding Zakat:

- **Nisab**: Minimum wealth threshold (typically equivalent to 85g of gold)
- **Hawl**: Full lunar year of ownership requirement
- **2.5% Rate**: Standard Zakat percentage on qualifying assets
- **School of Thought**: Primary alignment with Hanafi Madhab with variations

---

## 📄 License

This project is part of the Zakat Calculator Knowledge-Based System.

---

## 👨‍💻 Contributers

**Mouhamad Nour Zreak**
**Mohamad Yasen**
**Mouhamad Obada Al-Masri**
**Abd-Al-Rhman Al-Hamod**
**Abd-Al-Hafez Al-Kurdi**


---

## 🙏 Acknowledgments

- Built with [Experta Framework](https://experta.readthedocs.io/) for expert systems
- API powered by [FastAPI](https://fastapi.tiangolo.com/)
- Islamic jurisprudence consultation from classical sources

---

## 📞 Support

For issues, questions, or suggestions:
- 📧 Open an issue on GitHub
- 💬 Check existing issues/discussions
- 🔗 Reference Islamic Zakat sources for calculation clarifications

---

**Last Updated**: 2024 | Version: 1.0
