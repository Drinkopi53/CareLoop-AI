from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime
import json
import os

# File to store patient data
PATIENT_DATA_FILE = "patient_data.json"

def load_patient_data():
    """Load patient data from file"""
    if os.path.exists(PATIENT_DATA_FILE):
        with open(PATIENT_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_patient_data(data):
    """Save patient data to file"""
    with open(PATIENT_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class ActionGenerateTreatmentPlan(Action):
    """Action to generate initial treatment plan based on symptoms"""

    def name(self) -> Text:
        return "action_generate_treatment_plan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get patient information
        patient_name = tracker.get_slot("patient_name")
        symptoms = tracker.get_slot("symptoms") or []
        body_part = tracker.get_slot("body_part")
        severity = tracker.get_slot("severity")
        
        # Create treatment plan based on symptoms
        treatment_plan = self._create_treatment_plan(symptoms, body_part, severity)
        
        # Save patient data
        patient_data = load_patient_data()
        patient_data[patient_name] = {
            "symptoms": symptoms,
            "body_part": body_part,
            "severity": severity,
            "treatment_plan": treatment_plan,
            "last_updated": datetime.datetime.now().isoformat()
        }
        save_patient_data(patient_data)
        
        # Set the treatment plan slot
        return [SlotSet("treatment_plan", treatment_plan)]

    def _create_treatment_plan(self, symptoms, body_part, severity):
        """Create a treatment plan based on symptoms"""
        # This is a simplified example - in a real system, this would be more complex
        plan = "Rencana pengobatan awal:\n"
        
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
        
        return plan

class ActionReviseTreatmentPlan(Action):
    """Action to revise treatment plan based on daily checkins"""

    def name(self) -> Text:
        return "action_revise_treatment_plan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get patient information
        patient_name = tracker.get_slot("patient_name")
        symptoms = tracker.get_slot("symptoms") or []
        body_part = tracker.get_slot("body_part")
        severity = tracker.get_slot("severity")
        
        # Load existing patient data
        patient_data = load_patient_data()
        
        if patient_name in patient_data:
            # Update patient data with latest symptoms
            patient_data[patient_name].update({
                "symptoms": symptoms,
                "body_part": body_part,
                "severity": severity,
                "last_updated": datetime.datetime.now().isoformat()
            })
            
            # Revise treatment plan
            current_plan = patient_data[patient_name]["treatment_plan"]
            revised_plan = self._revise_treatment_plan(
                current_plan, 
                symptoms, 
                body_part, 
                severity,
                patient_data[patient_name]
            )
            
            # Update treatment plan
            patient_data[patient_name]["treatment_plan"] = revised_plan
            save_patient_data(patient_data)
            
            # Set the treatment plan slot
            return [SlotSet("treatment_plan", revised_plan)]
        else:
            # Create new treatment plan if patient not found
            treatment_plan = self._create_initial_plan(symptoms, body_part, severity)
            patient_data[patient_name] = {
                "symptoms": symptoms,
                "body_part": body_part,
                "severity": severity,
                "treatment_plan": treatment_plan,
                "last_updated": datetime.datetime.now().isoformat()
            }
            save_patient_data(patient_data)
            return [SlotSet("treatment_plan", treatment_plan)]

    def _create_initial_plan(self, symptoms, body_part, severity):
        """Create initial treatment plan"""
        plan = "Rencana pengobatan:\n"
        
        if any(s in symptoms for s in ["demam", "flu", "pilek"]):
            plan += "1. Istirahat cukup dan minum air putih banyak\n"
            
        if "batuk" in symptoms:
            plan += "2. Gunakan obat batuk sesuai dosis\n"
            
        if "sakit kepala" in symptoms:
            plan += "3. Kompres hangat dan hindari kebisingan\n"
            
        if "mual" in symptoms:
            plan += "4. Makan dalam porsi kecil dan sering\n"
            
        plan += "\nLaporkan kondisi harian Anda untuk penyesuaian rencana pengobatan."
        return plan

    def _revise_treatment_plan(self, current_plan, symptoms, body_part, severity, patient_history):
        """Revise treatment plan based on patient progress"""
        # This is a simplified example - in a real system, this would be more complex
        revised_plan = current_plan
        
        # Check if symptoms are improving
        if severity == "ringan" or "membaik" in symptoms:
            revised_plan += "\n\nUpdate: Kondisi membaik, lanjutkan pengobatan sesuai rencana."
        elif severity == "berat" or "memburuk" in symptoms:
            revised_plan += "\n\nUpdate: Kondisi memburuk, pertimbangkan kunjungan langsung ke klinik."
        else:
            revised_plan += "\n\nUpdate: Kondisi stabil, lanjutkan pengobatan."
            
        return revised_plan

class ActionProcessSymptomPhoto(Action):
    """Action to process symptom photos (placeholder implementation)"""

    def name(self) -> Text:
        return "action_process_symptom_photo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # In a real implementation, this would process the image
        # For now, we'll just provide a generic response
        dispatcher.utter_message(
            text="Terima kasih atas foto yang Anda kirim. "
                 "Sistem kami sedang menganalisis gambar untuk mengidentifikasi gejala. "
                 "Rencana pengobatan akan diperbarui berdasarkan temuan ini."
        )
        
        # Generate a treatment plan based on common symptoms
        treatment_plan = (
            "Rencana pengobatan berdasarkan analisis foto:\n"
            "1. Lanjutkan pengobatan sesuai rencana sebelumnya\n"
            "2. Monitor area yang terlihat pada foto setiap hari\n"
            "3. Jika ada perubahan warna, ukuran, atau rasa sakit meningkat, "
            "segera kunjungi klinik\n"
            "4. Tetap jaga kebersihan area yang terkena"
        )
        
        return [SlotSet("treatment_plan", treatment_plan)]

class ActionScheduleAppointment(Action):
    """Action to schedule an appointment"""

    def name(self) -> Text:
        return "action_schedule_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # In a real implementation, this would connect to a scheduling system
        dispatcher.utter_message(
            text="Kunjungan Anda telah dijadwalkan untuk besok pukul 10:00 pagi. "
                 "Silakan datang 15 menit sebelum waktu yang dijadwalkan. "
                 "Bawa kartu identitas dan riwayat pengobatan Anda."
        )
        
        return []

class ActionSendDailyCheckin(Action):
    """Action to send daily checkin reminder (placeholder)"""

    def name(self) -> Text:
        return "action_send_daily_checkin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # In a real implementation, this would send a message via SMS, email, or app notification
        dispatcher.utter_message(
            text="Halo! Ini reminder untuk update kondisi kesehatan Anda hari ini. "
                 "Bagaimana perasaan Anda? Apakah ada perubahan gejala?"
        )
        
        return []