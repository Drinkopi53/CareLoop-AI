"""
Command Line Interface for CareLoopAI Clinic Chatbot
"""

import sys
from careloopai_clinic import CareLoopAIClinic

def main():
    clinic = CareLoopAIClinic()
    
    print("=== CareLoopAI Clinic Chatbot ===")
    print("Selamat datang di asisten kesehatan virtual kami!")
    print("Ketik 'bantuan' untuk melihat daftar perintah yang tersedia.")
    print("Ketik 'keluar' untuk mengakhiri sesi.\n")
    
    print(clinic.greet_patient())
    
    while True:
        try:
            user_input = input("\nAnda: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['keluar', 'exit', 'quit']:
                print("Bot: Terima kasih telah menggunakan CareLoopAI Clinic Chatbot. Semoga lekas sembuh!")
                break
            
            if user_input.lower() in ['bantuan', 'help']:
                print("\nBot: Perintah yang tersedia:")
                print("- laporkan gejala [gejala] - Laporkan gejala yang Anda alami")
                print("- checkin harian [kondisi] - Update kondisi harian Anda")
                print("- rencana pengobatan - Lihat rencana pengobatan Anda")
                print("- jadwal janji - Jadwalkan kunjungan ke klinik")
                print("- ringkasan - Lihat ringkasan kondisi Anda")
                print("- foto gejala - Kirim foto gejala (simulasi)")
                print("- bantuan - Tampilkan bantuan ini")
                print("- keluar - Akhiri sesi chat")
                continue
            
            # Process user input
            response = process_user_input(clinic, user_input)
            print(f"Bot: {response}")
            
        except KeyboardInterrupt:
            print("\n\nBot: Terima kasih telah menggunakan CareLoopAI Clinic Chatbot. Semoga lekas sembuh!")
            break
        except Exception as e:
            print(f"Bot: Maaf, terjadi kesalahan: {str(e)}")

def process_user_input(clinic, user_input):
    """Process user input and generate appropriate response"""
    lower_input = user_input.lower()
    
    # Registration
    if "nama saya" in lower_input:
        name = user_input.split("nama saya", 1)[1].strip()
        if name:
            return clinic.register_patient(name)
        else:
            return "Silakan beri tahu saya nama Anda dengan format: 'Nama saya [nama Anda]'"
    
    # Symptom reporting
    if "laporkan gejala" in lower_input or "gejala" in lower_input:
        # Extract symptoms (simplified)
        if "gejala" in lower_input:
            symptoms_text = lower_input.split("gejala", 1)[1].strip()
        else:
            symptoms_text = lower_input
        
        symptoms = [s.strip() for s in symptoms_text.split(",") if s.strip()]
        if symptoms:
            return clinic.report_symptoms(symptoms)
        else:
            return "Silakan laporkan gejala yang Anda alami, contoh: 'laporkan gejala demam, batuk, sakit kepala'"
    
    # Daily checkin
    if "checkin harian" in lower_input or "kondisi hari ini" in lower_input:
        # Extract condition description
        if "checkin harian" in lower_input:
            condition_text = lower_input.split("checkin harian", 1)[1].strip()
        else:
            condition_text = lower_input
        
        symptoms = [s.strip() for s in condition_text.split(",") if s.strip()]
        if symptoms:
            return clinic.daily_checkin(symptoms)
        else:
            return "Silakan update kondisi harian Anda, contoh: 'checkin harian batuk membaik, tidak demam'"
    
    # Treatment plan
    if "rencana pengobatan" in lower_input or "pengobatan" in lower_input:
        return clinic.get_treatment_plan()
    
    # Appointment scheduling
    if "jadwal janji" in lower_input or "janji temu" in lower_input:
        # In a real implementation, we would extract date/time
        return clinic.schedule_appointment("2023-06-15 10:00")
    
    # Patient summary
    if "ringkasan" in lower_input:
        return clinic.get_patient_summary()
    
    # Photo submission (simulated)
    if "foto" in lower_input:
        return clinic.process_symptom_photo("simulated_image.jpg")
    
    # Default response
    return ("Maaf, saya belum memahami permintaan Anda. "
            "Anda bisa mencoba perintah seperti:\n"
            "- 'Nama saya [nama Anda]'\n"
            "- 'laporkan gejala [gejala Anda]'\n"
            "- 'checkin harian [kondisi Anda]'\n"
            "- 'rencana pengobatan'\n"
            "- 'jadwal janji'\n"
            "- 'bantuan' untuk melihat semua perintah")

if __name__ == "__main__":
    main()