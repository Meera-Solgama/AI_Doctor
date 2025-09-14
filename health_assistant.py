# health_assistant.py

import datetime

class Symptom:
    def __init__(self, name, severity, duration):
        self.name = name
        self.severity = severity
        self.duration = duration


class HealthAssistant:
    def __init__(self, location):
        self.location = location
        self.medications = []

    def analyze_symptoms(self, symptoms):
        return {
            "emergency": False,
            "message": "No emergency detected.",
            "recommendation": "Drink water and rest.",
            "conditions": [{"condition": "Mild fever", "confidence": 0.75}],
            "recommended_doctors": [
                {"name": "Dr. Meera", "specialty": "General Physician", "rating": 4.5,
                 "distance_km": 2.3, "contact": "123-456-7890"}
            ]
        }

    def get_health_trends(self, metric, days):
        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(days)]
        values = list(range(1, days+1))
        return {
            "latest": values[-1],
            "metric": "units",
            "average": sum(values) / len(values),
            "minimum": min(values),
            "maximum": max(values),
            "trend": "increasing",
            "timeline": {"dates": dates, "values": values}
        }

    def get_medication_reminders(self):
        return [{"message": "Take Paracetamol 500mg", "last_taken": "8:00 AM"}]

    def record_medication_taken(self, name):
        print(f"Medication {name} recorded as taken.")

    def add_medication(self, name, dosage, frequency, days_supply):
        med = type("Medication", (), {})()
        med.name, med.dosage, med.frequency = name, dosage, frequency
        self.medications.append(med)
        return med

    def send_emergency_alert(self, msg):
        print("🚨 Emergency Alert Sent:", msg)


class HealthAssistantCLI:
    pass

