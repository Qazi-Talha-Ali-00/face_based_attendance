from initialize import app, collection

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