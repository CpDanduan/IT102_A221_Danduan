def view_history():
    try:
        with open("transactions.txt", "r") as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        return []

""" 
######### Learning Signature ######### 
Programmed by: Cristian Paul P Danduan
Date Submitted: September 7, 2026
 
Program Description: This program is abour atm cli.
Reflection: I learned how to use a class.
 
AI Usage
[/] No AI Assistance - Completed independently without AI.
[ ] AI as Support Tool - Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner - Used AI to design, structure, or co-create significant code.
"""