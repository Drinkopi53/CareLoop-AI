"""
Setup script for CareLoopAI Clinic Chatbot
"""

import os
import subprocess
import sys

def create_directories():
    """Create necessary directories for the project"""
    directories = [
        "data",
        "data/nlu",
        "data/stories",
        "data/rules",
        "actions",
        "models",
        "results"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print("Please install dependencies manually using: pip install -r requirements.txt")

def initialize_rasa():
    """Initialize Rasa project (if Rasa is installed)"""
    try:
        # Check if Rasa is installed
        subprocess.check_call([sys.executable, "-c", "import rasa; print('Rasa is installed')"])
        
        # Initialize Rasa project
        print("Initializing Rasa project...")
        subprocess.check_call(["rasa", "init", "--no-prompt"])
        print("Rasa project initialized successfully!")
    except subprocess.CalledProcessError:
        print("Rasa is not installed or initialization failed. You can initialize manually later with: rasa init")

def create_sample_data():
    """Create sample patient data file"""
    sample_data = {
        "patients": {},
        "treatment_plans": {},
        "appointments": {}
    }
    
    with open("patient_data.json", "w") as f:
        import json
        json.dump(sample_data, f, indent=2)
    
    print("Created sample patient data file")

def main():
    print("Setting up CareLoopAI Clinic Chatbot...")
    
    # Create directories
    create_directories()
    
    # Create sample data
    create_sample_data()
    
    # Install dependencies
    install_dependencies()
    
    # Initialize Rasa (if possible)
    initialize_rasa()
    
    print("\nSetup complete!")
    print("\nTo run the CLI chatbot, use:")
    print("  python cli_chatbot.py")
    
    print("\nTo run the web interface, open:")
    print("  clinic_chatbot.html")
    
    print("\nTo train the Rasa model (after installing Rasa):")
    print("  rasa train")
    
    print("\nTo run the Rasa chatbot:")
    print("  rasa shell")

if __name__ == "__main__":
    main()