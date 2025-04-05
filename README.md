# Environmental Analysis Dashboard

This project is a Streamlit-based dashboard that provides environmental data analytics using the Gemini API.
It displays simulated environmental metrics, trends, and generates detailed AI-based environmental analysis reports.

## Features
- **Simulated Metrics:** Air Quality, Energy Efficiency, Public Transit, and Renewable Energy Adoption.
- **Visualization:** Trend charts for key environmental metrics.
- **Report Generation:** Detailed environmental analysis using the Gemini API.
- **Download Options:** Download reports as plain text or create a Google Doc.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your `GEMINI_API_KEY` as an environment variable:
   ```bash
   export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```

## License
MIT License
