Here is your complete Markdown document for sharing with teammates and other LLMs:

---

# AI-Powered NGO Civic Issue Routing System

## Competitive AI-Assisted Assignment Model (Hackathon Architecture)

---

## 📌 Project Overview

We are building an **AI-powered civic issue routing platform** that connects citizens to NGOs instead of government departments.

The system uses **Gemini API** to intelligently suggest the most relevant NGOs and implements a **competitive acceptance model** to improve response time and accountability.

---



# 🧠 System Flow

1. User submits:

   * Issue description
   * Image (optional)
   * Location (area/pincode)

2. Node.js sends issue data to FastAPI.

3. FastAPI:

   * Calls Gemini API
   * Extracts category & severity
   * Requests Top 3 NGO suggestions (from provided list)

4. Gemini returns ranked NGOs.

5. Node.js validates suggestions:

   * NGO exists
   * NGO operates in area
   * NGO has available capacity

6. System sends request to Top 3 NGOs.

7. First NGO to accept → Gets assignment.

8. Deadline timer starts.

9. If not completed before deadline → Automatically passed to next NGO.

---

# 🤖 Role of Gemini API

Gemini is used ONLY for:

* Issue classification
* Severity scoring
* Ranking top 3 NGOs from provided list
* Generating reasoning/explanation

Gemini does NOT:

* Write to database
* Finalize assignment
* Control workflow
* Handle deadlines

Final decisions remain deterministic.

---

# 📥 Input to FastAPI

```json
{
  "issue_text": "Water pipe burst near school, urgent help needed",
  "location": "Kothrud",
  "pincode": "411038",
  "image_url": "optional"
}
```

---

# 📤 Expected Output from FastAPI

```json
{
  "category": "Water Infrastructure",
  "severity": "High",
  "impact_score": 8.7,
  "suggested_ngos": [
    "CleanWater Foundation",
    "Urban Relief NGO",
    "CommunityAid Trust"
  ],
  "reasoning": "Public safety risk near school. Immediate response recommended."
}
```

---

# 🔐 Controlled Gemini Prompt Strategy

We will provide Gemini with a **fixed NGO list** and instruct it to select ONLY from that list.

Example prompt structure:

```
Here is the list of NGOs:

1. CleanWater Foundation – Water – Kothrud
2. GreenCity NGO – Waste – All Pune
3. SafeWomen NGO – Women Safety – All Pune
4. AnimalCare – Animal Rescue – Kothrud

Based on the issue below, return the top 3 NGOs from the list ONLY by exact name.
Return response in JSON format.
```

This prevents hallucination and ensures controlled selection.

---

# 🤝 Competitive Acceptance Model

Instead of directly assigning one NGO:

* Top 3 NGOs are notified
* Status = "Awaiting Acceptance"
* First NGO to accept gets the assignment

This ensures:

* Faster response time
* Reduced bias
* Fair opportunity
* Accountability

---

# 🔒 Assignment Locking Logic

When NGO clicks "Accept":


UPDATE complaints
SET assigned_ngo = X
WHERE complaint_id = Y
AND status = "Awaiting Acceptance"


If rows affected = 1 → Assignment successful
If rows affected = 0 → Another NGO already accepted

Prevents double assignment.

---

# ⏳ Deadline & Escalation Logic

After assignment:

* Deadline timer starts (e.g., 48 hours)
* If NGO completes → Status = "Completed"
* If deadline exceeded:

  * Auto-assign to next NGO
  * Notify user

Simple timer-based logic is sufficient for prototype.

---

# 📊 Database Design (Simplified) (MongoDB)

## Complaints Table

* complaint_id
* issue_text
* location
* category
* severity
* status
* assigned_ngo
* deadline
* created_at

## NGOs Table

* ngo_id
* name
* supported_categories
* operating_areas
* capacity_limit
* active_cases

---

# ⚠ Fallback Logic

If Gemini API fails:

* Use keyword-based classification
* Select NGOs using deterministic matching
* Continue workflow without crashing

System must remain stable without AI.

---
