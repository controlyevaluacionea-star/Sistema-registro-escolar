import reflex as rx
from typing import TypedDict, Optional
import re


class Student(TypedDict):
    id: str
    name: str
    student_dni: str
    grade: str
    section: str
    representative: str
    representative_dni: str


class StudentState(rx.State):
    students: list[Student] = [
        {
            "id": "S001",
            "name": "Sofía Martínez",
            "student_dni": "V-12345678",
            "grade": "1er Grado",
            "section": "A",
            "representative": "Carlos Martínez",
            "representative_dni": "V-87654321",
        },
        {
            "id": "S002",
            "name": "Diego Rodríguez",
            "student_dni": "V-23456789",
            "grade": "2do Grado",
            "section": "B",
            "representative": "Ana Rodríguez",
            "representative_dni": "V-98765432",
        },
        {
            "id": "S003",
            "name": "Valentina López",
            "student_dni": "V-34567890",
            "grade": "3er Grado",
            "section": "A",
            "representative": "Juan López",
            "representative_dni": "E-11223344",
        },
        {
            "id": "S004",
            "name": "Alejandro García",
            "student_dni": "V-45678901",
            "grade": "Kinder",
            "section": "C",
            "representative": "Maria García",
            "representative_dni": "V-55667788",
        },
        {
            "id": "S005",
            "name": "Isabella Fernández",
            "student_dni": "V-56789012",
            "grade": "4to Grado",
            "section": "B",
            "representative": "Luis Fernández",
            "representative_dni": "V-99887766",
        },
    ]
    search_query: str = ""
    is_open: bool = False
    current_student: dict = {}
    is_editing: bool = False

    @rx.var
    def filtered_students(self) -> list[Student]:
        if not self.search_query:
            return self.students
        query = self.search_query.lower()
        return [
            s
            for s in self.students
            if query in s["name"].lower()
            or query in s["representative"].lower()
            or query in s.get("student_dni", "").lower()
            or (query in s.get("representative_dni", "").lower())
        ]

    @rx.event
    def set_search(self, query: str):
        self.search_query = query

    @rx.event
    def open_add_dialog(self):
        self.current_student = {}
        self.is_editing = False
        self.is_open = True

    @rx.event
    def open_edit_dialog(self, student: Student):
        self.current_student = student
        self.is_editing = True
        self.is_open = True

    @rx.event
    def close_dialog(self):
        self.is_open = False
        self.current_student = {}

    @rx.event
    def validate_dni(self, dni: str) -> bool:
        pattern = "^[VE]-\\d+$"
        return bool(re.match(pattern, dni))

    @rx.event
    def save_student(self, data: dict):
        student_dni = data.get("student_dni", "").strip().upper()
        representative_dni = data.get("representative_dni", "").strip().upper()
        if not self.validate_dni(student_dni):
            return rx.toast.error(
                "Cédula del estudiante inválida. Formato: V-12345678 o E-12345678"
            )
        if not self.validate_dni(representative_dni):
            return rx.toast.error(
                "Cédula del representante inválida. Formato: V-12345678 o E-12345678"
            )
        data["student_dni"] = student_dni
        data["representative_dni"] = representative_dni
        if self.is_editing:
            for i, s in enumerate(self.students):
                if s["id"] == self.current_student["id"]:
                    self.students[i].update(data)
                    break
            rx.toast.success("Estudiante actualizado correctamente")
        else:
            new_id = f"S{len(self.students) + 1:03d}"
            data["id"] = new_id
            self.students.append(data)
            rx.toast.success("Estudiante registrado correctamente")
        self.close_dialog()

    @rx.event
    def delete_student(self, student_id: str):
        self.students = [s for s in self.students if s["id"] != student_id]
        rx.toast.info("Estudiante eliminado")