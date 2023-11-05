# CLI
#Bug- getting duplicte responses- still checking

from database import *

if __name__ == '__main__':
    therapist_db = TherapistDatabase('therapist.db')

    print("Welcome to Therapist Connect - Directory of Mental Health Professionals")

    therapist_db.populate_sample_data()

    while True:
        print("\n1. View all therapists\n2. Search for a therapist\n3. Review a therapist\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            therapists = therapist_db.get_all_therapists()
            print("\nAll Therapists:")
            for therapist in therapists:
                print(therapist)

        elif choice == '2':
            filter_option = input(
                "Choose a filter option (name, location, specialty, reviews): ")
            filter_value = input(
                f"Enter the {filter_option} you're looking for: ")
            therapists = therapist_db.filter_therapists(
                filter_option, filter_value)
            if therapists:
                print(
                    f"\nTherapists matching {filter_option} '{filter_value}':")
                for therapist in therapists:
                    print(therapist)
            else:
                print(
                    f"No therapists found with {filter_option} '{filter_value}'.")

        elif choice == '3':
            therapist_id = input(
                "Enter the ID of the therapist you want to review: ")
            rating = float(input("Enter your rating (0.0 - 5.0): "))
            therapist_db.review_therapist(therapist_id, rating)

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please select a valid option.")









