# Use an official Python image as a base
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Copy the MCP server script into the container
COPY mcp_weather.py .

# Install required dependencies
RUN pip install mcp aiohttp

# Expose the MCP server port
EXPOSE 8000

# Run the MCP server
CMD ["python", "mcp_weather.py"]
