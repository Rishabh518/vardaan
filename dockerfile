#Use official python image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#Set the working directory in the container
WORKDIR /app

#Copy only requirements first to leverage Docker cache
COPY Requirements.txt .

#Install dependencies
RUN pip install --no-cache-dir -r Requirements.txt

#Copy the rest of your application code into the container
COPY . .

# Expose the port your Flask app runs on (default is 5000)
EXPOSE 5000

#Command to run the app
CMD ["python", "app.py"]
