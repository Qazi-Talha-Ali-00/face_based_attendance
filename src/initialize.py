import insightface
import chromadb
import numpy as np
import cv2
from insightface.app import FaceAnalysis

# --- InsightFace setup ---
app = FaceAnalysis(name='buffalo_l')  # buffalo_l = best accuracy
app.prepare(ctx_id=0, det_size=(640, 640))  
# ctx_id=0 for GPU, ctx_id=-1 for CPU

# --- ChromaDB setup ---
chroma_client = chromadb.PersistentClient(path="./attendance_db")

collection = chroma_client.get_or_create_collection(
    name="students",
    metadata={"hnsw:space": "cosine"}  # cosine similarity for face embeddings
)

def register_student(image_path: str, roll_number: str, name: str):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = app.get(img)
    
    if len(faces) == 0:
        print(f"No face detected for {name}")
        return False
    
    # Pick the face with highest detection confidence
    best_face = max(faces, key=lambda f: f.det_score)
    
    print(f"Detected {len(faces)} face(s) — using best confidence: {best_face.det_score:.3f}")
    
    embedding = best_face.embedding  # 512-d ArcFace vector
    embedding = embedding / np.linalg.norm(embedding)
    
    collection.add(
        embeddings=[embedding.tolist()],
        ids=[roll_number],
        metadatas=[{"name": name, "roll": roll_number}]
    )
    
    print(f"Registered {name} ({roll_number}) successfully")
    return True
# Usage


def mark_attendance(group_photo_path: str, threshold: float = 0.45):
    img = cv2.imread(group_photo_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = app.get(img)
    print(f"Detected {len(faces)} faces in photo")
    
    attendance = []
    unrecognized = 0
    
    for face in faces:
        embedding = face.embedding
        embedding = embedding / np.linalg.norm(embedding)
        
        results = collection.query(
            query_embeddings=[embedding.tolist()],
            n_results=1
        )
        
        distance = results['distances'][0][0]
        similarity = 1 - distance  # chromadb cosine returns distance not similarity
        
        if similarity >= threshold:
            meta = results['metadatas'][0][0]
            attendance.append({
                "roll": meta['roll'],
                "name": meta['name'],
                "similarity": round(similarity, 3)
            })
        else:
            unrecognized += 1
    
    print(f"\nAttendance Marked: {len(attendance)} students")
    print(f"Unrecognized faces: {unrecognized}")
    
    for record in attendance:
        print(f"  ✓ {record['name']} ({record['roll']}) — confidence: {record['similarity']}")
    
    return attendance

def visualize_detections(group_photo_path: str, output_path: str = "detections.jpg"):
    img = cv2.imread(group_photo_path)
    faces = app.get(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    for i, face in enumerate(faces):
        box = face.bbox.astype(int)
        conf = face.det_score
        
        # Draw bounding box
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        
        # Label with face index and confidence
        label = f"#{i+1} {conf:.2f}"
        cv2.putText(img, label, (box[0], box[1] - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imwrite(output_path, img)
    print(f"Saved detection output to: {output_path} ({len(faces)} faces drawn)")


def main():
    # print("Trying tp register students")
    # register_student("../photos/qazi.png", "B22CS087", "Qazi Talha Ali")
    # print("Qazi registered successfully")

    # register_student("../photos/pari.png", "B22CS039", "Pari sharma")
    # print("Pari registered successfully")
    # register_student("../photos/chinmay.png", "B22BB001", "Chinmay Vashisth")
    # print("Chinmay registered successfully")
    # register_student("../photos/vignesh.png", "B22CS099", "Vignesh something something")
    # print("Vignesh registered successfully")

    print("\nTrying to mark attendance from group photo")
    mark_attendance("../photos/group.png", 0.25)
    print(visualize_detections("../photos/group.png", "group_detections.jpg"))

if __name__=='__main__':
    main()