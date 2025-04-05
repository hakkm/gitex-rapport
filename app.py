import streamlit as st
import os
import matplotlib.pyplot as plt
from extract_data import extract_data, generate_environmental_summary
from google import genai
from google.genai import types
import numpy as np
import pandas as pd
import time
import uuid
import webbrowser

# Set page configuration
st.set_page_config(
    page_title="Environmental Analysis Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Instantiate the client using API key from env vars
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash-lite"

# Title and Description
st.title("🌍 Environmental Analysis Dashboard")
st.markdown("""
This dashboard provides data on air quality, energy consumption, mobility infrastructure, and renewable energy
for any region in the world. Select a region and explore the environmental metrics.
""")

# Input Region
input_region = st.text_input("Enter a region (city, country, or continent):", "global")

# Simulate data for satisfaction levels (in a real app, this would come from actual data)
def get_simulated_metrics(region):
    # This is placeholder data - in a production app, you'd fetch real data
    np.random.seed(hash(region) % 10000)  # Ensures consistent random values for the same region

    metrics = {
        "Air Quality": int(np.random.normal(65, 15)),
        "Energy Efficiency": int(np.random.normal(70, 10)),
        "Public Transit": int(np.random.normal(60, 20)),
        "Renewable Energy Adoption": int(np.random.normal(55, 25)),
    }

    # Ensure values are between 0 and 100
    for key in metrics:
        metrics[key] = max(0, min(100, metrics[key]))

    return metrics

# Get simulated data for the selected region
if input_region:
    metrics = get_simulated_metrics(input_region)

    # Display satisfaction metrics
    st.subheader(f"Environmental Metrics for {input_region}")
    cols = st.columns(len(metrics))
    for i, (metric_name, value) in enumerate(metrics.items()):
        with cols[i]:
            st.metric(
                label=metric_name,
                value=f"{value}%",
                delta=f"{np.random.randint(-5, 6)}%" if value > 0 else None
            )

    # Visualization placeholder
    st.subheader("Environmental Trends")
    with st.expander("View Trends", expanded=True):
        # Create a simple chart showing simulated trend data
        fig, ax = plt.subplots(figsize=(10, 6))

        # Generate some fake historical data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        data = {}
        for metric in metrics:
            base_value = metrics[metric]
            # Generate a random trend with some correlation to the current value
            data[metric] = [max(0, min(100, int(base_value + np.random.normal(0, 10)))) for _ in range(len(months))]

        # Plot the data
        for metric, values in data.items():
            ax.plot(months, values, marker='o', linewidth=2, label=metric)

        ax.set_ylim(0, 100)
        ax.set_xlabel('Month')
        ax.set_ylabel('Score')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)

        # Display the chart in Streamlit
        st.pyplot(fig)

    # Create a placeholder for the summary that will be populated later
    summary_placeholder = st.empty()

    # Initial problems and recommendations (placeholder)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Initial Problems Identified")
        initial_problems = [
            f"Air quality issues in {input_region}" if metrics["Air Quality"] < 70 else "Air quality is generally good",
            f"Energy inefficiency in {input_region}" if metrics["Energy Efficiency"] < 70 else "Energy usage is relatively efficient",
            f"Limited public transit options" if metrics["Public Transit"] < 70 else "Public transit system is well-developed",
            f"Low renewable energy adoption" if metrics["Renewable Energy Adoption"] < 70 else "Good progress in renewable energy adoption"
        ]
        for problem in initial_problems:
            st.markdown(f"- {problem}")

    with col2:
        st.subheader("Initial Recommendations")
        initial_recommendations = [
            "Implement stricter emission controls" if metrics["Air Quality"] < 70 else "Maintain current air quality standards",
            "Invest in energy-efficient technologies" if metrics["Energy Efficiency"] < 70 else "Continue energy efficiency initiatives",
            "Expand public transportation network" if metrics["Public Transit"] < 70 else "Optimize current transit system",
            "Increase incentives for renewable energy" if metrics["Renewable Energy Adoption"] < 70 else "Expand existing renewable programs"
        ]
        for recommendation in initial_recommendations:
            st.markdown(f"- {recommendation}")

    # Button to generate detailed report
    if st.button("Generate Detailed Environmental Report"):
        if input_region:
            with st.spinner(f"Analyzing environmental data for {input_region}..."):
                # Generate the prompt for the LLM
                prompt = f"""
                Generate a comprehensive environmental analysis report for {input_region} with the following sections:

                1. Summary: Provide a concise overview of the environmental state in {input_region}, focusing on:
                   - Air quality status (current score: {metrics['Air Quality']}%)
                   - Energy consumption and efficiency (current score: {metrics['Energy Efficiency']}%)
                   - Mobility infrastructure and public transit (current score: {metrics['Public Transit']}%)
                   - Renewable energy adoption (current score: {metrics['Renewable Energy Adoption']}%)

                2. Problems: Expand on these initial problems with detailed explanations:
                   {", ".join(initial_problems)}

                3. Recommendations: Provide actionable and specific recommendations to address the identified problems:
                   {", ".join(initial_recommendations)}

                Format the report with clear headings (### Summary, ### Problems, ### Recommendations).
                Be factual, specific, and provide actionable insights. Include statistics where relevant.
                """

                # Prepare content similar to test_genai.py and call generate_content
                contents = [
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=prompt)]
                    )
                ]
                generate_content_config = types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="text/plain",
                )

                response = client.models.generate_content(
                    model=MODEL,
                    contents=contents,
                    config=generate_content_config,
                )
                report_text = response.text

                # Parse the report into sections
                sections = {}
                current_section = None
                current_content = []

                for line in report_text.split('\n'):
                    if line.startswith('###'):
                        if current_section and current_content:
                            sections[current_section] = '\n'.join(current_content)
                            current_content = []
                        current_section = line.replace('###', '').strip()
                    elif current_section:
                        current_content.append(line)

                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)

                # Display the summary in the placeholder
                if 'Summary' in sections:
                    summary_placeholder.subheader("Environmental Summary")
                    summary_placeholder.markdown(sections['Summary'])

                # Display problems and recommendations
                if 'Problems' in sections or 'Recommendations' in sections:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Detailed Problems Analysis")
                        st.markdown(sections.get('Problems', 'No detailed problems analysis available'))
                    with col2:
                        st.subheader("Detailed Recommendations")
                        st.markdown(sections.get('Recommendations', 'No detailed recommendations available'))

                # Save the full report for download
                st.session_state.full_report = report_text

                # Create columns for download options
                download_col1, download_col2 = st.columns(2)

                with download_col1:
                    st.download_button(
                        label="Download as Text",
                        data=report_text,
                        file_name=f"environmental_report_{input_region.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )

                with download_col2:
                    # Generate a unique document ID
                    doc_id = str(uuid.uuid4())[:8]
                    doc_title = f"Environmental Report - {input_region} - {doc_id}"

                    if st.button("Create Google Doc", key="google_doc"):
                        try:
                            # Generate a shareable Google Docs link
                            # In a real app, you would use the Google Docs API here
                            google_docs_url = f"https://docs.new/?title={doc_title.replace(' ', '%20')}"

                            # Show success message with link
                            st.success(f"Google Doc created! Click below to open and paste the report.")

                            # Create a clickable link
                            st.markdown(f"[Open Google Doc]({google_docs_url})")

                            # Try to open the browser automatically
                            webbrowser.open(google_docs_url)
                        except Exception as e:
                            st.error(f"Error creating Google Doc: {e}")
                            st.info("You can manually create a Google Doc and copy the report text.")
        else:
            st.warning("Please enter a region before generating a report.")
else:
    st.info("Please enter a region to begin the analysis.")

# Footer
st.markdown("---")
st.caption("Environmental Analysis Dashboard | Powered by Gemini AI")
