import reflex as rx
from app.components.sidebar import sidebar
from app.states.student_state import StudentState
from app.states.payment_state import PaymentState, PaymentEntry


class StudentDetailState(rx.State):
    student: dict = {}

    @rx.var
    def student_payments(self) -> list[PaymentEntry]:
        if not self.student:
            return []
        return []

    @rx.event
    async def load_student(self):
        student_id = self.router.page.params.get("id")
        student_state = await self.get_state(StudentState)
        for s in student_state.students:
            if s["id"] == student_id:
                self.student = s
                break


def student_detail_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.header(
                rx.el.div(
                    rx.el.div(
                        rx.el.button(
                            rx.icon("arrow-left", class_name="w-5 h-5 text-gray-600"),
                            on_click=rx.redirect("/students"),
                            class_name="mr-4 p-2 hover:bg-gray-100 rounded-full transition-colors",
                        ),
                        rx.el.h2(
                            "Estado de Cuenta",
                            class_name="text-xl font-semibold text-gray-800",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex items-center h-full px-8",
                ),
                class_name="h-20 bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    StudentDetailState.student["name"],
                                    class_name="text-2xl font-bold text-gray-900 mb-1",
                                ),
                                rx.el.p(
                                    f"ID: {StudentDetailState.student['id']} | C.I: {StudentDetailState.student.get('student_dni', 'N/A')}",
                                    class_name="text-sm text-gray-500 font-mono",
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "Grado y Sección",
                                        class_name="text-xs font-medium text-gray-500 uppercase tracking-wider mb-1 block",
                                    ),
                                    rx.el.p(
                                        f"{StudentDetailState.student['grade']} - {StudentDetailState.student['section']}",
                                        class_name="text-lg font-medium text-gray-800",
                                    ),
                                    class_name="bg-gray-50 p-4 rounded-xl",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        "Representante",
                                        class_name="text-xs font-medium text-gray-500 uppercase tracking-wider mb-1 block",
                                    ),
                                    rx.el.p(
                                        StudentDetailState.student["representative"],
                                        class_name="text-lg font-medium text-gray-800",
                                    ),
                                    rx.el.p(
                                        f"C.I: {StudentDetailState.student.get('representative_dni', 'N/A')}",
                                        class_name="text-xs text-gray-500 mt-1",
                                    ),
                                    class_name="bg-gray-50 p-4 rounded-xl",
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                            ),
                            class_name="p-8",
                        ),
                        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 mb-8",
                    ),
                    rx.el.h3(
                        "Historial de Pagos",
                        class_name="text-lg font-bold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Fecha",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Concepto",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Monto",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Método",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                ),
                                class_name="bg-gray-50 border-b border-gray-100",
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    PaymentState.payments,
                                    lambda p: rx.cond(
                                        p["student_id"]
                                        == StudentDetailState.student["id"],
                                        rx.el.tr(
                                            rx.el.td(
                                                p["date"],
                                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                                            ),
                                            rx.el.td(
                                                rx.el.span(
                                                    p["concept"],
                                                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700",
                                                ),
                                                class_name="px-6 py-4 whitespace-nowrap",
                                            ),
                                            rx.el.td(
                                                rx.el.span(
                                                    f"{p['amount']} {p['currency']}",
                                                    class_name="font-medium text-gray-900",
                                                ),
                                                class_name="px-6 py-4 whitespace-nowrap text-sm",
                                            ),
                                            rx.el.td(
                                                p["method"],
                                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                                            ),
                                            class_name="border-b border-gray-50 hover:bg-gray-50",
                                        ),
                                        None,
                                    ),
                                ),
                                class_name="bg-white divide-y divide-gray-100",
                            ),
                            class_name="min-w-full",
                        ),
                        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
                    ),
                    class_name="p-8 max-w-[1000px] mx-auto",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden bg-gray-50/50",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900 overflow-hidden",
    )