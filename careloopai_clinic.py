"""
Main Application for CareLoopAI Clinic Chatbot
This file integrates all components of the clinic chatbot system.
"""

import json
import datetime
from patient_data_manager import PatientDataManager
from image_processor import SymptomImageProcessor

class CareLoopAIClinic:
    def __init__(self):
        self.patient_manager = PatientDataManager()
        self.image_processor = SymptomImageProcessor()
        self.current_patient = None
    
    def greet_patient(self):
        """Greet the patient and ask for their name"""
        return "Halo! Selamat datang di klinik CareLoopAI. Saya asisten virtual Anda yang akan membantu memantau kondisi kesehatan Anda. Boleh tahu nama Anda?"
    
    def register_patient(self, name, phone="", email=""):
        """Register a new patient"""
        self.patient_manager.register_patient(name, phone, email)
        self.current_patient = name
        return f"Terima kasih, {name}. Sekarang, bolehkah Anda menjelaskan gejala yang Anda alami?"
    
    def report_symptoms(self, symptoms, body_part="", severity="sedang"):
        """Handle symptom reporting and generate initial treatment plan"""
        if not self.current_patient:
            return "Maaf, saya belum tahu nama Anda. Boleh tahu nama Anda terlebih dahulu?"
        
        # Add symptom report
        self.patient_manager.add_symptom_report(self.current_patient, symptoms, body_part, severity)
        
        # Generate treatment plan
        treatment_plan = self.patient_manager.generate_treatment_plan(
            self.current_patient, symptoms, body_part, severity
        )
        
        return f"Berdasarkan gejala yang Anda alami, berikut rencana pengobatan:\n\n{treatment_plan}\n\nSaya akan mengirimkan update rencana pengobatan setiap hari berdasarkan laporan Anda."
    
    def daily_checkin(self, symptoms, body_part="", severity="sedang"):
        """Handle daily checkin and revise treatment plan"""
        if not self.current_patient:
            return "Maaf, saya belum tahu nama Anda. Boleh tahu nama Anda terlebih dahulu?"
        
        # Add daily checkin
        self.patient_manager.add_daily_checkin(self.current_patient, symptoms, body_part, severity)
        
        # Revise treatment plan
        revised_plan = self.patient_manager.revise_treatment_plan(
            self.current_patient, symptoms, body_part, severity
        )
        
        return f"Terima kasih atas update harian Anda. Berikut rencana pengobatan yang telah diperbarui:\n\n{revised_plan}\n\nBerdasarkan perkembangan Anda, kunjungan ulang ke klinik tidak diperlukan saat ini."
    
    def process_symptom_photo(self, image_data):
        """Process a symptom photo and update treatment plan"""
        # Process the image
        result = self.image_processor.process_uploaded_image(image_data)
        
        # In a real implementation, we would extract symptoms from the result
        # and update the treatment plan accordingly
        symptoms = ["kemerahan", "pembengkakan"]  # Placeholder
        
        # Add to symptom history
        if self.current_patient:
            self.patient_manager.add_symptom_report(
                self.current_patient, symptoms, "area_terdampak", "sedang"
            )
        
        return (f"{result['message']}\n"
                f"Temuan: {result['findings']['kondisi']}\n"
                f"Update pengobatan: {result['treatment_update']}")
    
    def get_treatment_plan(self):
        """Get the current treatment plan for the patient"""
        if not self.current_patient:
            return "Maaf, saya belum tahu nama Anda. Boleh tahu nama Anda terlebih dahulu?"
        
        plan = self.patient_manager.get_latest_treatment_plan(self.current_patient)
        if plan:
            return f"Rencana pengobatan Anda saat ini:\n\n{plan}"
        else:
            return "Saya belum memiliki rencana pengobatan untuk Anda. Silakan laporkan gejala Anda terlebih dahulu."
    
    def schedule_appointment(self, date_time, reason="Perlu pemeriksaan langsung"):
        """Schedule an appointment for the patient"""
        if not self.current_patient:
            return "Maaf, saya belum tahu nama Anda. Boleh tahu nama Anda terlebih dahulu?"
        
        result = self.patient_manager.schedule_appointment(self.current_patient, date_time, reason)
        return f"{result} Silakan datang 15 menit sebelum waktu yang dijadwalkan. Bawa kartu identitas dan riwayat pengobatan Anda."
    
    def check_followup_needed(self):
        """Check if a follow-up visit is needed"""
        if not self.current_patient:
            return "Maaf, saya belum tahu nama Anda. Boleh tahu nama Anda terlebih dahulu?"
        
        # In a real implementation, this would analyze the patient's progress
        # For now, we'll return a generic response
        return "Berdasarkan perkembangan Anda, kunjungan ulang ke klinik tidak diperlukan saat ini. Rencana pengobatan telah diperbarui secara otomatis."
    
    def get_patient_summary(self):
        """Get a summary of the patient's condition and treatment"""
        if not self.current_patient:
            return "Maaf, saya belum tahu nama Anda. Boleh tahu nama Anda terlebih dahulu?"
        
        patient_data = self.patient_manager.get_patient_data(self.current_patient)
        if not patient_data:
            return "Data pasien tidak ditemukan."
        
        # Get latest treatment plan
        treatment_plan = self.patient_manager.get_latest_treatment_plan(self.current_patient)
        
        # Get recent symptom history
        symptom_history = self.patient_manager.get_symptom_history(self.current_patient, 7)
        
        summary = f"Ringkasan kondisi Anda, {self.current_patient}:\n\n"
        
        if treatment_plan:
            summary += f"Rencana Pengobatan:\n{treatment_plan[:200]}...\n\n"
        
        if symptom_history:
            summary += "Riwayat Gejala (7 hari terakhir):\n"
            for entry in symptom_history[-3:]:  # Show last 3 entries
                date = datetime.datetime.fromisoformat(entry['date']).strftime('%d %b %Y')
                symptoms = ', '.join(entry['symptoms'])
                summary += f"- {date}: {symptoms} ({entry['severity']})\n"
        
        return summary

# Example usage and testing
def main():
    clinic = CareLoopAIClinic()
    
    print("=== CareLoopAI Clinic Chatbot ===")
    print(clinic.greet_patient())
    
    # Register a patient
    print("\nBot:", clinic.register_patient("Budi Santoso", "08123456789"))
    
    # Report symptoms
    symptoms = ["demam", "batuk", "sakit kepala"]
    print("\nBot:", clinic.report_symptoms(symptoms, "kepala", "sedang"))
    
    # Daily checkin
    print("\nBot:", clinic.daily_checkin(["batuk", "membaik"], "dada", "ringan"))
    
    # Get treatment plan
    print("\nBot:", clinic.get_treatment_plan())
    
    # Process symptom photo (simulated)
    print("\nBot:", clinic.process_symptom_photo("sample_image.jpg"))
    
    # Get patient summary
    print("\nBot:", clinic.get_patient_summary())
    
    # Schedule appointment
    print("\nBot:", clinic.schedule_appointment("2023-06-15 10:00"))

if __name__ == "__main__":
    main()