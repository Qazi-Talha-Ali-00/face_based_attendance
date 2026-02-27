from initialize import register_student, mark_attendance

class AttendanceOrchestrator:

    def __init__(self):
        pass

    def register(self, image_path, roll, name):
        return register_student(image_path, roll, name)

    def mark(self, group_photo_path, threshold=0.45):
        return mark_attendance(group_photo_path, threshold)

    def run_pipeline(self, group_photo_path):
        attendance = self.mark(group_photo_path)

        print("\nFinal Attendance List:")
        for person in attendance:
            print(f"{person['name']} ({person['roll']})")

        return attendance