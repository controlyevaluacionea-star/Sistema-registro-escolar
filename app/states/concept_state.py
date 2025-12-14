import reflex as rx
from typing import TypedDict


class Concept(TypedDict):
    id: str
    name: str
    amount: float
    currency: str


class ConceptState(rx.State):
    concepts: list[Concept] = [
        {"id": "C001", "name": "Inscripción", "amount": 50.0, "currency": "USD ($)"},
        {"id": "C002", "name": "Seguro Escolar", "amount": 20.0, "currency": "USD ($)"},
        {
            "id": "C003",
            "name": "Mensualidad - Septiembre",
            "amount": 80.0,
            "currency": "USD ($)",
        },
        {
            "id": "C004",
            "name": "Mensualidad - Octubre",
            "amount": 80.0,
            "currency": "USD ($)",
        },
        {
            "id": "C005",
            "name": "Mensualidad - Noviembre",
            "amount": 80.0,
            "currency": "USD ($)",
        },
        {
            "id": "C006",
            "name": "Mensualidad - Diciembre",
            "amount": 80.0,
            "currency": "USD ($)",
        },
        {
            "id": "C007",
            "name": "Mensualidad - Enero",
            "amount": 85.0,
            "currency": "USD ($)",
        },
        {
            "id": "C008",
            "name": "Mensualidad - Febrero",
            "amount": 85.0,
            "currency": "USD ($)",
        },
        {
            "id": "C009",
            "name": "Mensualidad - Marzo",
            "amount": 85.0,
            "currency": "USD ($)",
        },
        {
            "id": "C010",
            "name": "Pago Extraordinario",
            "amount": 10.0,
            "currency": "USD ($)",
        },
    ]
    is_open: bool = False
    current_concept: dict = {}
    is_editing: bool = False

    @rx.event
    def open_add_dialog(self):
        self.current_concept = {}
        self.is_editing = False
        self.is_open = True

    @rx.event
    def open_edit_dialog(self, concept: Concept):
        self.current_concept = concept
        self.is_editing = True
        self.is_open = True

    @rx.event
    def close_dialog(self):
        self.is_open = False
        self.current_concept = {}

    @rx.event
    def save_concept(self, data: dict):
        name = data.get("name")
        amount = float(data.get("amount", 0))
        currency = data.get("currency")
        if not name or amount <= 0:
            return rx.toast.error("Datos inválidos")
        if self.is_editing:
            for i, c in enumerate(self.concepts):
                if c["id"] == self.current_concept["id"]:
                    self.concepts[i].update(
                        {"name": name, "amount": amount, "currency": currency}
                    )
                    break
            rx.toast.success("Concepto actualizado")
        else:
            new_id = f"C{len(self.concepts) + 1:03d}"
            self.concepts.append(
                {"id": new_id, "name": name, "amount": amount, "currency": currency}
            )
            rx.toast.success("Concepto creado")
        self.close_dialog()

    @rx.event
    def delete_concept(self, concept_id: str):
        self.concepts = [c for c in self.concepts if c["id"] != concept_id]
        rx.toast.info("Concepto eliminado")