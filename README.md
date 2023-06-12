# Database Lecturer Expert System

![image](https://user-images.githubusercontent.com/63803360/121194572-700b2300-c8a1-11eb-8168-b53198546842.png)

This is a prototype of an expert system developed for WID2001 - Knowledge Representation and Reasoning. Our group decided to develop the expert system based on the course WIA2002 - Database.

The system was intended to be a web based system built using Flask with MongoDB as a database to store our extracted expert knowledge. However, due to lack of necessity, the current system stores said knowledge in a JSON file and imported into our main app file.

We applied expert system components into the system as described below:

1. Knowledge Base

- Our chosen knowledge representation technique was a rule-based representation.
- Hence, extracted knowledge from our domain expert was converted into rules and stored in the knowledge base.

2. Inference Engine

- We applied a forward chaining approach with deductive reasoning to generate conclusions based on the student's input.
- This is a data driven approach where the system collects input from the student to narrow down the possible conclusions until a final conclusion can be presented back to the student.

3. User Interface

## To Run

1. Run command `pip install requirements.txt`
2. Run `lecturer_es.py` and open the app locally.

## References

1. Redirecting to other URLs on button click
   - https://kanchanardj.medium.com/redirecting-to-another-page-with-button-click-in-python-flask-c112a2a2304c
