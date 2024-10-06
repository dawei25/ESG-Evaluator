ESG Evaluator

Overview

ESG Evaluator is an AI-powered tool designed to assess and analyze Environmental, Social, and Governance (ESG) scores for companies. This project combines data collection from various sources, natural language processing for text analysis, and a user-friendly dashboard for visualizing ESG trends and comparisons.

Features

- Data pipeline for collecting information from SEC filings, news articles, and company websites
- NLP analysis for entity extraction, sentiment analysis, and ESG content classification
- Interactive dashboard for viewing and comparing ESG scores
- Customizable weighting for ESG components
- Historical ESG score trends
- RESTful API for accessing ESG data


Tech Stack

- Backend: Python (FastAPI, spaCy, Transformers, scikit-learn)
- Frontend: React with TypeScript
- Database: PostgreSQL
- Data Visualization: Recharts


Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- News API key (for fetching news articles)


Installation

1. Clone the repository:
git clone [https://github.com/yourusername/esg-evaluator.git](https://github.com/yourusername/esg-evaluator.git)
cd esg-evaluator
2. Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install Python dependencies:
pip install -r requirements.txt
4. Install Node.js dependencies:
npm install
5. Set up the PostgreSQL database:

1. Create a new database named `esg_evaluator`
2. Run the `database_setup.sql` script to create the necessary tables



6. Set up environment variables:

1. Copy the `.env.example` file to `.env`
2. Fill in the required values in the `.env` file





Usage

1. Start the FastAPI backend:
python app.py
2. In a separate terminal, start the React frontend:
npm start
3. Access the ESG Evaluator dashboard at [http://localhost:3000](http://localhost:3000)


Project Structure

- data_pipeline.py: Handles data collection from various sources
- nlp_analysis.py: Performs NLP tasks and ESG score calculations
- app.py: FastAPI backend server
- esg_dashboard.tsx: React component for the ESG dashboard
- database_setup.sql: SQL script for setting up the database schema


API Endpoints

- GET /api/companies: Retrieve a list of companies with their latest ESG scores
- GET /api/esg-trend/company_id: Retrieve historical ESG score trends for a specific company


Contributing

Contributions to the ESG Evaluator project are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with descriptive commit messages
4. Push your changes to your fork
5. Submit a pull request to the main repository


Please ensure that your code follows the project's coding standards and includes appropriate tests.

