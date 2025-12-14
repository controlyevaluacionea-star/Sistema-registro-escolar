import reflex as rx
from app.components.sidebar import sidebar
from app.states.extra_payment_state import ExtraPaymentState


def extra_payment_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(
                        ExtraPaymentState.is_editing,
                        "Editar Pago Extra",
                        "Nuevo Pago Extra",
                    ),
                    class_name="text-xl font-bold text-gray-800 mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Nombre del Concepto",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="name",
                            default_value=ExtraPaymentState.current_payment.get(
                                "name", ""
                            ),
                            required=True,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Monto (USD)",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                step="0.01",
                                name="amount",
                                default_value=ExtraPaymentState.current_payment.get(
                                    "amount", ""
                                ),
                                required=True,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Alcance",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option("Toda la Escuela", value="Global"),
                                rx.el.option("Por Grado", value="Grado"),
                                rx.el.option("Por Sección", value="Seccion"),
                                name="scope",
                                value=ExtraPaymentState.form_scope,
                                on_change=ExtraPaymentState.set_form_scope,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="flex-1",
                        ),
                        class_name="flex gap-4 mb-4",
                    ),
                    rx.cond(
                        ExtraPaymentState.form_scope == "Grado",
                        rx.el.div(
                            rx.el.label(
                                "Grado Específico",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option("Kinder", value="Kinder"),
                                rx.el.option("1er Grado", value="1er Grado"),
                                rx.el.option("2do Grado", value="2do Grado"),
                                rx.el.option("3er Grado", value="3er Grado"),
                                rx.el.option("4to Grado", value="4to Grado"),
                                rx.el.option("5to Grado", value="5to Grado"),
                                rx.el.option("6to Grado", value="6to Grado"),
                                name="target",
                                default_value=ExtraPaymentState.current_payment.get(
                                    "target", "1er Grado"
                                ),
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="mb-6",
                        ),
                    ),
                    rx.cond(
                        ExtraPaymentState.form_scope == "Seccion",
                        rx.el.div(
                            rx.el.label(
                                "Sección Específica",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="target",
                                placeholder="Ej. A",
                                default_value=ExtraPaymentState.current_payment.get(
                                    "target", ""
                                ),
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            type="button",
                            on_click=ExtraPaymentState.close_dialog,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50",
                        ),
                        rx.el.button(
                            "Guardar",
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                        ),
                        class_name="flex justify-end gap-3 mt-4",
                    ),
                    on_submit=ExtraPaymentState.save_extra_payment,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-md z-50",
            ),
        ),
        open=ExtraPaymentState.is_open,
        on_open_change=ExtraPaymentState.close_dialog,
    )


def extra_payment_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.header(
                rx.el.div(
                    rx.el.h2(
                        "Configuración de Pagos Extraordinarios",
                        class_name="text-xl font-semibold text-gray-800",
                    ),
                    class_name="flex items-center h-full px-8",
                ),
                class_name="h-20 bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Administre los pagos especiales y extraordinarios.",
                            class_name="text-gray-500",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="w-4 h-4 mr-2"),
                            "Nuevo Pago Extra",
                            on_click=ExtraPaymentState.open_add_dialog,
                            class_name="flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-xl hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Concepto",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Monto (USD)",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Alcance",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Objetivo",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Acciones",
                                        class_name="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                ),
                                class_name="bg-gray-50 border-b border-gray-100",
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    ExtraPaymentState.extra_payments,
                                    lambda p: rx.el.tr(
                                        rx.el.td(
                                            rx.el.div(
                                                p["name"],
                                                class_name="font-medium text-gray-900",
                                            ),
                                            class_name="px-6 py-4 whitespace-nowrap",
                                        ),
                                        rx.el.td(
                                            rx.el.div(
                                                f"$ {p['amount']}",
                                                class_name="px-3 py-1 inline-flex text-sm font-semibold bg-green-50 text-green-700 rounded-full",
                                            ),
                                            class_name="px-6 py-4 whitespace-nowrap",
                                        ),
                                        rx.el.td(
                                            rx.el.span(
                                                p["scope"],
                                                class_name="text-sm text-gray-600",
                                            ),
                                            class_name="px-6 py-4 whitespace-nowrap",
                                        ),
                                        rx.el.td(
                                            rx.el.span(
                                                rx.cond(
                                                    p["target"] == "", "-", p["target"]
                                                ),
                                                class_name="text-sm font-mono text-gray-500",
                                            ),
                                            class_name="px-6 py-4 whitespace-nowrap",
                                        ),
                                        rx.el.td(
                                            rx.el.div(
                                                rx.el.button(
                                                    rx.icon(
                                                        "pencil",
                                                        class_name="w-4 h-4 text-blue-500",
                                                    ),
                                                    on_click=lambda: ExtraPaymentState.open_edit_dialog(
                                                        p
                                                    ),
                                                    class_name="p-2 hover:bg-blue-50 rounded-lg",
                                                ),
                                                rx.el.button(
                                                    rx.icon(
                                                        "trash-2",
                                                        class_name="w-4 h-4 text-red-500",
                                                    ),
                                                    on_click=lambda: ExtraPaymentState.delete_extra_payment(
                                                        p["id"]
                                                    ),
                                                    class_name="p-2 hover:bg-red-50 rounded-lg",
                                                ),
                                                class_name="flex justify-end gap-1",
                                            ),
                                            class_name="px-6 py-4 whitespace-nowrap text-right",
                                        ),
                                        class_name="border-b border-gray-50 hover:bg-gray-50 transition-colors",
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
            extra_payment_dialog(),
            class_name="flex flex-col flex-1 h-screen overflow-hidden bg-gray-50/50",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900 overflow-hidden",
    )