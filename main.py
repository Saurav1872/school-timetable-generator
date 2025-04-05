#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
School Timetable Generator

This program generates an optimal weekly timetable for a school based on 
classes, subjects, teachers, and period requirements.
"""

### DO NOT MODIFY THE CODE BELOW THIS LINE ###

# Define the input constraints
# Classes
classes = ["Class 6A", "Class 6B", "Class 7A", "Class 7B"]

# Subjects
subjects = ["Mathematics", "Science", "English", "Social Studies", "Computer Science", "Physical Education"]

# Weekly period requirements for each class and subject
# {class_name: {subject_name: number_of_periods_per_week}}
class_subject_periods = {
    "Class 6A": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 3, "Physical Education": 3},
    "Class 6B": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 3, "Physical Education": 3},
    "Class 7A": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 4, "Physical Education": 2},
    "Class 7B": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 4, "Physical Education": 2}
}

# Teachers and their teaching capabilities
# {teacher_name: [list_of_subjects_they_can_teach]}
teachers = {
    "Mr. Kumar": ["Mathematics"],
    "Mrs. Sharma": ["Mathematics"],
    "Ms. Gupta": ["Science"],
    "Mr. Singh": ["Science", "Social Studies"],
    "Mrs. Patel": ["English"],
    "Mr. Joshi": ["English", "Social Studies"],
    "Mr. Malhotra": ["Computer Science"],
    "Mr. Chauhan": ["Physical Education"]
}

# School timing configuration
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
periods_per_day = 6

### DO NOT MODIFY THE CODE ABOVE THIS LINE ###

def generate_timetable():
    """
    Generate a weekly timetable for the school based on the given constraints.
    
    Returns:
        dict: A data structure representing the complete timetable
              Format: {day: {period: {class: (subject, teacher)}}}
    """
    timetable = {day: {period: {} for period in range(1, periods_per_day + 1)} for day in days_of_week}

    remaining_periods = {class: subjects.copy() for class, subjects in class_subject_periods.items()}

    teacher_availability = {day: {period: set(teachers.keys()) for period in range(1, periods_per_day + 1)} for day in days_of_week}

    for day in days_of_week:
        for period in range(1, periods_per_day + 1):
            for class in classes:
                for subject, count in list(remaining_periods[class].items()):
                    if count > 0:
                        for teacher, teachable_subjects in teachers.items():
                            if subject in teachable_subjects and teacher in teacher_availability[day][period]:
                                timetable[day][period][class] = (subject, teacher)
                                remaining_periods[class][subject] -= 1
                                teacher_availability[day][period].remove(teacher)
                                break
                        break

    return timetable


def display_timetable(timetable):
    """
    Display the generated timetable in a readable format.
    
    Args:
        timetable (dict): The generated timetable
    """
    print("\nSchool Timetable:")
    for day, periods in timetable.items():
        print(f"\n{day}:")
        for period, classes in periods.items():
            print(f"  Period {period}:")
            for class, (subject, teacher) in classes.items():
                print(f"    {class}: {subject} (Teacher: {teacher})")


def validate_timetable(timetable):
    """
    Validate that the generated timetable meets all constraints.
    
    Args:
        timetable (dict): The generated timetable
        
    Returns:
        bool: True if timetable is valid, False otherwise
        str: Error message if timetable is invalid
    """
    class_subject_count = {class: {subject: 0 for subject in subjects} for class in classes}
    for day, periods in timetable.items():
        for period, classes in periods.items():
            for class, (subject, teacher) in classes.items():
                class_subject_count[class][subject] += 1

    for class, subject_counts in class_subject_periods.items():
        for subject, required_count in subject_counts.items():
            if class_subject_count[class][subject] != required_count:
                return False, f"{class} - {subject} failed to make"

    for day, periods in timetable.items():
        for period, classes in periods.items():
            teacher_set = set()
            for _, (_, teacher) in classes.items():
                if teacher in teacher_set:
                    return False, f"Teacher {teacher} {day}, period {period} - repetitive assignment"
                teacher_set.add(teacher)

    for day, periods in timetable.items():
        for period, classes in periods.items():
            for _, (subject, teacher) in classes.items():
                if subject not in teachers[teacher]:
                    return False, f"Teacher {teacher} - {subject} : teacher cannot teach this subject"

    return True, "Timetable is valid"


def main():
    """
    Main function to generate and display the timetable.
    """
    print("Generating school timetable...")
    
    # Generate the timetable
    timetable = generate_timetable()

    # Validate the timetable
    is_valid, message = validate_timetable(timetable)
    
    if is_valid:
        # Display the timetable
        display_timetable(timetable)
    else:
        print(f"Failed to generate valid timetable: {message}")


if __name__ == "__main__":
    main()
