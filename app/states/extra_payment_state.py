import reflex as rx
from typing import TypedDict, Optional


class ExtraPayment(TypedDict):
    id: str
    name: str
    amount: float
    scope: str
    target: str


class ExtraPaymentState(rx.State):
    extra_payments: list[ExtraPayment] = [
        {
            "id": "EP001",
            "name": "Bono Navideño",
            "amount": 20.0,
            "scope": "Global",
            "target": "",
        },
        {
            "id": "EP002",
            "name": "Guía 1er Grado",
            "amount": 15.0,
            "scope": "Grado",
            "target": "1er Grado",
        },
    ]
    is_open: bool = False
    current_payment: dict = {}
    is_editing: bool = False
    form_scope: str = "Global"

    @rx.event
    def set_form_scope(self, value: str):
        self.form_scope = value

    @rx.event
    def open_add_dialog(self):
        self.current_payment = {}
        self.form_scope = "Global"
        self.is_editing = False
        self.is_open = True

    @rx.event
    def open_edit_dialog(self, payment: ExtraPayment):
        self.current_payment = payment
        self.form_scope = payment["scope"]
        self.is_editing = True
        self.is_open = True

    @rx.event
    def close_dialog(self):
        self.is_open = False
        self.current_payment = {}

    @rx.event
    def save_extra_payment(self, data: dict):
        name = data.get("name")
        amount = float(data.get("amount", 0))
        scope = data.get("scope", "Global")
        target = data.get("target", "")
        if not name or amount <= 0:
            return rx.toast.error("Datos inválidos")
        if scope != "Global" and (not target):
            return rx.toast.error("Debe especificar el grado o sección")
        if self.is_editing:
            for i, p in enumerate(self.extra_payments):
                if p["id"] == self.current_payment["id"]:
                    self.extra_payments[i].update(
                        {
                            "name": name,
                            "amount": amount,
                            "scope": scope,
                            "target": target,
                        }
                    )
                    break
            rx.toast.success("Pago extraordinario actualizado")
        else:
            new_id = f"EP{len(self.extra_payments) + 1:03d}"
            self.extra_payments.append(
                {
                    "id": new_id,
                    "name": name,
                    "amount": amount,
                    "scope": scope,
                    "target": target,
                }
            )
            rx.toast.success("Pago extraordinario creado")
        self.close_dialog()

    @rx.event
    def delete_extra_payment(self, payment_id: str):
        self.extra_payments = [p for p in self.extra_payments if p["id"] != payment_id]
        rx.toast.info("Pago extraordinario eliminado")