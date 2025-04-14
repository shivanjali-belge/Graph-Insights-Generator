AI-powered Data Visualization and Insight Extraction System

This project is designed to help users easily upload CSV datasets, generate a variety of useful graphs, and receive insights powered by Google Gemini 1.5 Pro. It combines FastAPI for backend services and a potential Streamlit frontend to deliver a smooth, interactive experience. The aim is to simplify data exploration and analysis using AI.

Features

Users can upload their own CSV files through a simple interface.

The system supports generating different types of graphs like bar charts, line charts, scatter plots, heatmaps, pie charts, histograms, and boxplots.

After graph generation, the system can send the graph along with sample data to Gemini AI to get insights automatically or in response to custom queries.

The project is built with FastAPI for the backend and uses libraries like Pandas, Matplotlib, and Seaborn for data handling and visualization.

Gemini 1.5 Pro is used to analyze the graphs and provide textual insights including anomalies, trends, and questions for further exploration.

Technologies Used

FastAPI and Uvicorn for the backend server

Pandas and NumPy for data processing

Matplotlib and Seaborn for data visualization

Google Generative AI (Gemini 1.5 Pro) for generating insights

Streamlit for the optional user interface

Requests, UUID, OS modules for utility purposes

Installation Steps

Clone the repository to your local machine using Git.

Open the project in VS Code or any code editor.

(Optional but recommended) Set up a virtual environment.

Install required Python libraries using pip.

Add your Gemini API key in the backend code where indicated.

Run the backend server using the command uvicorn main:app --reload --port 8050.

If a Streamlit frontend is included, you can start it using streamlit run app.py.

Project Structure

static/uploads: Folder where uploaded CSV files are stored.

static/graphs: Folder where generated graph images are saved.

main.py: FastAPI backend that handles all core functionality.

app.py: Optional Streamlit frontend for easier interaction.

requirements.txt: Contains all the dependencies used in the project.

README.md: This file.

How It Works

The user starts by uploading a CSV file.

Once uploaded, the system reads the data and extracts available columns.

The user then selects a type of graph and the relevant columns.

A graph is generated and stored in the static folder.

The system sends the image and sample data to Gemini AI.

Gemini analyzes the image and data, then responds with insights.

The insights are shown to the user, including any patterns, anomalies, or suggestions.

Future Improvements

Deployment to platforms like Render, Railway, or AWS.

Allow users to compare multiple graphs at once.

Make the backend accessible publicly through services like Ngrok.

Add more advanced filtering and interactivity in the frontend.

About the Author

This project was created by Shivanjali Belge, an engineering student passionate about AI, data visualization, and full-stack development. Connect on LinkedIn: https://www.linkedin.com/in/shivanjali-belge-839547258
