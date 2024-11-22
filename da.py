import numpy as np

P_Fever = 0.6
P_Cough_given_Fever = {True: 0.85, False: 0.3}
P_Fatigue_given_Fever = {True: 0.75, False: 0.4}
P_Flu_given_Fever_Cough_Fatigue = {
    (True, True, True): 0.95,
    (True, True, False): 0.85,
    (True, False, True): 0.8,
    (True, False, False): 0.7,
    (False, True, True): 0.5,
    (False, True, False): 0.3,
    (False, False, True): 0.2,
    (False, False, False): 0.05,
}

def simulate_patient_diagnosis(num_samples=10_000):
    flu_when_fever = 0
    fever_occurrences = 0

    for _ in range(num_samples):
        has_fever = np.random.rand() < P_Fever

        has_cough = np.random.rand() < P_Cough_given_Fever[has_fever]
        has_fatigue = np.random.rand() < P_Fatigue_given_Fever[has_fever]

        has_flu = np.random.rand() < P_Flu_given_Fever_Cough_Fatigue[(has_fever, has_cough, has_fatigue)]

        if has_fever:
            fever_occurrences += 1
            if has_flu:
                flu_when_fever += 1

    if fever_occurrences == 0:
        return 0.0

    return flu_when_fever / fever_occurrences

estimated_probability = simulate_patient_diagnosis()
print(f"Estimated Probability of Flu Given Fever: {estimated_probability:.4f}")
