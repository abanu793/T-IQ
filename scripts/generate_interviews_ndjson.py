# generate_interviews_ndjson.py
# Generates synthetic interview transcripts in NDJSON (one JSON object per line).
# Output: C:\Users\abanu\Documents\T-IQ\data\raw\interview_transcripts_100.ndjson

import random
import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta

# Output path (Windows)
OUT_PATH = Path(
    r"C:\Users\abanu\Documents\T-IQ\data\raw\interview_transcripts_100.ndjson"
)
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

roles = [
    "Data Analyst",
    "Software Engineer",
    "HR Manager",
    "Product Manager",
    "Customer Support Executive",
    "Business Analyst",
    "QA Engineer",
    "Cloud Architect",
    "ML Engineer",
    "Marketing Specialist",
    "DevOps Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "UX Designer",
    "Security Engineer",
    "Data Engineer",
    "Recruiter",
    "Finance Analyst",
    "Sales Executive",
]

interviewers = [
    "Priya Rao",
    "Rohit Menon",
    "Anita Joseph",
    "Karthik Srinivasan",
    "Deepika Nair",
    "Naveen Krishnan",
    "Vishal Shetty",
    "Aparna Roy",
    "Harsha Reddy",
    "Sudeep Kumar",
    "Meena Iyer",
    "Sanjay Kulkarni",
    "Nidhi Sharma",
    "Amitabh Joshi",
    "Ritika Banerjee",
]

question_pool = [
    "Tell me about yourself.",
    "Why do you want this role?",
    "Describe a challenging project you worked on and how you solved it.",
    "How do you handle tight deadlines?",
    "What is your greatest strength?",
    "What is your biggest weakness?",
    "Where do you see yourself in 5 years?",
    "How do you handle conflict within a team?",
    "Tell me about a time you showed leadership.",
    "Why should we hire you?",
    "Explain a technical concept you used recently.",
    "How do you prioritize tasks?",
    "Describe your experience with {tech}.",
    "How do you ensure quality in your work?",
    "What metrics do you track for success?",
    "How do you keep up with industry trends?",
    "Explain a time you failed and what you learned.",
    "How do you approach debugging/troubleshooting?",
    "Give an example of cross-functional collaboration.",
    "Describe your experience with cloud platforms.",
    "How do you manage stakeholder expectations?",
    "What tools do you use for project management?",
    "How would you improve our product/process?",
    "Explain a machine learning concept you are familiar with.",
    "How do you ensure data privacy and security?",
    "Walk me through your resume.",
    "What is your approach to mentoring juniors?",
    "How do you conduct A/B testing?",
    "Describe experience with CI/CD pipelines.",
    "What questions do you have for us?",
]

tech_keywords = [
    "Python",
    "SQL",
    "Pandas",
    "TensorFlow",
    "PyTorch",
    "Docker",
    "Kubernetes",
    "AWS",
    "GCP",
    "Azure",
    "React",
    "Node.js",
    "Kafka",
    "Spark",
    "Airflow",
    "FastAPI",
    "REST",
    "GraphQL",
    "BERT",
    "scikit-learn",
]

modes = ["Online", "Onsite", "Phone"]


def gen_candidate_name():
    first = random.choice(
        [
            "Aarav",
            "Priya",
            "Rahul",
            "Sneha",
            "Ishika",
            "Arjun",
            "Nisha",
            "Kunal",
            "Meera",
            "Vikram",
            "Anika",
            "Rohit",
            "Sana",
            "Karan",
            "Divya",
            "Sameer",
            "Pooja",
            "Aman",
            "Rita",
            "Neha",
            "Siddharth",
            "Kavya",
            "Ananya",
            "Tarun",
            "Isha",
            "Kavitha",
            "Kiran",
            "Maya",
        ]
    )
    last = random.choice(
        [
            "Sharma",
            "Patel",
            "Kumar",
            "Iyer",
            "Verma",
            "Singh",
            "Gupta",
            "Reddy",
            "Nair",
            "Das",
            "Roy",
            "Mehta",
            "Joshi",
        ]
    )
    return f"{first} {last}"


def gen_summary(transcript):
    skills = set()
    for qa in transcript:
        for kw in tech_keywords:
            if (
                kw.lower() in qa["answer"].lower()
                or kw.lower() in qa["question"].lower()
            ):
                skills.add(kw)
    skills_list = list(skills)[:6]
    impression = random.choice(
        [
            "Strong technical skills and clear communicator.",
            "Good foundational knowledge with practical experience.",
            "Promising candidate but needs more production experience.",
            "Excellent communication and problem-solving abilities.",
        ]
    )
    return f"{impression} Skills noted: {', '.join(skills_list)}"


NUM = 100  # <-- number of interviews to generate

with OUT_PATH.open("w", encoding="utf-8") as fout:
    for i in range(1, NUM + 1):
        role = random.choice(roles)
        interviewer = random.choice(interviewers)
        mode = random.choice(modes)
        date = (datetime.now() - timedelta(days=random.randint(1, 365 * 3))).strftime(
            "%Y-%m-%d"
        )
        used_questions = random.sample(question_pool, 10)  # 10 Q&A per interview
        transcript = []
        for q in used_questions:
            if "{tech}" in q:
                q = q.replace("{tech}", random.choice(tech_keywords))
            base_answer = random.choice(
                [
                    "I've worked intensively on this and applied it in production.",
                    "I approach this by breaking the problem into smaller parts and validating each step.",
                    "I use best practices and automated testing to ensure reliability.",
                    "I collaborated with cross-functional teams and focused on measurable outcomes.",
                    "I used cloud services and containerization to deploy scalable solutions.",
                    "I collect metrics and iterate based on feedback from users and stakeholders.",
                ]
            )
            if random.random() < 0.5:
                base_answer += f" For example, I used {random.choice(tech_keywords)}."
            transcript.append({"question": q, "answer": base_answer})
        record = {
            "id": str(uuid.uuid4()),
            "candidate_name": gen_candidate_name(),
            "role": role,
            "round": random.choice(
                ["HR Round", "Technical Round 1", "Technical Round 2", "Manager Round"]
            ),
            "interviewer": interviewer,
            "mode": mode,
            "date": date,
            "transcript": transcript,
            "summary": gen_summary(transcript),
            "skill_tags": list(
                {
                    kw
                    for kw in tech_keywords
                    if any(
                        kw.lower() in (qa["answer"] + qa["question"]).lower()
                        for qa in transcript
                    )
                }
            )[:8],
        }
        fout.write(json.dumps(record, ensure_ascii=False) + "\n")

print("NDJSON written to:", OUT_PATH)
