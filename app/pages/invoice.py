import reflex as rx
from app.states.payment_state import PaymentState
from app.states.student_state import StudentState


class InvoiceState(rx.State):
    payment: dict = {}
    student: dict = {}
    company_name: str = "EduPay School System"
    company_rif: str = "J-12345678-9"
    company_address: str = "Av. Principal, Edificio Escolar, Caracas, Venezuela"
    company_phone: str = "+58 212 123-4567"

    @rx.event
    async def load_invoice(self):
        payment_id = self.router.page.params.get("payment_id")
        payment_state = await self.get_state(PaymentState)
        student_state = await self.get_state(StudentState)
        found_payment = None
        for p in payment_state.payments:
            if p["id"] == payment_id:
                found_payment = p
                break
        if found_payment:
            self.payment = found_payment
            for s in student_state.students:
                if s["id"] == found_payment["student_id"]:
                    self.student = s
                    break


def invoice_page() -> rx.Component:
    return rx.el.div(
        rx.el.style(
            "@media print { body { background: white; } .no-print { display: none !important; } .print-content { box-shadow: none !important; border: none !important; padding: 0 !important; margin: 0 !important; width: 100% !important; } }"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("arrow-left", class_name="w-4 h-4 mr-2"),
                    "Volver",
                    on_click=rx.redirect("/"),
                    class_name="flex items-center px-4 py-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 text-sm font-medium transition-colors",
                ),
                rx.el.button(
                    rx.icon("printer", class_name="w-4 h-4 mr-2"),
                    "Imprimir Factura",
                    on_click=rx.call_script("window.print()"),
                    class_name="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium transition-colors",
                ),
                class_name="flex justify-between items-center mb-8 no-print max-w-3xl mx-auto w-full",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("graduation-cap", class_name="w-12 h-12 text-blue-600"),
                        rx.el.div(
                            rx.el.h1(
                                InvoiceState.company_name,
                                class_name="text-2xl font-bold text-gray-900",
                            ),
                            rx.el.p(
                                InvoiceState.company_rif,
                                class_name="text-sm text-gray-500",
                            ),
                            rx.el.p(
                                InvoiceState.company_address,
                                class_name="text-sm text-gray-500",
                            ),
                            rx.el.p(
                                InvoiceState.company_phone,
                                class_name="text-sm text-gray-500",
                            ),
                            class_name="ml-4",
                        ),
                        class_name="flex items-start",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "FACTURA",
                            class_name="text-3xl font-bold text-gray-200 tracking-widest uppercase",
                        ),
                        rx.el.p(
                            InvoiceState.payment["invoice_number"],
                            class_name="text-lg font-bold text-gray-700 font-mono mt-1",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Fecha:",
                                class_name="text-sm font-semibold text-gray-500 mr-2",
                            ),
                            rx.el.span(
                                InvoiceState.payment["date"],
                                class_name="text-sm text-gray-900",
                            ),
                            class_name="mt-2",
                        ),
                        class_name="text-right",
                    ),
                    class_name="flex justify-between items-start mb-12 border-b border-gray-100 pb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Facturar A:",
                            class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4",
                        ),
                        rx.el.p(
                            InvoiceState.student["representative"],
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.p(
                            f"C.I: {InvoiceState.student.get('representative_dni', 'N/A')}",
                            class_name="text-sm text-gray-600",
                        ),
                        class_name="w-1/2",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Estudiante:",
                            class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4",
                        ),
                        rx.el.p(
                            InvoiceState.student["name"],
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.p(
                            f"C.I: {InvoiceState.student.get('student_dni', 'N/A')}",
                            class_name="text-sm text-gray-600",
                        ),
                        rx.el.p(
                            f"{InvoiceState.student['grade']} - {InvoiceState.student['section']}",
                            class_name="text-sm text-gray-600",
                        ),
                        class_name="w-1/2 text-right",
                    ),
                    class_name="flex justify-between mb-12",
                ),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Concepto",
                                class_name="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 rounded-tl-lg rounded-bl-lg",
                            ),
                            rx.el.th(
                                "Método",
                                class_name="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                "Ref",
                                class_name="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                "Importe",
                                class_name="px-4 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 rounded-tr-lg rounded-br-lg",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.el.tr(
                            rx.el.td(
                                rx.el.div(
                                    InvoiceState.payment["concept"],
                                    class_name="font-bold text-gray-900",
                                ),
                                class_name="px-4 py-4 text-sm",
                            ),
                            rx.el.td(
                                InvoiceState.payment["method"],
                                class_name="px-4 py-4 text-sm text-gray-600",
                            ),
                            rx.el.td(
                                InvoiceState.payment["reference"],
                                class_name="px-4 py-4 text-sm text-gray-600 font-mono",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    f"{InvoiceState.payment['amount']:.2f}",
                                    class_name="font-bold text-gray-900",
                                ),
                                rx.el.div(
                                    InvoiceState.payment["currency"],
                                    class_name="text-xs text-gray-500",
                                ),
                                class_name="px-4 py-4 text-sm text-right",
                            ),
                            class_name="border-b border-gray-100",
                        )
                    ),
                    class_name="w-full mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Total Pagado:",
                                class_name="font-bold text-gray-700 mr-8",
                            ),
                            rx.el.span(
                                f"{InvoiceState.payment['amount']:.2f} {InvoiceState.payment.get('currency', '')}",
                                class_name="text-2xl font-bold text-blue-600",
                            ),
                            class_name="flex justify-between items-center pt-4 border-t-2 border-gray-100",
                        ),
                        class_name="w-1/2 ml-auto",
                    ),
                    class_name="mb-16",
                ),
                rx.el.div(
                    rx.el.p(
                        "Gracias por su pago",
                        class_name="text-center font-medium text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Este documento sirve como comprobante de pago válido.",
                        class_name="text-center text-sm text-gray-500",
                    ),
                    class_name="border-t border-gray-100 pt-8",
                ),
                class_name="bg-white p-12 rounded-2xl shadow-lg border border-gray-100 max-w-3xl mx-auto print-content",
            ),
            class_name="min-h-screen bg-gray-50 py-12 px-4 print:p-0 print:bg-white",
        ),
        class_name="w-full font-['Inter']",
    )