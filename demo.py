"""
Demonstration script for CareLoopAI Clinic Chatbot
"""

from careloopai_clinic import CareLoopAIClinic

def main():
    print("=== CareLoopAI Clinic Chatbot Demo ===")
    print("Menunjukkan cara kerja chatbot dalam skenario nyata\n")
    
    # Create clinic instance
    clinic = CareLoopAIClinic()
    
    # 1. Greeting
    print("1. Greeting:")
    print("Bot:", clinic.greet_patient())
    print()
    
    # 2. Patient registration
    print("2. Registrasi Pasien:")
    print("Pasien: Nama saya Budi Santoso")
    response = clinic.register_patient("Budi Santoso", "08123456789")
    print("Bot:", response)
    print()
    
    # 3. Symptom reporting
    print("3. Pelaporan Gejala:")
    print("Pasien: Saya merasa demam, batuk, dan sakit kepala")
    symptoms = ["demam", "batuk", "sakit kepala"]
    response = clinic.report_symptoms(symptoms, "kepala", "sedang")
    print("Bot:", response)
    print()
    
    # 4. First follow-up
    print("4. Checkin Harian (Hari 1):")
    print("Pasien: Hari ini batuk saya membaik, tapi masih demam")
    symptoms = ["batuk membaik", "masih demam"]
    response = clinic.daily_checkin(symptoms, "dada", "sedang")
    print("Bot:", response)
    print()
    
    # 5. Second follow-up
    print("5. Checkin Harian (Hari 2):")
    print("Pasien: Kondisi saya membaik, tidak demam lagi")
    symptoms = ["membaik", "tidak demam"]
    response = clinic.daily_checkin(symptoms, "umum", "ringan")
    print("Bot:", response)
    print()
    
    # 6. Treatment plan request
    print("6. Permintaan Rencana Pengobatan:")
    print("Pasien: Apa rencana pengobatan saya sekarang?")
    response = clinic.get_treatment_plan()
    print("Bot:", response)
    print()
    
    # 7. Photo submission (simulated)
    print("7. Pengiriman Foto Gejala:")
    print("Pasien: Saya kirim foto kondisi tenggorokan saya")
    response = clinic.process_symptom_photo("tenggorokan_foto.jpg")
    print("Bot:", response)
    print()
    
    # 8. Patient summary
    print("8. Ringkasan Kondisi:")
    print("Pasien: Bisa beri ringkasan kondisi saya?")
    response = clinic.get_patient_summary()
    print("Bot:", response)
    print()
    
    # 9. Follow-up check
    print("9. Cek Kunjungan Ulang:")
    print("Pasien: Apakah saya perlu kontrol ulang?")
    response = clinic.check_followup_needed()
    print("Bot:", response)
    print()
    
    print("=== Demo selesai ===")
    print("\nDalam implementasi nyata, pasien akan menerima:")
    print("- Reminder harian untuk update kondisi")
    print("- Revisi rencana pengobatan otomatis")
    print("- Notifikasi jika kunjungan langsung diperlukan")
    print("- Pengurangan kunjungan ulang yang tidak perlu")

if __name__ == "__main__":
    main()