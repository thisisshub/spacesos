---

# **Generative AI Task Manager**  

🚀 **Goal:** Automate task prioritization and scheduling for users based on client interactions and real-time updates.  

---

## **📌 Features & Workflows**  

### **1️⃣ Task Prioritization & Scheduling**  
- Auto-generates **daily tasks** based on user behavior.  
- **Reminders** are created for events like birthdays & follow-ups.  
- Uses **Marvin AI** to summarize and prioritize tasks dynamically.  

### **2️⃣ AI-Powered Task Summarization**  
- Generates concise **task summaries & advisories** using OpenAI.  
- Tasks are categorized by priority (`HIGH`, `MEDIUM`, `LOW`).  
- Provides **recommendations** for financial advisors.  

### **3️⃣ Real-Time Task Updates**  
- Updating a task **automatically updates its reminder**.  
- Uses **Django signals** to detect task modifications.  

### **4️⃣ Authentication & Security**  
- Uses **JWT authentication** for secure user login.  
- **Predefined permissions** based on Django auth groups.  

---

## **🛠️ Technologies Used**  

| Tech Stack   | Purpose |
|-------------|---------|
| **Django REST Framework** | API backend |
| **PostgreSQL** | Database |
| **Supabase** | Cloud storage & authentication |
| **Marvin AI** | AI-based task summaries |
| **OpenAI API** | Natural Language Processing |
| **Google Cloud Functions** | Asynchronous task execution |
| **Structlog** | Logging middleware for debugging |

---

## **📁 Project File Structure**  

```
generative-ai-task-manager/
│── app/
│   ├── ai/                     # AI-related logic (task summarization)
│   │   ├── marvin_ai_agent.py   # Uses Marvin AI for prioritization
│   ├── tasks/                   # Task management logic
│   │   ├── models.py            # Task & Reminder models
│   │   ├── serializers.py       # Serializes tasks for APIs
│   │   ├── views.py             # Task API endpoints
│   ├── users/                   # Authentication & Permissions
│── config/                      # Django settings & configurations
│── requirements.txt             # Python dependencies
│── README.md                    # Project documentation
```

---

## **⚙️ Workflow Diagram**  

```mermaid
graph TD;
    A[User Creates Task] -->|Task Saved| B[Task Serializer];
    B --> C{Check Title for Date};
    C -- No Date Found --> D[Set Reminder for Next Day];
    C -- Date Found --> E[Extract Reminder Date];
    E --> F[Create Reminder];
    D --> F;
    F -->|Task + Reminder Stored| G[Update User Dashboard];
```

---

## **🔄 How the Project Works**  

### **1️⃣ Creating a Task**  
- User creates a new **task** via API (`POST /tasks/`).  
- System **extracts date** from the task title (if available).  
- If **no date is found**, a **default reminder** is set for the next day.  

### **2️⃣ Updating a Task**  
- Updating a task also updates the **associated reminder**.  
- **Structlog** logs all updates for debugging.  

### **3️⃣ AI-Powered Task Summaries**  
- **Marvin AI** generates **task summaries** and **priority advisories**.  
- Example response:  
  ```json
  {
    "priority": "HIGH",
    "title": "Call Bhavya today.",
    "summary": "The following tasks are scheduled for HIGH priority: Call Bhavya today.",
    "advisory": "You should do this before others."
  }
  ```

### **4️⃣ Authentication & Security**  
- **JWT Authentication** ensures **secure user login**.  
- **Superuser is created automatically** when a new database is initialized.  

---

## **🔧 Setup & Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/your-repo/generative-ai-task-manager.git
cd generative-ai-task-manager
```

### **2️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3️⃣ Setup Environment Variables**  
Create a `.env` file with:  
```env
DATABASE_URL=postgresql://postgres:yourpassword@db.supabase.co:5432/postgres
SECRET_KEY=your-secret-key
DEBUG=True
```

### **4️⃣ Run Migrations & Start Server**  
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## **📌 API Endpoints**  

| Method | Endpoint | Description |
|--------|---------|-------------|
| **POST** | `/tasks/` | Create a new task |
| **PATCH** | `/tasks/{id}/` | Update a task (also updates reminder) |
| **GET** | `/tasks/` | Retrieve tasks |
| **DELETE** | `/tasks/{id}/` | Delete a task |
| **GET** | `/reports/` | Generate AI-powered task reports |

---

## **📜 Logs & Debugging**  

Django uses **Structlog** for improved logging. Example log format:  
```bash
2025-02-14T07:02:26.119911Z [info] request_started request='POST /api/token/' user_agent=curl/8.7.1 user_id=None
```

---

## **🚀 Future Enhancements**  

✅ **Integrate AI for auto-task completion suggestions**  
✅ **Build a mobile-friendly UI for managing tasks**  
✅ **Enable voice-based task inputs**  

---

**🎯 Ready to build smarter task management? Let’s go!** 🚀