"""
Patient Data Management System
This module handles patient data storage and retrieval for the clinic chatbot.
"""

import json
import datetime
from typing import Dict, List, Optional

class PatientDataManager:
    def __init__(self, data_file: str = "patient_data.json"):
        self.data_file = data_file
        self.patients = self.load_data()
    
    def load_data(self) -> Dict:
        """Load patient data from file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_data(self) -> None:
        """Save patient data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.patients, f, indent=2, default=str)
    
    def register_patient(self, name: str, phone: str = "", email: str = "") -> None:
        """Register a new patient"""
        self.patients[name] = {
            "personal_info": {
                "name": name,
                "phone": phone,
                "email": email,
                "registration_date": datetime.datetime.now().isoformat()
            },
            "symptoms_history": [],
            "treatment_plans": [],
            "checkin_history": [],
            "appointments": []
        }
        self.save_data()
    
    def add_symptom_report(self, patient_name: str, symptoms: List[str], 
                          body_part: str = "", severity: str = "sedang") -> None:
        """Add a symptom report for a patient"""
        if patient_name not in self.patients:
            self.register_patient(patient_name)
        
        symptom_entry = {
            "date": datetime.datetime.now().isoformat(),
            "symptoms": symptoms,
            "body_part": body_part,
            "severity": severity
        }
        
        self.patients[patient_name]["symptoms_history"].append(symptom_entry)
        self.save_data()
    
    def generate_treatment_plan(self, patient_name: str, symptoms: List[str], 
                               body_part: str = "", severity: str = "sedang") -> str:
        """Generate a treatment plan based on symptoms"""
        # This is a simplified example - in a real system, this would be more complex
        plan = f"Rencana pengobatan untuk {patient_name}:\n"
        
        if "demam" in symptoms or "flu" in symptoms:
            plan += "1. Istirahat yang cukup (minimal 8 jam tidur per hari)\n"
            plan += "2. Minum air putih minimal 2-3 liter per hari\n"
            plan += "3. Konsumsi paracetamol jika suhu tubuh >38.5°C\n"
            
        if "batuk" in symptoms or "pilek" in symptoms:
            plan += "4. Gunakan obat batuk sesuai anjuran apoteker\n"
            plan += "5. Perbanyak makanan bergizi untuk meningkatkan imun\n"
            
        if "sakit kepala" in symptoms:
            plan += "6. Kompres hangat pada area dahi dan pelipis\n"
            plan += "7. Hindari paparan cahaya terang dan kebisingan\n"
            
        if "diare" in symptoms:
            plan += "8. Atur pola makan dengan makanan lunak dan bergizi\n"
            plan += "9. Hindari makanan pedas, berlemak, dan minuman berkafein\n"
            
        if "mual" in symptoms or "muntah" in symptoms:
            plan += "10. Makan dalam porsi kecil tapi sering\n"
            plan += "11. Hindari makanan berat dan berlemak\n"
            
        # Add general recommendations
        plan += "\nUmum:\n"
        plan += "- Jangan memaksakan aktivitas berat\n"
        plan += "- Monitor kondisi setiap hari dan laporkan perubahan\n"
        plan += "- Jika gejala memburuk dalam 2-3 hari, segera kunjungi klinik\n"
        
        # Save the treatment plan
        treatment_entry = {
            "date": datetime.datetime.now().isoformat(),
            "plan": plan,
            "based_on_symptoms": symptoms,
            "body_part": body_part,
            "severity": severity
        }
        
        self.patients[patient_name]["treatment_plans"].append(treatment_entry)
        self.save_data()
        
        return plan
    
    def revise_treatment_plan(self, patient_name: str, symptoms: List[str], 
                             body_part: str = "", severity: str = "sedang") -> str:
        """Revise treatment plan based on patient progress"""
        if patient_name not in self.patients or not self.patients[patient_name]["treatment_plans"]:
            return self.generate_treatment_plan(patient_name, symptoms, body_part, severity)
        
        # Get the latest treatment plan
        latest_plan = self.patients[patient_name]["treatment_plans"][-1]["plan"]
        
        # Check if symptoms are improving
        if severity == "ringan" or "membaik" in symptoms:
            revised_plan = latest_plan + "\n\nUpdate: Kondisi membaik, lanjutkan pengobatan sesuai rencana."
        elif severity == "berat" or "memburuk" in symptoms:
            revised_plan = latest_plan + "\n\nUpdate: Kondisi memburuk, pertimbangkan kunjungan langsung ke klinik."
        else:
            revised_plan = latest_plan + "\n\nUpdate: Kondisi stabil, lanjutkan pengobatan."
        
        # Save the revised treatment plan
        treatment_entry = {
            "date": datetime.datetime.now().isoformat(),
            "plan": revised_plan,
            "based_on_symptoms": symptoms,
            "body_part": body_part,
            "severity": severity,
            "revision_of": len(self.patients[patient_name]["treatment_plans"]) - 1
        }
        
        self.patients[patient_name]["treatment_plans"].append(treatment_entry)
        self.save_data()
        
        return revised_plan
    
    def add_daily_checkin(self, patient_name: str, symptoms: List[str], 
                         body_part: str = "", severity: str = "sedang") -> None:
        """Add a daily checkin entry for a patient"""
        if patient_name not in self.patients:
            self.register_patient(patient_name)
        
        checkin_entry = {
            "date": datetime.datetime.now().isoformat(),
            "symptoms": symptoms,
            "body_part": body_part,
            "severity": severity
        }
        
        self.patients[patient_name]["checkin_history"].append(checkin_entry)
        self.save_data()
    
    def schedule_appointment(self, patient_name: str, date_time: str, 
                           reason: str = "Perlu pemeriksaan langsung") -> str:
        """Schedule an appointment for a patient"""
        if patient_name not in self.patients:
            self.register_patient(patient_name)
        
        appointment = {
            "date_time": date_time,
            "reason": reason,
            "status": "scheduled",
            "created_date": datetime.datetime.now().isoformat()
        }
        
        self.patients[patient_name]["appointments"].append(appointment)
        self.save_data()
        
        return f"Kunjungan Anda telah dijadwalkan untuk {date_time}."
    
    def get_patient_data(self, patient_name: str) -> Optional[Dict]:
        """Get all data for a specific patient"""
        return self.patients.get(patient_name)
    
    def get_latest_treatment_plan(self, patient_name: str) -> Optional[str]:
        """Get the latest treatment plan for a patient"""
        if patient_name in self.patients and self.patients[patient_name]["treatment_plans"]:
            return self.patients[patient_name]["treatment_plans"][-1]["plan"]
        return None
    
    def get_symptom_history(self, patient_name: str, days: int = 7) -> List[Dict]:
        """Get symptom history for a patient for the last N days"""
        if patient_name not in self.patients:
            return []
        
        history = self.patients[patient_name]["symptoms_history"]
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        recent_history = [
            entry for entry in history 
            if datetime.datetime.fromisoformat(entry["date"]) > cutoff_date
        ]
        
        return recent_history

# Example usage
if __name__ == "__main__":
    # Create a patient data manager
    pdm = PatientDataManager()
    
    # Register a patient
    pdm.register_patient("Budi Santoso", "08123456789", "budi@email.com")
    
    # Add symptom report
    pdm.add_symptom_report("Budi Santoso", ["demam", "batuk", "sakit kepala"], "kepala", "sedang")
    
    # Generate treatment plan
    plan = pdm.generate_treatment_plan("Budi Santoso", ["demam", "batuk", "sakit kepala"], "kepala", "sedang")
    print("Treatment Plan:")
    print(plan)
    
    # Add daily checkin
    pdm.add_daily_checkin("Budi Santoso", ["batuk", "membaik"], "dada", "ringan")
    
    # Revise treatment plan
    revised_plan = pdm.revise_treatment_plan("Budi Santoso", ["batuk", "membaik"], "dada", "ringan")
    print("\nRevised Treatment Plan:")
    print(revised_plan)
    
    # Schedule appointment
    appointment = pdm.schedule_appointment("Budi Santoso", "2023-06-15 10:00", "Perlu pemeriksaan langsung")
    print("\nAppointment:")
    print(appointment)
    
    # Get patient data
    patient_data = pdm.get_patient_data("Budi Santoso")
    print("\nPatient Data:")
    print(json.dumps(patient_data, indent=2))