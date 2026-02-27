from orchestrator import AttendanceOrchestrator

# Create system
system = AttendanceOrchestrator()

# 1️⃣ Register a student (use a SOLO clear face image)
system.register("../photos/qazi.png", "B22CS087", "Qazi Talha Ali")
system.register("../photos/pari.png", "B22CS039", "Pari sharma")

system.register("../photos/chinmay.png", "B22BB001", "Chinmay Vashisth")
system.register("../photos/vignesh.png", "B22CS099", "Vignesh something something")


# def main():
#     print("Trying tp register students")
#     register_student("../photos/qazi.png", "B22CS087", "Qazi Talha Ali")
#     print("Qazi registered successfully")

#     register_student("../photos/pari.png", "B22CS039", "Pari sharma")
#     print("Pari registered successfully")
#     register_student("../photos/chinmay.png", "B22BB001", "Chinmay Vashisth")
#     print("Chinmay registered successfully")
#     register_student("../photos/vignesh.png", "B22CS099", "Vignesh something something")
#     print("Vignesh registered successfully")

#     print("\nTrying to mark attendance from group photo")
#     mark_attendance("../photos/group.png", 0.25)


# 2️⃣ Mark attendance from group photo
attendance = system.mark("../photos/group.png", 0.25)

print("\nReturned Attendance Data:")
print(attendance)