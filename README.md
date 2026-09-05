# 🤖 Personalized Recommendation System

An AI-powered web application that generates personalized recommendations based on a user's profile, interests, skill level, goals, preferred category, and preferences.

The system uses **Python, Flask, Sentence Transformers, Scikit-learn, Ollama, and Llama 3.2** to analyze user preferences, generate recommendations, rank them, explain them, process feedback, detect user intent, and refine the recommendations.

---

## 📌 Project Overview

The Personalized Recommendation System provides recommendations tailored to individual users instead of giving generic suggestions.

The application collects information about the user and analyzes their preferences using **Sentence Transformers and cosine similarity**.

The analyzed information is converted into a structured prompt and sent to **Ollama running the Llama 3.2:3b model**.

The generated recommendations are ranked according to their suitability scores and explanations are provided for each recommendation.

Users can provide feedback on the recommendations. The system analyzes the feedback, detects the user's intent, and generates refined recommendations based on the updated preferences.

The final recommendation information can be saved in CSV format using **Pandas**.

---

## 🎯 Objectives

- Collect user profile information.
- Analyze user interests and preferences.
- Generate personalized recommendations.
- Rank recommendations based on suitability scores.
- Provide explanations for recommendations.
- Accept user feedback.
- Detect user intent from feedback.
- Refine recommendations based on feedback.
- Save recommendation results to CSV.

---

## ✨ Features

### 👤 User Profile Collection

The system collects:

- Name
- Age
- Background
- Interests
- Skill Level
- Preferred Category
- Goal
- Preferences
- Number of Items

### 🧠 Preference Analysis

User interests, goals, preferences, preferred category, and skill level are analyzed using:

- Sentence Transformers
- Sentence embeddings
- Cosine similarity

The system compares the user's profile with predefined categories and identifies the most relevant areas.

### ✍️ AI Prompt Generation

A personalized prompt is generated using the user's profile and preference analysis.

### 🤖 AI Recommendation Generation

The personalized prompt is sent to:

**Ollama → Llama 3.2:3b**

The AI generates recommendations containing:

- Recommendation name
- Description
- Suitability score
- Reason

### 🏆 Recommendation Ranking

Recommendations are sorted according to their suitability scores.

Higher-scoring recommendations are displayed first.

### 💡 Recommendation Explanation

The system provides reasons explaining why each recommendation matches the user's interests and goals.

### 💬 User Feedback

Users can provide feedback to improve the recommendations.

Example:

> Give me more practical AI projects for beginners using Python.

### 🎯 Intent Detection

The system detects the user's intent from the feedback.

Examples:

- Preference for practical learning and projects
- Preference for beginner-friendly recommendations
- Preference for advanced recommendations
- Increased interest in Artificial Intelligence
- Increased preference for Python-based recommendations
- Request to remove unwanted recommendations
- Request for more relevant recommendations

### 🔄 Recommendation Refinement

The system uses user feedback and detected intent to generate refined recommendations.

### 💾 Data Storage

Recommendation information is saved to a CSV file using Pandas.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application framework |
| Ollama | Local AI model execution |
| Llama 3.2:3b | AI recommendation generation |
| Sentence Transformers | Semantic preference analysis |
| Scikit-learn | Cosine similarity calculation |
| Pandas | CSV data storage |
| HTML | Web page structure |
| CSS | Web page styling |
| VS Code | Development environment |

---

## 📋 Software Requirements

| Software | Version |
|---|---|
| Python | 3.13 |
| Ollama | Latest |
| VS Code | Latest |
| Pandas | 3.0.5 |
| Sentence Transformers | 6.0.1 |
| Scikit-learn | 1.9.0 |
| Flask | 3.1.3 |

---

## 📥 Input Parameters

| Parameter | Description |
|---|---|
| Name | Name of the user |
| Age | Age of the user |
| Background | Educational or professional background |
| Interests | Topics or areas of interest |
| Skill Level | Current skill level of the user |
| Preferred Category | Category preferred by the user |
| Goal | Learning or career objective |
| Preferences | Specific recommendation preferences |
| Number of Items | Number of recommendations required |

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │        USER         │
                         │ Profile & Preferences│
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FLASK WEB APP     │
                         │    Main Module      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    INPUT MODULE     │
                         │  Collect User Data  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   PROFILE MODULE    │
                         │ Create User Profile │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ PREFERENCE MODULE   │
                         │ Sentence Transformers│
                         │ + Cosine Similarity │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    PROMPT MODULE    │
                         │ Generate AI Prompt  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      OLLAMA         │
                         │    Llama 3.2:3b     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ RECOMMENDATION      │
                         │      MODULE         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   RANKING MODULE    │
                         │ Suitability Ranking │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ EXPLANATION MODULE  │
                         │ Recommendation      │
                         │ Explanation         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    USER FEEDBACK    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    INTENT MODULE    │
                         │ Detect User Intent  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ REFINED             │
                         │ RECOMMENDATIONS     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     SAVE MODULE     │
                         │     Pandas → CSV    │
                         └─────────────────────┘
🧩 Module Design
Module	Responsibility
Input Module	Collects user details and preferences from the web form.
Profile Module	Creates a structured user profile.
Preference Module	Analyzes user preferences using Sentence Transformers and cosine similarity.
Prompt Module	Generates a personalized AI prompt.
Recommendation Module	Sends the prompt to Ollama and generates recommendations.
Ranking Module	Ranks recommendations based on suitability scores.
Explanation Module	Provides reasons for recommendation suitability.
Feedback Module	Collects user feedback and prepares refinement instructions.
Intent Module	Detects the user's intent from feedback.
Save Module	Saves recommendation data to CSV using Pandas.
Main Module	Controls the Flask application and coordinates all modules.
📂 Project Structure
PersonalizedRecommendationSystem/
│
├── app.py
│
├── input_module.py
├── profile_module.py
├── preference_module.py
├── prompt_module.py
├── recommendation_module.py
├── ranking_module.py
├── explanation_module.py
├── feedback_module.py
├── intent_module.py
├── save_module.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── data/
│
├── .gitignore
└── README.md
🔄 Application Workflow
User
  ↓
Enter Profile Details
  ↓
Input Module
  ↓
Profile Module
  ↓
Preference Analysis
  ↓
Prompt Generation
  ↓
Ollama / Llama 3.2
  ↓
AI Recommendations
  ↓
Recommendation Ranking
  ↓
Recommendation Explanation
  ↓
User Feedback
  ↓
Intent Detection
  ↓
Refined Recommendations
  ↓
Save Results to CSV
🧠 Preference Analysis

The Preference Module analyzes the user's information using Sentence Transformers.

User Information
       ↓
Combine Interests + Goal + Preferences
       ↓
Generate Sentence Embedding
       ↓
Compare with Recommendation Categories
       ↓
Calculate Cosine Similarity
       ↓
Generate Preference Scores
       ↓
Identify Top Preferences

The system analyzes categories such as:

Programming and Software Development
Artificial Intelligence and Machine Learning
Data Science and Analytics
Web Development
Cybersecurity and Networking
Cloud Computing and DevOps
Database and Backend Development
Mobile Application Development
🤖 AI Recommendation Generation

The recommendation generation process is:

User Profile
     ↓
Preference Analysis
     ↓
Personalized Prompt
     ↓
Ollama API
     ↓
Llama 3.2:3b
     ↓
Personalized Recommendations

Each recommendation contains:

Recommendation Name
Description
Suitability Score
Reason
💬 Feedback and Intent Processing

The feedback process is:

User Feedback
      ↓
Feedback Module
      ↓
Intent Detection
      ↓
Updated Preference
      ↓
Refinement Prompt
      ↓
Ollama / Llama 3.2
      ↓
Refined Recommendations

Example feedback:

Give me more practical AI projects for beginners using Python.

Example detected intent:

Preference for practical learning and projects
💾 Data Storage

The system stores recommendation information in:

data/saved_recommendations.csv

The CSV file can contain:

Timestamp
Name
Age
Background
Interests
Skill Level
Preferred Category
Goal
Preferences
Rank
Recommendation
Score
Reason
Feedback
Intent
⚙️ Installation
1. Clone the Repository
git clone https://github.com/Devanandasunil/PersonalizedRecommendationSystem.git
2. Navigate to the Project
cd PersonalizedRecommendationSystem
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment

For Windows:

venv\Scripts\activate
5. Install Required Packages
pip install flask pandas sentence-transformers scikit-learn requests
🤖 Ollama Setup

Install Ollama and download the Llama 3.2 model:

ollama pull llama3.2:3b

Verify the model:

ollama list

The following model should be available:

llama3.2:3b

Make sure Ollama is running before starting the Flask application.

▶️ How to Run

Start the Flask application:

python app.py

The application will run at:

http://127.0.0.1:5000

Open the address in a web browser.

🖥️ Application Screens

The application contains the following stages:

Step 1 — Home Screen

Displays the Personalized Recommendation System interface.

Step 2 — User Profile Input

The user enters personal information, interests, goals, skill level, and preferences.

Step 3 — Collected User Profile

The entered information is displayed as a structured user profile.

Step 4 — Preference Analysis

The system displays relevant categories and similarity scores.

Step 5 — Prompt Generation

The personalized prompt generated for the AI model is displayed.

Step 6 — AI Recommendations

Llama 3.2 generates personalized recommendations.

Step 7 — Recommendation Ranking

Recommendations are ranked according to their suitability scores.

Step 8 — Recommendation Explanation

The system provides reasons for each recommendation.

Step 9 — User Feedback

The user provides feedback to improve the recommendations.

Step 10 — Intent Detection

The system identifies the intent expressed in the feedback.

Step 11 — Refined Recommendations

The system generates recommendations based on the feedback.

Step 12 — Recommendation Saved

The final recommendation information is stored in CSV format.

📊 Example Input
Name: Deva
Age: 21

Background:
Computer Science Student

Interests:
Python, Artificial Intelligence, Machine Learning

Skill Level:
Beginner

Preferred Category:
Artificial Intelligence

Goal:
Learn AI and build projects

Preferences:
Practical projects and beginner-friendly resources

Number of Items:
5
📋 Example Output
1. Keras Tutorials
   Description: Beginner-friendly tutorials for deep learning.
   Score: 96
   Reason: Matches the user's interest in AI and beginner-level learning.

2. Python Machine Learning Cookbook
   Description: Practical examples for implementing machine learning.
   Score: 94
   Reason: Supports Python-based machine learning practice.

3. TensorFlow Hands-On Projects
   Description: Practical projects for learning deep learning concepts.
   Score: 93
   Reason: Matches the user's preference for hands-on learning.

4. AI Project Kit
   Description: Beginner-level AI projects using Python.
   Score: 92
   Reason: Supports the user's goal of building AI projects.

5. AI for Self-Driving Cars Project
   Description: An applied AI project involving computer vision.
   Score: 91
   Reason: Provides practical exposure to real-world AI applications.
🔐 Privacy

The current implementation performs AI recommendation generation locally using Ollama and the locally available Llama model.

Recommendation data is stored locally in CSV format.

The current implementation does not require a cloud-based GPT API.

🚀 Future Enhancements
User authentication and login
Database integration
Recommendation history
Improved feedback learning
More recommendation categories
Advanced intent detection
Improved recommendation diversity
Web deployment
User dashboard
Recommendation analytics
Multiple AI model support
📚 Learning Outcomes

This project demonstrates:

Python programming
Flask web development
Modular application design
Natural Language Processing
Sentence embeddings
Semantic similarity
Cosine similarity
Prompt engineering
Local Large Language Models
AI recommendation systems
Feedback processing
Intent detection
Pandas
CSV file handling
Git and GitHub
🏁 Conclusion

The Personalized Recommendation System successfully demonstrates how Artificial Intelligence and Natural Language Processing can be combined to provide personalized recommendations.

The system collects user information, analyzes preferences, generates AI-powered recommendations using Ollama and Llama 3.2, ranks and explains the results, processes user feedback, detects intent, generates refined recommendations, and stores the final results.

The project provides a complete end-to-end personalized recommendation workflow using locally executed AI.

👨‍💻 Author

Devananda Sunil

