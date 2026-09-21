"""
LLM Provider Abstraction Service
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)

Provides a unified interface for LLM text generation supporting:
- MockLLMProvider (Default offline pattern-matching provider)
- OpenAIProvider (OpenAI API)
- AnthropicProvider (Anthropic Claude API)
- GeminiProvider (Google Gemini API)
"""

import json
import re
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.config import settings

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_sql_response(self, system_prompt: str, user_question: str) -> Dict[str, Any]:
        """Generates structured SQL response dict with generated_sql, reasoning_summary, tables_used."""
        pass

    @abstractmethod
    def generate_explanation(self, question: str, sql: str, columns: list, rows: list) -> str:
        """Generates conversational natural-language explanation of database results."""
        pass


class MockLLMProvider(BaseLLMProvider):
    """
    Offline pattern-matching LLM provider.
    Ensures 100% full application functionality without requiring external API keys.
    """
    def generate_sql_response(self, system_prompt: str, user_question: str) -> Dict[str, Any]:
        q = user_question.lower().strip()

        # Check if question is a direct destructive SQL command or contains forbidden statements
        if any(kw in q for kw in ["drop", "delete", "update", "insert", "alter", "truncate", "pragma", "create", "attach", "detach", "exec"]):
            return {
                "generated_sql": user_question,
                "reasoning_summary": "Passed input text directly to SQL safety validation engine.",
                "tables_used": []
            }

        if "top" in q and "cgpa" in q:
            limit_match = re.search(r'\b\d+\b', q)
            limit = limit_match.group(0) if limit_match else "5"
            return {
                "generated_sql": f"SELECT name, roll_number, cgpa FROM students ORDER BY cgpa DESC LIMIT {limit};",
                "reasoning_summary": f"Ordered students table by CGPA in descending order to retrieve top {limit} performers.",
                "tables_used": ["students"]
            }

        elif "how many students" in q or ("student" in q and "count" in q) or "number of students" in q:
            if "by department" in q or "each department" in q or "per department" in q:
                return {
                    "generated_sql": "SELECT d.name AS department_name, COUNT(s.id) AS student_count FROM departments d JOIN students s ON d.id = s.department_id GROUP BY d.name ORDER BY student_count DESC;",
                    "reasoning_summary": "Joined departments and students tables, grouped by department name to calculate student counts.",
                    "tables_used": ["departments", "students"]
                }
            elif "computer science" in q or "cs" in q:
                return {
                    "generated_sql": "SELECT COUNT(s.id) AS cs_student_count FROM students s JOIN departments d ON s.department_id = d.id WHERE d.name = 'Computer Science';",
                    "reasoning_summary": "Filtered students enrolled in the Computer Science department and counted records.",
                    "tables_used": ["students", "departments"]
                }
            elif "cyber security" in q or "csec" in q:
                return {
                    "generated_sql": "SELECT COUNT(s.id) AS csec_student_count FROM students s JOIN departments d ON s.department_id = d.id WHERE d.name = 'Cyber Security';",
                    "reasoning_summary": "Filtered students enrolled in Cyber Security and calculated count.",
                    "tables_used": ["students", "departments"]
                }
            else:
                return {
                    "generated_sql": "SELECT COUNT(*) AS total_students FROM students;",
                    "reasoning_summary": "Counted total number of student records in database.",
                    "tables_used": ["students"]
                }

        elif "most students" in q or "highest students" in q:
            return {
                "generated_sql": "SELECT d.name AS department_name, COUNT(s.id) AS student_count FROM departments d JOIN students s ON d.id = s.department_id GROUP BY d.name ORDER BY student_count DESC LIMIT 1;",
                "reasoning_summary": "Grouped students by department, sorted by count descending, and limited output to top 1 result.",
                "tables_used": ["departments", "students"]
            }

        elif "cgpa above" in q or "cgpa greater" in q or "cgpa >" in q:
            cutoff_match = re.search(r'\b\d+(\.\d+)?\b', q)
            cutoff = cutoff_match.group(0) if cutoff_match else "8.5"
            return {
                "generated_sql": f"SELECT name, roll_number, cgpa, semester FROM students WHERE cgpa > {cutoff} ORDER BY cgpa DESC;",
                "reasoning_summary": f"Filtered students table where CGPA exceeds {cutoff} threshold.",
                "tables_used": ["students"]
            }

        elif "average cgpa" in q or "avg cgpa" in q:
            if "by department" in q or "each department" in q:
                return {
                    "generated_sql": "SELECT d.name AS department_name, ROUND(AVG(s.cgpa), 2) AS average_cgpa FROM departments d JOIN students s ON d.id = s.department_id GROUP BY d.name ORDER BY average_cgpa DESC;",
                    "reasoning_summary": "Joined departments and students tables, calculated average CGPA grouped per department.",
                    "tables_used": ["departments", "students"]
                }
            else:
                return {
                    "generated_sql": "SELECT ROUND(AVG(cgpa), 2) AS overall_average_cgpa FROM students;",
                    "reasoning_summary": "Calculated overall average CGPA across all students.",
                    "tables_used": ["students"]
                }

        elif "courses" in q:
            if "cyber security" in q:
                return {
                    "generated_sql": "SELECT c.course_code, c.course_name, c.credits FROM courses c JOIN departments d ON c.department_id = d.id WHERE d.name = 'Cyber Security';",
                    "reasoning_summary": "Joined courses and departments tables to list courses offered by Cyber Security.",
                    "tables_used": ["courses", "departments"]
                }
            elif "computer science" in q:
                return {
                    "generated_sql": "SELECT c.course_code, c.course_name, c.credits FROM courses c JOIN departments d ON c.department_id = d.id WHERE d.name = 'Computer Science';",
                    "reasoning_summary": "Joined courses and departments tables to list courses offered by Computer Science.",
                    "tables_used": ["courses", "departments"]
                }
            elif "artificial intelligence" in q or "ai" in q:
                return {
                    "generated_sql": "SELECT c.course_code, c.course_name, c.credits FROM courses c JOIN departments d ON c.department_id = d.id WHERE d.name = 'Artificial Intelligence';",
                    "reasoning_summary": "Joined courses and departments tables to list courses offered by Artificial Intelligence.",
                    "tables_used": ["courses", "departments"]
                }
            else:
                return {
                    "generated_sql": "SELECT c.course_code, c.course_name, d.name AS department_name, c.credits FROM courses c JOIN departments d ON c.department_id = d.id;",
                    "reasoning_summary": "Retrieved list of all courses along with offering department names.",
                    "tables_used": ["courses", "departments"]
                }

        elif "enrolled in" in q or "enrollment" in q:
            if "artificial intelligence" in q or "ai" in q:
                return {
                    "generated_sql": "SELECT s.name AS student_name, s.roll_number, c.course_name, e.grade FROM students s JOIN enrollments e ON s.id = e.student_id JOIN courses c ON e.course_id = c.id WHERE c.course_name LIKE '%Artificial Intelligence%' OR c.course_code LIKE 'AI%';",
                    "reasoning_summary": "Joined students, enrollments, and courses tables to list students enrolled in AI courses.",
                    "tables_used": ["students", "enrollments", "courses"]
                }
            else:
                return {
                    "generated_sql": "SELECT s.name AS student_name, c.course_name, e.grade FROM students s JOIN enrollments e ON s.id = e.student_id JOIN courses c ON e.course_id = c.id LIMIT 10;",
                    "reasoning_summary": "Retrieved student course enrollment records.",
                    "tables_used": ["students", "enrollments", "courses"]
                }

        elif "faculty" in q or "professors" in q or "teachers" in q:
            return {
                "generated_sql": "SELECT f.name AS faculty_name, f.designation, d.name AS department_name FROM faculty f JOIN departments d ON f.department_id = d.id;",
                "reasoning_summary": "Joined faculty and departments tables to list faculty members and designations.",
                "tables_used": ["faculty", "departments"]
            }

        else:
            # General fallback query on students table
            return {
                "generated_sql": "SELECT name, roll_number, semester, cgpa FROM students LIMIT 5;",
                "reasoning_summary": "Generated default student summary query for general inquiry.",
                "tables_used": ["students"]
            }

    def generate_explanation(self, question: str, sql: str, columns: list, rows: list) -> str:
        row_count = len(rows)
        if row_count == 0:
            return "The database query executed successfully, but returned 0 matching records."

        if row_count == 1 and len(columns) == 1:
            val = rows[0][0]
            col_name = columns[0].replace("_", " ").title()
            return f"Based on the database records, the {col_name} is **{val}**."

        if "top" in question.lower():
            names = [f"{r[0]} (CGPA: {r[2]})" for r in rows[:3]] if len(columns) >= 3 else [str(r[0]) for r in rows[:3]]
            return f"The query returned the top records sorted by CGPA. Top candidates include: **{', '.join(names)}**."

        if "department" in question.lower() and ("count" in question.lower() or "most" in question.lower()):
            first_dept = rows[0][0]
            first_cnt = rows[0][1]
            return f"The department with the highest student count is **{first_dept}** with **{first_cnt}** registered students."

        return f"Successfully retrieved **{row_count}** record(s) matching your query from the university database."


class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        import httpx
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.httpx = httpx

    def generate_sql_response(self, system_prompt: str, user_question: str) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured in environment settings.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }
        response = self.httpx.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)

    def generate_explanation(self, question: str, sql: str, columns: list, rows: list) -> str:
        if not self.api_key:
            return f"Retrieved {len(rows)} record(s) matching your query."
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        prompt = f"User asked: '{question}'. Executed SQL: '{sql}'. Results: Columns: {columns}, Rows: {rows[:5]}. Provide a concise, clear 2-sentence conversational summary of this result."
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        try:
            response = self.httpx.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15.0)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            return f"Retrieved {len(rows)} record(s) matching your question."


class AnthropicProvider(BaseLLMProvider):
    def __init__(self):
        import httpx
        self.api_key = settings.ANTHROPIC_API_KEY
        self.model = settings.ANTHROPIC_MODEL
        self.httpx = httpx

    def generate_sql_response(self, system_prompt: str, user_question: str) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured in environment settings.")
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model,
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_question}]
        }
        response = self.httpx.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        content = response.json()["content"][0]["text"]
        
        # Extract JSON block
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return json.loads(content)

    def generate_explanation(self, question: str, sql: str, columns: list, rows: list) -> str:
        return f"Retrieved {len(rows)} record(s) matching your query."


class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        import httpx
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
        self.httpx = httpx

    def generate_sql_response(self, system_prompt: str, user_question: str) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured in environment settings.")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"{system_prompt}\n\nUser Question: {user_question}"}]}
            ]
        }
        response = self.httpx.post(url, json=payload, timeout=30.0)
        response.raise_for_status()
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return json.loads(text)

    def generate_explanation(self, question: str, sql: str, columns: list, rows: list) -> str:
        return f"Retrieved {len(rows)} record(s) matching your query."


def get_llm_provider() -> BaseLLMProvider:
    """Factory function to return configured LLM provider instance."""
    provider_name = settings.LLM_PROVIDER.upper().strip()

    if provider_name == "OPENAI" and settings.OPENAI_API_KEY:
        return OpenAIProvider()
    elif provider_name == "ANTHROPIC" and settings.ANTHROPIC_API_KEY:
        return AnthropicProvider()
    elif provider_name == "GEMINI" and settings.GEMINI_API_KEY:
        return GeminiProvider()
    else:
        # Fallback to Mock provider for zero-config / offline laboratory usage
        return MockLLMProvider()
