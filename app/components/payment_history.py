import reflex as rx
from app.states.payment_state import PaymentState


def payment_history() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Historial de Transacciones",
                class_name="text-lg font-bold text-gray-800",
            ),
            rx.el.div(
                rx.el.span(
                    f"Total USD: ${PaymentState.total_collected_usd}",
                    class_name="text-sm font-semibold text-green-600 bg-green-50 px-3 py-1 rounded-lg border border-green-100",
                ),
                rx.el.span(
                    f"Total Bs: {PaymentState.total_collected_bs} Bs",
                    class_name="text-sm font-semibold text-blue-600 bg-blue-50 px-3 py-1 rounded-lg border border-blue-100",
                ),
                class_name="flex gap-2",
            ),
            class_name="flex items-center justify-between mb-6",
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
                            "Estudiante",
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
                        rx.el.th(
                            "Ref",
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
                    rx.cond(
                        PaymentState.payments.length() > 0,
                        rx.foreach(
                            PaymentState.payments,
                            lambda p: rx.el.tr(
                                rx.el.td(
                                    rx.el.div(
                                        p["date"],
                                        class_name="font-medium text-gray-900",
                                    ),
                                    rx.el.div(
                                        p["timestamp"],
                                        class_name="text-xs text-gray-400",
                                    ),
                                    class_name="px-6 py-4 whitespace-nowrap text-sm",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        p["student_name"],
                                        class_name="font-medium text-gray-900",
                                    ),
                                    class_name="px-6 py-4 whitespace-nowrap text-sm",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        p["concept"],
                                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700",
                                    ),
                                    class_name="px-6 py-4 whitespace-nowrap text-sm",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        f"{p['amount']}",
                                        class_name="font-bold text-gray-900",
                                    ),
                                    rx.el.div(
                                        p["currency"],
                                        class_name="text-xs text-gray-500",
                                    ),
                                    class_name="px-6 py-4 whitespace-nowrap text-sm",
                                ),
                                rx.el.td(
                                    p["method"],
                                    class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                                ),
                                rx.el.td(
                                    p["reference"],
                                    class_name="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-500",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.a(
                                            rx.icon(
                                                "file-text",
                                                class_name="w-4 h-4 text-blue-500",
                                            ),
                                            href=f"/invoices/{p['id']}",
                                            target="_blank",
                                            class_name="p-2 hover:bg-blue-50 rounded-lg transition-colors block",
                                            title="Ver Factura",
                                        ),
                                        rx.el.button(
                                            rx.icon(
                                                "trash-2",
                                                class_name="w-4 h-4 text-red-500",
                                            ),
                                            on_click=lambda: PaymentState.delete_payment(
                                                p["id"]
                                            ),
                                            class_name="p-2 hover:bg-red-50 rounded-lg transition-colors",
                                            title="Eliminar registro",
                                        ),
                                        class_name="flex justify-end gap-1",
                                    ),
                                    class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
                                ),
                                class_name="hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-0",
                            ),
                        ),
                        rx.el.tr(
                            rx.el.td(
                                rx.el.div(
                                    rx.icon(
                                        "inbox",
                                        class_name="w-12 h-12 text-gray-300 mb-2",
                                    ),
                                    rx.el.p(
                                        "No hay pagos registrados aún",
                                        class_name="text-gray-500 font-medium",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-12",
                                ),
                                col_span=6,
                                class_name="px-6 py-4 text-center",
                            )
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-100",
                ),
                class_name="min-w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
    )