"""
Test suite for CareLoopAI Clinic Chatbot components
"""

import unittest
import json
import os
from careloopai_clinic import CareLoopAIClinic
from patient_data_manager import PatientDataManager
from image_processor import SymptomImageProcessor

class TestPatientDataManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_file = "test_patient_data.json"
        self.pdm = PatientDataManager(self.test_file)
        # Clear any existing data
        self.pdm.patients = {}
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_register_patient(self):
        """Test patient registration"""
        self.pdm.register_patient("Budi Santoso", "08123456789", "budi@email.com")
        self.assertIn("Budi Santoso", self.pdm.patients)
        self.assertEqual(self.pdm.patients["Budi Santoso"]["personal_info"]["phone"], "08123456789")
    
    def test_add_symptom_report(self):
        """Test adding symptom report"""
        self.pdm.register_patient("Budi Santoso")
        self.pdm.add_symptom_report("Budi Santoso", ["demam", "batuk"], "kepala", "sedang")
        
        history = self.pdm.patients["Budi Santoso"]["symptoms_history"]
        self.assertEqual(len(history), 1)
        self.assertIn("demam", history[0]["symptoms"])
    
    def test_generate_treatment_plan(self):
        """Test generating treatment plan"""
        self.pdm.register_patient("Budi Santoso")
        plan = self.pdm.generate_treatment_plan("Budi Santoso", ["demam", "batuk"], "kepala", "sedang")
        
        self.assertIn("Rencana pengobatan untuk Budi Santoso", plan)
        self.assertIn("Istirahat yang cukup", plan)
    
    def test_get_latest_treatment_plan(self):
        """Test getting latest treatment plan"""
        self.pdm.register_patient("Budi Santoso")
        plan1 = self.pdm.generate_treatment_plan("Budi Santoso", ["demam"], "kepala", "sedang")
        plan2 = self.pdm.revise_treatment_plan("Budi Santoso", ["demam", "membaik"], "kepala", "ringan")
        
        latest_plan = self.pdm.get_latest_treatment_plan("Budi Santoso")
        self.assertEqual(latest_plan, plan2)

class TestSymptomImageProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = SymptomImageProcessor()
    
    def test_process_uploaded_image(self):
        """Test processing uploaded image"""
        result = self.processor.process_uploaded_image("sample_image.jpg")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("findings", result)
        self.assertIn("treatment_update", result)

class TestCareLoopAIClinic(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.clinic = CareLoopAIClinic()
        # Use a test data file
        self.clinic.patient_manager.data_file = "test_patient_data.json"
        self.clinic.patient_manager.patients = {}
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        if os.path.exists("test_patient_data.json"):
            os.remove("test_patient_data.json")
    
    def test_greet_patient(self):
        """Test greeting patient"""
        greeting = self.clinic.greet_patient()
        self.assertIn("Selamat datang di klinik CareLoopAI", greeting)
    
    def test_register_patient(self):
        """Test patient registration"""
        response = self.clinic.register_patient("Budi Santoso", "08123456789")
        self.assertIn("Terima kasih, Budi Santoso", response)
        self.assertEqual(self.clinic.current_patient, "Budi Santoso")
    
    def test_report_symptoms(self):
        """Test symptom reporting"""
        self.clinic.register_patient("Budi Santoso")
        response = self.clinic.report_symptoms(["demam", "batuk"], "kepala", "sedang")
        
        self.assertIn("Berdasarkan gejala yang Anda alami", response)
        self.assertIn("Rencana pengobatan", response)
    
    def test_daily_checkin(self):
        """Test daily checkin"""
        self.clinic.register_patient("Budi Santoso")
        # First report symptoms
        self.clinic.report_symptoms(["demam", "batuk"], "kepala", "sedang")
        # Then do daily checkin
        response = self.clinic.daily_checkin(["batuk", "membaik"], "dada", "ringan")
        
        self.assertIn("Terima kasih atas update harian Anda", response)
        self.assertIn("Update: Kondisi membaik", response)
    
    def test_get_treatment_plan(self):
        """Test getting treatment plan"""
        self.clinic.register_patient("Budi Santoso")
        self.clinic.report_symptoms(["demam", "batuk"], "kepala", "sedang")
        response = self.clinic.get_treatment_plan()
        
        self.assertIn("Rencana pengobatan Anda saat ini", response)
        self.assertIn("Istirahat yang cukup", response)

def run_tests():
    """Run all tests"""
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add tests to the suite
    test_suite.addTest(unittest.makeSuite(TestPatientDataManager))
    test_suite.addTest(unittest.makeSuite(TestSymptomImageProcessor))
    test_suite.addTest(unittest.makeSuite(TestCareLoopAIClinic))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("Running tests for CareLoopAI Clinic Chatbot...")
    success = run_tests()
    if success:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")
        exit(1)