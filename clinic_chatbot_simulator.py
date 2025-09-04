"""
CareLoopAI - Clinic Chatbot Simulator

This is a simple simulator to demonstrate the clinic chatbot functionality
without requiring Rasa to be installed.
"""

import json
import datetime

class ClinicChatbotSimulator:
    def __init__(self):
        self.patient_data = {}
        self.current_patient = None
        
    def greet(self):
        return "Halo! Selamat datang di klinik CareLoopAI. Saya asisten virtual Anda yang akan membantu memantau kondisi kesehatan Anda. Boleh tahu nama Anda?"
    
    def set_patient_name(self, name):
        self.current_patient = name
        if name not in self.patient_data:
            self.patient_data[name] = {
                "symptoms": [],
                "treatment_plan": "",
                "last_updated": ""
            }
        return f"Terima kasih, {name}. Sekarang, bolehkah Anda menjelaskan gejala yang Anda alami?"
    
    def report_symptoms(self, symptoms):
        if not self.current_patient:
            return "Maaf, saya belum tahu nama Anda. Boleh tahu nama Anda terlebih dahulu?"
        
        # Store symptoms
        self.patient_data[self.current_patient]["symptoms"] = symptoms
        self.patient_data[self.current_patient]["last_updated"] = datetime.datetime.now().isoformat()
        
        # Generate treatment plan
        treatment_plan = self.generate_treatment_plan(symptoms)
        self.patient_data[self.current_patient]["treatment_plan"] = treatment_plan
        
        return f"Berdasarkan gejala yang Anda alami, berikut rencana pengobatan:\n\n{treatment_plan}\n\nSaya akan mengirimkan update rencana pengobatan setiap hari berdasarkan laporan Anda."
    
    def generate_treatment_plan(self, symptoms):
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
    
    def daily_checkin(self, symptoms):
        if not self.current_patient:
            return "Maaf, saya belum tahu nama Anda. Boleh tahu nama Anda terlebih dahulu?"
        
        # Update symptoms
        self.patient_data[self.current_patient]["symptoms"] = symptoms
        self.patient_data[self.current_patient]["last_updated"] = datetime.datetime.now().isoformat()
        
        # Revise treatment plan
        current_plan = self.patient_data[self.current_patient]["treatment_plan"]
        revised_plan = self.revise_treatment_plan(current_plan, symptoms)
        self.patient_data[self.current_patient]["treatment_plan"] = revised_plan
        
        return f"Terima kasih atas update harian Anda. Berikut rencana pengobatan yang telah diperbarui:\n\n{revised_plan}\n\nBerdasarkan perkembangan Anda, kunjungan ulang ke klinik tidak diperlukan saat ini."
    
    def revise_treatment_plan(self, current_plan, symptoms):
        # Check if symptoms are improving
        if "membaik" in symptoms:
            revised_plan = current_plan + "\n\nUpdate: Kondisi membaik, lanjutkan pengobatan sesuai rencana."
        elif "memburuk" in symptoms:
            revised_plan = current_plan + "\n\nUpdate: Kondisi memburuk, pertimbangkan kunjungan langsung ke klinik."
        else:
            revised_plan = current_plan + "\n\nUpdate: Kondisi stabil, lanjutkan pengobatan."
            
        return revised_plan
    
    def ask_treatment(self):
        if not self.current_patient or self.current_patient not in self.patient_data:
            return "Maaf, saya belum memiliki data pengobatan Anda. Silakan laporkan gejala Anda terlebih dahulu."
        
        return f"Rencana pengobatan Anda saat ini:\n\n{self.patient_data[self.current_patient]['treatment_plan']}"
    
    def save_data(self, filename="patient_data.json"):
        with open(filename, 'w') as f:
            json.dump(self.patient_data, f, indent=2)
    
    def load_data(self, filename="patient_data.json"):
        try:
            with open(filename, 'r') as f:
                self.patient_data = json.load(f)
        except FileNotFoundError:
            self.patient_data = {}

def main():
    bot = ClinicChatbotSimulator()
    bot.load_data()
    
    print("=== CareLoopAI Clinic Chatbot Simulator ===")
    print("Ketik 'quit' untuk keluar\n")
    
    print(bot.greet())
    
    while True:
        user_input = input("\nAnda: ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        # Simple intent recognition
        if "halo" in user_input.lower() or "hai" in user_input.lower():
            print("Bot:", bot.greet())
        elif user_input.lower().startswith("nama saya"):
            name = user_input.split(" ", 2)[2] if len(user_input.split(" ")) > 2 else "Pasien"
            print("Bot:", bot.set_patient_name(name))
        elif "demam" in user_input.lower() or "batuk" in user_input.lower():
            symptoms = user_input.lower().split()
            print("Bot:", bot.report_symptoms(symptoms))
        elif "membaik" in user_input.lower() or "memburuk" in user_input.lower():
            symptoms = user_input.lower().split()
            print("Bot:", bot.daily_checkin(symptoms))
        elif "pengobatan" in user_input.lower():
            print("Bot:", bot.ask_treatment())
        else:
            print("Bot: Maaf, saya belum memahami permintaan Anda. Bisa jelaskan lagi?")
    
    # Save data before exiting
    bot.save_data()
    print("\nTerima kasih telah menggunakan CareLoopAI Clinic Chatbot!")

if __name__ == "__main__":
    main()