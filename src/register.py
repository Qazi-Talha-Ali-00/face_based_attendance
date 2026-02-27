from initialize import app, collection

def register_student(image_path: str, roll_number: str, name: str):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = app.get(img)
    
    if len(faces) == 0:
        print(f"No face detected for {name}")
        return False
    if len(faces) > 1:
        print(f"Multiple faces detected — use a solo photo for registration")
        return False
    
    embedding = faces[0].embedding  # 512-d ArcFace vector
    embedding = embedding / np.linalg.norm(embedding)  # normalize before storing
    
    collection.add(
        embeddings=[embedding.tolist()],
        ids=[roll_number],                          # roll number as unique ID
        metadatas=[{"name": name, "roll": roll_number}]
    )
    
    print(f"Registered {name} ({roll_number}) successfully")
    return True

# Usage
#register_student("john_photo.jpg", "CS2021001", "John Doe")