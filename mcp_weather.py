import aiohttp
from mcp.server.fastmcp import FastMCP
from typing import Dict

# Initialize MCP server
mcp = FastMCP("WeatherService")

# Open-Meteo API (No API Key Required)
BASE_URL = "https://api.open-meteo.com/v1/forecast"

async def get_coordinates(city: str) -> Dict:
    """Fetch latitude and longitude for a given city using Open-Meteo."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return {"error": "City not found"}
            data = await response.json()
            if "results" not in data or not data["results"]:
                return {"error": "Invalid city name"}
            location = data["results"][0]
            return {"lat": location["latitude"], "lon": location["longitude"]}

@mcp.tool()
async def test_echo() -> Dict:
    return {"message": "Hello from WeatherService!"}

@mcp.tool()
async def get_weather(city: str) -> Dict:
    """Fetch current weather data for a given city."""
    coordinates = await get_coordinates(city)
    if "error" in coordinates:
        return coordinates  # Return error message if location lookup fails

    lat, lon = coordinates["lat"], coordinates["lon"]
    url = f"{BASE_URL}?latitude={lat}&longitude={lon}&current_weather=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return {"error": "Weather data unavailable"}
            data = await response.json()
            weather = data.get("current_weather", {})
            return {
                "city": city,
                "temperature": weather.get("temperature"),
                "wind_speed": weather.get("windspeed"),
                "condition": weather.get("weathercode")
            }

# Run the MCP server
if __name__ == "__main__":
    mcp.run()
