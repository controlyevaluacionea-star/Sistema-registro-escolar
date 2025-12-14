import reflex as rx
from app.components.sidebar import sidebar
from app.components.payment_form import payment_form
from app.components.payment_history import payment_history


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.header(
                rx.el.div(
                    rx.el.h2(
                        "Registro de Pagos",
                        class_name="text-xl font-semibold text-gray-800",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("bell", class_name="w-5 h-5 text-gray-600"),
                            class_name="w-10 h-10 rounded-full bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.div(
                            rx.el.div("AD", class_name="text-sm font-bold text-white"),
                            class_name="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center border-2 border-white shadow-sm",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    class_name="flex justify-between items-center h-full px-8",
                ),
                class_name="h-20 bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            payment_form(), class_name="col-span-1 lg:col-span-4"
                        ),
                        rx.el.div(
                            payment_history(), class_name="col-span-1 lg:col-span-8"
                        ),
                        class_name="grid grid-cols-1 lg:grid-cols-12 gap-8 max-w-[1600px] mx-auto",
                    ),
                    class_name="p-8",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden bg-gray-50/50",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900 overflow-hidden",
    )


from app.pages.students import student_page
from app.pages.concepts import concept_page
from app.pages.student_detail import student_detail_page, StudentDetailState
from app.pages.reports import reports_page
from app.pages.settings import settings_page
from app.pages.extra_payments import extra_payment_page
from app.pages.invoice import invoice_page, InvoiceState
from app.states.stats_state import StatsState
from app.states.config_state import ConfigState
from app.states.payment_state import PaymentState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
            rel="stylesheet",
        )
    ],
)
app.add_page(
    index,
    route="/",
    on_load=[ConfigState.fetch_bcv_rate, PaymentState.load_initial_data],
)
app.add_page(student_page, route="/students")
app.add_page(concept_page, route="/concepts")
app.add_page(
    student_detail_page, route="/students/[id]", on_load=StudentDetailState.load_student
)
app.add_page(reports_page, route="/reports", on_load=StatsState.load_data)
app.add_page(settings_page, route="/settings")
app.add_page(extra_payment_page, route="/extra-payments")
app.add_page(
    invoice_page, route="/invoices/[payment_id]", on_load=InvoiceState.load_invoice
)