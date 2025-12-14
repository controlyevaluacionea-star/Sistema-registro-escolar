import reflex as rx
from app.states.payment_state import PaymentState
from app.states.student_state import StudentState
from app.states.concept_state import ConceptState
from app.states.config_state import ConfigState
from app.states.extra_payment_state import ExtraPaymentState


def payment_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Registrar Nuevo Pago", class_name="text-lg font-bold text-gray-800"
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("refresh-cw", class_name="w-3 h-3 text-blue-600 mr-1"),
                        "Actualizar",
                        on_click=ConfigState.fetch_bcv_rate,
                        class_name="text-xs text-blue-600 font-medium hover:bg-blue-50 px-2 py-1 rounded-md transition-colors flex items-center mr-2",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Tasa BCV:", class_name="text-xs text-gray-500 mr-2"
                        ),
                        rx.el.span(
                            f"{ConfigState.active_rate} Bs/$",
                            class_name="text-xs font-bold text-white bg-blue-600 px-2 py-1 rounded-md shadow-sm",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center mb-2",
            ),
            rx.el.p(
                "Complete los detalles del pago recibido.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.span("Estudiante", class_name="text-sm font-medium text-gray-700"),
            rx.el.input(
                placeholder="Buscar por nombre o cédula...",
                on_change=StudentState.set_search,
                class_name="text-xs px-2 py-1 bg-white border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 w-48",
            ),
            class_name="flex justify-between items-center mb-1.5",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "user",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400",
                    ),
                    rx.el.select(
                        rx.el.option("Seleccione un estudiante...", value=""),
                        rx.foreach(
                            StudentState.filtered_students,
                            lambda s: rx.el.option(
                                f"{s['name']} ({s.get('student_dni', 'S/I')}) - {s['grade']}",
                                value=s["id"],
                            ),
                        ),
                        name="student_id",
                        on_change=PaymentState.select_student,
                        class_name="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all cursor-pointer appearance-none",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="mb-5",
            ),
            rx.el.div(
                rx.el.label(
                    "Concepto de Pago",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.div(
                    rx.icon(
                        "tag",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400",
                    ),
                    rx.el.select(
                        rx.el.option("Seleccione concepto...", value=""),
                        rx.el.optgroup(
                            rx.foreach(
                                ConceptState.concepts,
                                lambda c: rx.el.option(c["name"], value=c["name"]),
                            ),
                            label="Mensualidades y Aranceles",
                        ),
                        rx.cond(
                            PaymentState.show_extra_payments,
                            rx.el.optgroup(
                                rx.foreach(
                                    PaymentState.filtered_extra_payments,
                                    lambda ep: rx.el.option(
                                        ep["name"], value=ep["name"]
                                    ),
                                ),
                                label="Pagos Extraordinarios",
                            ),
                        ),
                        name="concept",
                        value=PaymentState.form_concept,
                        on_change=PaymentState.set_form_concept,
                        class_name="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all cursor-pointer appearance-none",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            checked=PaymentState.show_extra_payments,
                            on_click=PaymentState.toggle_extra_payments,
                            class_name="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500",
                        ),
                        rx.el.span(
                            "Incluir pagos extraordinarios en la lista",
                            class_name="ml-2 text-xs text-gray-500",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="mb-5",
                ),
                class_name="mb-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Método de Pago",
                        class_name="block text-sm font-medium text-gray-700 mb-1.5",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                PaymentState.methods, lambda m: rx.el.option(m, value=m)
                            ),
                            name="method",
                            value=PaymentState.form_method,
                            on_change=PaymentState.set_form_method,
                            class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all cursor-pointer appearance-none",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                    class_name="w-1/2",
                ),
                rx.el.div(
                    rx.el.label(
                        "Moneda",
                        class_name="block text-sm font-medium text-gray-700 mb-1.5",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                PaymentState.currencies,
                                lambda c: rx.el.option(c, value=c),
                            ),
                            name="currency",
                            value=PaymentState.form_currency,
                            on_change=PaymentState.set_form_currency,
                            class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all cursor-pointer appearance-none",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                    class_name="w-1/2",
                ),
                class_name="flex gap-4 mb-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Monto a Pagar",
                        class_name="block text-sm font-medium text-gray-700 mb-1.5",
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="number",
                            step="0.01",
                            placeholder="0.00",
                            name="amount",
                            class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all placeholder:text-gray-400",
                            default_value=PaymentState.form_amount,
                            key=PaymentState.form_amount,
                        ),
                        rx.cond(
                            PaymentState.conversion_info != "",
                            rx.el.p(
                                PaymentState.conversion_info,
                                class_name="text-xs text-blue-600 font-medium mt-1 absolute -bottom-5 left-1",
                            ),
                        ),
                        class_name="relative mb-2",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.label(
                        "Referencia / Nota",
                        class_name="block text-sm font-medium text-gray-700 mb-1.5",
                    ),
                    rx.el.input(
                        type="text",
                        placeholder="Ej. #123456",
                        name="reference",
                        class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all placeholder:text-gray-400",
                    ),
                    class_name="w-1/2",
                ),
                class_name="flex gap-4 mb-8",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5 mr-2"),
                "Registrar Pago",
                type="submit",
                class_name="w-full flex items-center justify-center py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl shadow-lg shadow-blue-200 transition-all duration-200 active:scale-[0.98]",
            ),
            on_submit=PaymentState.handle_payment_submit,
            reset_on_submit=True,
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-fit sticky top-6",
    )