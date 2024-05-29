# #!/bin/bash
# Define terminal colors as variable
COLOR_PURPLE='\e[1;35m'
COLOR_YELLOW='\033[0;33m'
COLOR_RESET='\e[0m'

# Function to create and activate virtual enviroment on Linux
create_and_activate_venv_linux() {
  if [ -d ".venv" ]; then
    echo -e "${COLOR_YELLOW}Virtual environment already exists. Activating...${COLOR_NC}"
    source .venv/bin/activate
    echo "ambiente ativado"
  else
    echo -e "${COLOR_YELLOW}Creating virtual environment...${COLOR_NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    echo "ambiente ativado"
  fi
}

# Function to create and activate virtual enviroment on Windows
create_and_activate_venv_windows() {
  if [ -d ".venv "]; then
    echo -e "${COLOR_YELLOW}Virtual environment already exists. Activating...${COLOR_NC}"
    source .venv/Scripts/activate
  else
    echo -e "${COLOR_YELLOW}Creating virtual environment...${COLOR_NC}"
    python -m venv .venv
    source .venv/Scripts/activate
  fi
}

# Function to handle script exit gracefully
cleanup() {
  echo -e "${COLOR_YELLOW}\nExiting...${COLOR_RESET}"
  deactivate
  exit 0
}

# Trap (Ctrl+C) to run the cleaup function
trap cleanup SIGINT

# Function to check if the requiremnts are already installed
requirements_installed() {
  while read requirement; do
    if ! pip freeze | grep -q "$requirement"; then
      return 1
    fi
  done < requirements.txt
  return 0
}

# Ask the user for the framework
echo -e "${COLOR_PURPLE}Which framework would you like to use?${COLOR_RESET}"
echo "[0] - Django"
echo "[1] - Flask"
read framework

# Ask the user for the operating system
echo -e "\n${COLOR_PURPLE}Which operating system are you using?${COLOR_RESET}"
echo "[0] - Windows"
echo "[1] - Linux"
read os

# Create and activate virtual enviroment based on the os
echo -e "\nCreating .venv"
if [ "$os" == "1" ]; then
  create_and_activate_venv_linux
elif [ "$os" == "0" ]; then
  create_and_activate_venv_windows
else
  echo "Unsupported operating system."
  exit 1
fi

# Install the required packages from requirements.txt if it exists and if not already installed
if [ -f requirements.txt ]; then
  echo -e "${COLOR_PURPLE}Installing requirements...${COLOR_NC}"
  pip install -r requirements.txt -q -q -q --exists-action i
else
  echo "requirements.txt not found."
fi

# if [ -f requirements.txt ]; then
#   if requirements_installed; then
#     echo -e "${COLOR_PURPLE}All requirements are already installed.${COLOR_NC}"
#   else
#     echo -e "${COLOR_PURPLE}Installing requirements...${COLOR_NC}"
#     pip install -r requirements.txt
#   fi
# else
#   echo "requirements.txt not found."
# fi

# if [ -f requirements.txt ]; then
#   if requirements_installed; then
#     echo -e "${COLOR_YELLOW}All requirements are already installed.${COLOR_NC}\n"
#   else
#     echo "Quietly installing dependencies..."
#     pip install -r requirements.txt -q -q -q --exists-action i
#     echo -e "${COLOR_PURPLE}Dependencies fully installed${COLOR_RESET}\n"
#   fi
# else
#   echo "'requirements.txt' not found."
#   exit 1
# fi

# Initialize the project based on the framework
if [ "$framework" == "0" ]; then
  python manage.py runserver
elif [ "$framework" == "1" ]; then
  flask run
else
  echo "Unsupported framework."
  deactivate
  exit 1
fi

# Ensure cleanup is called if the script completes succesfully
cleanup