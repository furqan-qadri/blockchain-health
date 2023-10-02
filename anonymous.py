import hashlib

# Define a function to anonymize patient data
def anonymize_patient_data(patient_data):
    # Anonymize sensitive fields such as name, phone number, and address
    anonymized_data = {
        "name": hash_data(patient_data["name"]),
        "sex": patient_data["sex"],
        "age": patient_data["age"],
        "phone": hash_data(patient_data["phone"]),
        "address": hash_data(patient_data["address"])
    }
    return anonymized_data

# Define a function to hash sensitive data
def hash_data(data):
    # Use a secure hash function (SHA-256) to anonymize data
    return hashlib.sha256(data.encode()).hexdigest()

# Example patient data retrieved from the smart contract
patient_data = {
    "name": "John Doe",
    "sex": "Male",
    "age": 30,
    "phone": "123-456-7890",
    "address": "123 Main Street"
}

# Anonymize the patient data
anonymized_data = anonymize_patient_data(patient_data)

# Print the anonymized data
print("Anonymized Patient Data:")
print(anonymized_data)
