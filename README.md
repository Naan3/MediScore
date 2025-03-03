**MediScore Calculation**

**Purpose:**
The purpose of this project is to be able to assess patient health by implementing a Medi Score system
which is based on specific parameters such as:
  - Oxygen Dependency (Air or Supplemental Oxygen) - Enum
  - Level of Consciousness (Alert or CVPU) - Enum
  - Respiration rate - Int
  - Oxygen Saturation(SpO2) - Int
  - Temperature  - Float
  - Capillary Blood Glucose (CBG) - Float
  - Trend Monitoring for score increases - Tuples
These are what the system bases the score on.


**Thought Process & Design Choices**


**Input Handling and Validation**
  - Program asks the user for an input and makes sure the correct data types are being used
  - Made a function (get_valid_input()) that continuously makes sure the user provides a valid entry

    
**Medi Score Calculation**
  - Each parameter has a predefined scoring system
  - The score is based on input ranges, which are determined by conditional statements
  - The total score is calculated by summing up the individual component scores


**CBG**
  - Scoring depends whether or not the patient is fasting or has eaten in the last
    two hours
  - The scoring is then adjusted based on the status of fasting

    
**Tracking and Alerting for Trends**
  - Timestamps are used to maintain a history of past scores
  - The medi scores and timestamps are saved in a .txt file
  - Alert is triggered only when the patient's score increases by more than 2 points
    in 24 hours
  - The datetime module is imported to track the timestamps and figure out time differences

**Future Improvements**
  - In the future, I would like to have a feature where it asks for a patient's name
    and DOB so that it can track the specific patient.


