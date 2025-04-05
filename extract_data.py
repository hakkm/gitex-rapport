import os
from google import genai
from google.genai import types

def extract_data(location="global"):
    """
    Extract data about air quality, mobility infrastructure, energy consumption,
    and renewable energy using the Gemini API.

    Args:
        location (str): The region, city, or country to focus on. Default is "global".

    Returns:
        dict: Extracted environmental data
    """
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""
                Please provide structured data about {location} for:
                1. Air quality indices for major cities in {location}
                2. Mobility infrastructure statistics (public transit, bike lanes, EV charging) in {location}
                3. Energy consumption patterns by sector in {location}
                4. Renewable energy adoption rates in {location}

                Format the data in a structured way that can be easily parsed.
                """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,  # Lower temperature for more factual responses
        response_mime_type="text/plain",
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    # Process and structure the response
    # In a real application, you might want to parse this into a more structured format
    environmental_data = {
        "air_quality": {},
        "mobility_infrastructure": {},
        "energy_consumption": {},
        "renewable_energy": {},
        "raw_response": response.text
    }

    # Here you could add additional parsing logic to structure the data
    # For now, returning the raw response and an empty structure

    return environmental_data

def main():
    """
    Main function to demonstrate the extract_data functionality
    """
    location = input("Enter a location (city, country, or region) for environmental data (press Enter for global data): ")
    location = location.strip() or "global"

    print(f"Extracting environmental data for {location} using Gemini API...")
    env_data = extract_data(location)

    print("\n---ENVIRONMENTAL DATA SUMMARY---\n")
    print("Raw Response from Gemini:")
    print(env_data["raw_response"])

    # You could add more processing or display logic here
    print("\nData categories available:")
    for category in env_data.keys():
        if category != "raw_response":
            print(f"- {category}")

if __name__ == "__main__":
    main()
