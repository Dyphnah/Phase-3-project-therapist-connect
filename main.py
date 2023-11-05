# CLI
# Bug- getting duplicte responses- still checking

from database import *

if __name__ == '__main__':
    therapist_db = TherapistDatabase('therapist.db')

    print("Welcome to Therapist Connect - Directory of Mental Health Professionals")

    therapist_db.populate_sample_data()

    while True:
        print("\n1. View all therapists\n2. Search for a therapist\n3. Review a therapist\n4. Exit")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice < 1 or choice > 4:
                raise ValueError
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 4.")
            continue

        if choice == 1:
            therapists = therapist_db.get_all_therapists()
            print("\nAll Therapists:")
            for therapist in therapists:
                print(therapist)

        elif choice == 2:
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

        elif choice == 3:
            therapist_id = input(
                "Enter the ID of the therapist you want to review: ")

            try:
                therapist_id = int(therapist_id)
            except ValueError:
                print("Invalid input. Therapist ID should be an integer.")
                continue

            rating = input("Enter your rating (0.0 - 5.0): ")
            try:
                rating = float(rating)
                if rating < 0.0 or rating > 5.0:
                    raise ValueError
            except ValueError:
                print("Invalid input. Rating should be a float between 0.0 and 5.0.")
                continue

            therapist_db.review_therapist(therapist_id, rating)

        elif choice == 4:
            break
