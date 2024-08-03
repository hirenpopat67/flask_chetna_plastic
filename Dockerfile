FROM python:3.12.4

WORKDIR /chetnaplastic

# Command to install wkhtmltopdf (Convert HTML to PDF using in this app)
RUN apt-get update && apt-get install -y wkhtmltopdf

# Copy the requirements file first and install dependencies
COPY requirements.txt .

# Command to install python depedencies
RUN pip install -r requirements.txt --no-cache-dir

# copy project to working dir
COPY . /chetnaplastic


# Make port 2002 (Flask App) available to the world outside this container
# EXPOSE 2002