from pyteal import *

# Define constants for keys and data types
patient_key = Bytes("patient")
disease_key = Bytes("disease")
medication_key = Bytes("medication")

# Define data structures for diseases and medications
disease_struct = {
    "name": str(""),
    "type": str(""),
    "code": Int(0),
    "days": Int(0)
}

medication_struct = {
    "name": str(""),
    "time": str(""),
    "type": str("")
}

# Define data structure for patient records
patient_struct = {
    "name": str(""),
    "sex": str(""),
    "age": Int(0),
    "phone": str(""),
    "address": str("")
}

# Define the main contract logic
def medical_records_contract():
    # Define state variables for storing patient records, diseases, and medications
    patient_data = App.localGet(Int(0), patient_key)
    diseases = App.localGet(Int(0), disease_key)
    medications = App.localGet(Int(0), medication_key)

    # Initialize contract state
    on_initialize = Seq([
        App.localPut(Int(0), patient_key, Int(0)),
        App.localPut(Int(0), disease_key, Array()),
        App.localPut(Int(0), medication_key, Array()),
        Return(Int(1))
    ])

    # Add a new patient record
    on_add_patient = Seq([
        App.localPut(Int(0), patient_key, Add(patient_data, Int(1))),
        Return(Int(1))
    ])

    # Function to add personal details of a patient with validation
    def add_patient_details(name, sex, age, phone, address):
        on_valid_input = Seq([
            Assert(name.Length() > Int(0)),  # Name should not be empty
            Assert(InSet(sex, ["Male", "Female", "Other"])),  # Sex should be one of the allowed values
            Assert(age >= Int(0)),  # Age should be non-negative
            Assert(phone.Length() == Int(10)),  # Phone number should be 10 digits
            App.localPut(Int(0), patient_key, Array.push(patient_data, {
                "name": name,
                "sex": sex,
                "age": age,
                "phone": phone,
                "address": address
            })),
            Return(Int(1))
        ])

        return Cond(
            [on_valid_input],
            [Else(), Return(Int(0))]
        )

    # Function to add a new disease record with validation
    def add_disease(name, type, code, days):
        on_valid_input = Seq([
            Assert(name.Length() > Int(0)),  # Name should not be empty
            Assert(type.Length() > Int(0)),  # Type should not be empty
            Assert(code > Int(0)),  # Code should be a positive integer
            Assert(days >= Int(0)),  # Days should be non-negative
            new_disease_data,
            App.localPut(Int(0), disease_key, Array.push(diseases, new_disease_data)),
            Return(Int(1))
        ])

        new_disease_data = {
            "name": name,
            "type": type,
            "code": code,
            "days": days
        }

        return Cond(
            [on_valid_input],
            [Else(), Return(Int(0))]
        )

    # Function to add a new medication record with validation
    def add_medication(name, time, type):
        on_valid_input = Seq([
            Assert(name.Length() > Int(0)),  # Name should not be empty
            Assert(time.Length() > Int(0)),  # Time should not be empty
            Assert(type.Length() > Int(0)),  # Type should not be empty
            new_medication_data,
            App.localPut(Int(0), medication_key, Array.push(medications, new_medication_data)),
            Return(Int(1))
        ])

        new_medication_data = {
            "name": name,
            "time": time,
            "type": type
        }

        return Cond(
            [on_valid_input],
            [Else(), Return(Int(0))]
        )

    # Search for patient data
    on_search_patient = Seq([
        Return(patient_data)
    ])

    # Search for disease records
    on_search_diseases = Seq([
        Return(diseases)
    ])

    # Search for medication records
    on_search_medications = Seq([
        Return(medications)
    ])

    return Cond(
        [Txn.application_id() == Int(0), on_initialize],
        [Txn.application_id() == Int(1), on_add_patient],
        [Txn.application_id() == Int(2), on_add_patient_details],
        [Txn.application_id() == Int(3), on_add_disease],
        [Txn.application_id() == Int(4), on_add_medication],
        [Txn.application_id() == Int(5), on_search_patient],
        [Txn.application_id() == Int(6), on_search_diseases],
        [Txn.application_id() == Int(7), on_search_medications],
        [Else(), Return(Int(0))]
    )

# Compile the smart contract
compiled_contract = compileTeal(medical_records_contract(), mode=Mode.Application)

# Print the compiled contract
print(compiled_contract)
