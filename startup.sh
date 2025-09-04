#!/bin/bash
# Startup script for CareLoopAI Clinic Chatbot

echo "CareLoopAI Clinic Chatbot - Startup Options"
echo "=========================================="
echo "1. Run CLI Chatbot:         python cli_chatbot.py"
echo "2. Run Web Interface:       Open clinic_chatbot.html in your browser"
echo "3. Run Demo:                python demo.py"
echo "4. Run Tests:               python test_chatbot.py"
echo "5. Train Rasa Model:        rasa train (requires Rasa installation)"
echo "6. Run Rasa Shell:          rasa shell (requires Rasa installation)"
echo ""
echo "To install dependencies: pip install -r requirements.txt"
echo ""
echo "For development, you can also run individual components:"
echo "- Patient data management: python patient_data_manager.py"
echo "- Image processing:        python image_processor.py"
echo "- Core system:             python careloopai_clinic.py"