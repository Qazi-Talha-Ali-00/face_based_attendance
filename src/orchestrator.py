from register import register_student
from mark_attendance import mark_attendance


class AttendanceOrchestrator:

    def __init__(self):
        """
        Orchestrator does not initialize models.
        That is already handled inside init.py.
        """
        pass

    # ---------------------------------------------

    def register(self, image_path, roll, name):
        return register_student(image_path, roll, name)

    # ---------------------------------------------

    def mark(self, group_photo_path, threshold=0.45):
        return mark_attendance(group_photo_path, threshold)

    # ---------------------------------------------

    def run_pipeline(self, group_photo_path):
        """
        High-level function for full attendance workflow
        """
        attendance = self.mark(group_photo_path)

        print("\nFinal Attendance List:")
        for person in attendance:
            print(f"{person['name']} ({person['roll']})")

        return attendance