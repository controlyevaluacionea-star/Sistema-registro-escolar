import reflex as rx
from typing import TypedDict
import datetime


class PaymentEntry(TypedDict):
    id: str
    invoice_number: str
    student_id: str
    student_name: str
    concept: str
    amount: float
    currency: str
    method: str
    reference: str
    date: str
    timestamp: str


class PaymentState(rx.State):
    methods: list[str] = [
        "Efectivo",
        "Pago Móvil",
        "Transferencia Bancaria",
        "Zelle",
        "Punto de Venta",
    ]
    currencies: list[str] = ["USD ($)", "Bolívares (Bs)", "Euros (€)"]
    payments: list[PaymentEntry] = []
    form_concept: str = ""
    form_currency: str = "USD ($)"
    form_amount: str = ""
    form_method: str = "Efectivo"
    show_extra_payments: bool = False
    conversion_info: str = ""
    filtered_extra_payments: list[dict] = []

    @rx.event
    async def load_initial_data(self):
        from app.states.extra_payment_state import ExtraPaymentState

        extra_state = await self.get_state(ExtraPaymentState)
        self.filtered_extra_payments = [
            p for p in extra_state.extra_payments if p["scope"] == "Global"
        ]

    @rx.event
    async def select_student(self, student_id: str):
        from app.states.student_state import StudentState
        from app.states.extra_payment_state import ExtraPaymentState

        self.form_concept = ""
        self.form_amount = ""
        self.conversion_info = ""
        student_state = await self.get_state(StudentState)
        extra_state = await self.get_state(ExtraPaymentState)
        student = None
        for s in student_state.students:
            if s["id"] == student_id:
                student = s
                break
        filtered = []
        if student:
            for ep in extra_state.extra_payments:
                if ep["scope"] == "Global":
                    filtered.append(ep)
                elif ep["scope"] == "Grado":
                    if ep.get("target", "").lower() == student["grade"].lower():
                        filtered.append(ep)
                elif ep["scope"] == "Seccion":
                    if ep.get("target", "").lower() == student["section"].lower():
                        filtered.append(ep)
        self.filtered_extra_payments = filtered

    @rx.event
    def toggle_extra_payments(self):
        self.show_extra_payments = not self.show_extra_payments

    @rx.var
    def total_collected_usd(self) -> float:
        return sum((p["amount"] for p in self.payments if p["currency"] == "USD ($)"))

    @rx.var
    def total_collected_bs(self) -> float:
        return sum(
            (p["amount"] for p in self.payments if p["currency"] == "Bolívares (Bs)")
        )

    @rx.event
    def set_form_concept(self, value: str):
        self.form_concept = value
        yield PaymentState.calculate_amount

    @rx.event
    def set_form_currency(self, value: str):
        self.form_currency = value
        yield PaymentState.calculate_amount

    @rx.event
    def set_form_method(self, value: str):
        self.form_method = value
        if value in ["Pago Móvil", "Transferencia Bancaria", "Punto de Venta"]:
            self.form_currency = "Bolívares (Bs)"
        elif value in ["Zelle", "Efectivo USD"]:
            self.form_currency = "USD ($)"
        elif value == "Efectivo":
            pass
        yield PaymentState.calculate_amount

    @rx.event
    def set_form_amount(self, value: str):
        self.form_amount = value

    @rx.event
    async def calculate_amount(self):
        if not self.form_concept:
            self.conversion_info = ""
            return
        from app.states.concept_state import ConceptState
        from app.states.extra_payment_state import ExtraPaymentState
        from app.states.config_state import ConfigState

        concept_state = await self.get_state(ConceptState)
        extra_state = await self.get_state(ExtraPaymentState)
        config_state = await self.get_state(ConfigState)
        base_amount_usd = 0.0
        for c in concept_state.concepts:
            if c["name"] == self.form_concept:
                base_amount_usd = float(c["amount"])
                break
        if base_amount_usd == 0.0:
            for ep in extra_state.extra_payments:
                if ep["name"] == self.form_concept:
                    base_amount_usd = float(ep["amount"])
                    break
        if base_amount_usd == 0:
            self.conversion_info = ""
            return
        if self.form_currency == "Bolívares (Bs)":
            rate = config_state.active_rate
            if rate <= 0:
                self.form_amount = "0.00"
                self.conversion_info = "Error: Tasa de cambio no disponible"
            else:
                converted = base_amount_usd * rate
                self.form_amount = f"{converted:.2f}"
                self.conversion_info = f"Base: ${base_amount_usd:.2f} x {rate:.2f} Bs/$"
        else:
            self.form_amount = f"{base_amount_usd:.2f}"
            self.conversion_info = ""

    @rx.event
    async def handle_payment_submit(self, form_data: dict):
        from app.states.student_state import StudentState

        student_state = await self.get_state(StudentState)
        student_id = form_data.get("student_id")
        concept = form_data.get("concept")
        amount_str = form_data.get("amount")
        currency = form_data.get("currency")
        method = form_data.get("method")
        if not student_id or student_id == "":
            return rx.toast.warning("Por favor seleccione un estudiante.")
        if not concept or concept == "":
            return rx.toast.warning("Por favor seleccione un concepto de pago.")
        if not amount_str or float(amount_str) <= 0:
            return rx.toast.warning("El monto debe ser mayor a 0.")
        student_name = "Desconocido"
        for s in student_state.students:
            if s["id"] == student_id:
                student_name = s["name"]
                break
        invoice_number = f"FACT-{datetime.datetime.now().strftime('%Y%m')}-{len(self.payments) + 1:04d}"
        new_payment: PaymentEntry = {
            "id": f"PAY-{len(self.payments) + 1:04d}",
            "invoice_number": invoice_number,
            "student_id": student_id,
            "student_name": student_name,
            "concept": concept,
            "amount": float(amount_str),
            "currency": currency,
            "method": method,
            "reference": form_data.get("reference", ""),
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        }
        self.payments.insert(0, new_payment)
        return rx.toast.success(
            f"Pago registrado exitosamente. Factura: {invoice_number}"
        )

    @rx.event
    def delete_payment(self, payment_id: str):
        self.payments = [p for p in self.payments if p["id"] != payment_id]
        rx.toast.info("Pago eliminado del registro")