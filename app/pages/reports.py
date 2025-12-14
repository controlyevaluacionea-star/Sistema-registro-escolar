import reflex as rx
from app.components.sidebar import sidebar
from app.states.stats_state import StatsState
from app.states.payment_state import PaymentState


def stat_card(
    title: str, value: str, icon: str, color_class: str, subtext: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-6 h-6 {color_class}"),
            class_name=f"w-12 h-12 rounded-xl flex items-center justify-center mb-3 {color_class.replace('text-', 'bg-').replace('600', '50')}",
        ),
        rx.el.h3(title, class_name="text-sm font-medium text-gray-500 mb-1"),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        rx.cond(
            subtext != "", rx.el.p(subtext, class_name="text-xs text-gray-400 mt-1")
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def revenue_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Evolución de Recaudación (Año Actual)",
            class_name="text-lg font-bold text-gray-800 mb-6",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                horizontal=True,
                vertical=False,
                class_name="opacity-25",
                stroke_dasharray="3 3",
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "white",
                    "borderRadius": "8px",
                    "border": "1px solid #e5e7eb",
                    "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                }
            ),
            rx.recharts.x_axis(
                data_key="name",
                axis_line=False,
                tick_line=False,
                tick_size=10,
                custom_attrs={"fontSize": "12px"},
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                tick_size=10,
                custom_attrs={"fontSize": "12px"},
            ),
            rx.recharts.area(
                data_key="usd",
                name="USD ($)",
                stroke="#2563EB",
                fill="#3B82F6",
                fill_opacity=0.2,
                stroke_width=2,
                type_="monotone",
            ),
            rx.recharts.area(
                data_key="bs",
                name="Bolívares (Bs)",
                stroke="#059669",
                fill="#10B981",
                fill_opacity=0.1,
                stroke_width=2,
                type_="monotone",
            ),
            data=StatsState.monthly_revenue_data,
            height=350,
            width="100%",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mb-8",
    )


def closing_report_filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Desde", class_name="block text-xs font-medium text-gray-500 mb-1"
                ),
                rx.el.input(
                    type="date",
                    default_value=StatsState.start_date,
                    on_change=StatsState.set_start_date,
                    class_name="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Hasta", class_name="block text-xs font-medium text-gray-500 mb-1"
                ),
                rx.el.input(
                    type="date",
                    default_value=StatsState.end_date,
                    on_change=StatsState.set_end_date,
                    class_name="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Método", class_name="block text-xs font-medium text-gray-500 mb-1"
                ),
                rx.el.select(
                    rx.el.option("Todos", value="Todos"),
                    rx.foreach(
                        PaymentState.methods, lambda m: rx.el.option(m, value=m)
                    ),
                    on_change=StatsState.set_method,
                    class_name="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Moneda", class_name="block text-xs font-medium text-gray-500 mb-1"
                ),
                rx.el.select(
                    rx.el.option("Todos", value="Todos"),
                    rx.foreach(
                        PaymentState.currencies, lambda c: rx.el.option(c, value=c)
                    ),
                    on_change=StatsState.set_currency,
                    class_name="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                ),
                class_name="flex-1",
            ),
            class_name="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6 print:hidden",
        ),
        class_name="w-full",
    )


def closing_report_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Reporte Detallado de Cierre",
                class_name="text-lg font-bold text-gray-800",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("printer", class_name="w-4 h-4 mr-2"),
                    "Imprimir Reporte",
                    on_click=rx.call_script("window.print()"),
                    class_name="flex items-center px-4 py-2 bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded-xl hover:bg-gray-50 transition-colors shadow-sm",
                ),
                class_name="print:hidden",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        closing_report_filters(),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Fecha/Hora",
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
                            "Método",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Ref",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Monto",
                            class_name="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-50 border-b border-gray-100",
                ),
                rx.el.tbody(
                    rx.foreach(
                        StatsState.filtered_payments,
                        lambda p: rx.el.tr(
                            rx.el.td(
                                rx.el.div(
                                    p["date"], class_name="font-medium text-gray-900"
                                ),
                                rx.el.div(
                                    p["timestamp"], class_name="text-xs text-gray-400"
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-sm",
                            ),
                            rx.el.td(
                                p["student_name"],
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
                                p["method"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            rx.el.td(
                                p["reference"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-500",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    f"{p['amount']}",
                                    class_name="font-bold text-gray-900",
                                ),
                                rx.el.div(
                                    p["currency"], class_name="text-xs text-gray-500"
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-right",
                            ),
                            class_name="border-b border-gray-50 hover:bg-gray-50",
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-100",
                ),
                rx.el.tfoot(
                    rx.el.tr(
                        rx.el.td(
                            "Total Recaudado (Selección)",
                            col_span=5,
                            class_name="px-6 py-4 text-right text-sm font-bold text-gray-800",
                        ),
                        rx.el.td(
                            rx.el.div(
                                f"$ {StatsState.filtered_totals['usd']}",
                                class_name="text-sm font-bold text-blue-600",
                            ),
                            rx.el.div(
                                f"Bs {StatsState.filtered_totals['bs']}",
                                class_name="text-sm font-bold text-green-600",
                            ),
                            class_name="px-6 py-4 text-right bg-gray-50",
                        ),
                        class_name="border-t-2 border-gray-100",
                    )
                ),
                class_name="min-w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden p-6",
    )


def reports_page() -> rx.Component:
    return rx.el.div(
        rx.el.style(
            "@media print { .no-print { display: none !important; } body { background: white; } .print-content { padding: 0; margin: 0; } }"
        ),
        rx.el.div(sidebar(), class_name="no-print"),
        rx.el.main(
            rx.el.header(
                rx.el.div(
                    rx.el.h2(
                        "Reportes y Estadísticas",
                        class_name="text-xl font-semibold text-gray-800",
                    ),
                    class_name="flex items-center h-full px-8",
                ),
                class_name="h-20 bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-10 no-print",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        stat_card(
                            "Recaudado Hoy (USD)",
                            f"$ {StatsState.today_metrics['usd']}",
                            "dollar-sign",
                            "text-blue-600",
                            "Ingresos en divisa",
                        ),
                        stat_card(
                            "Recaudado Hoy (Bs)",
                            f"Bs {StatsState.today_metrics['bs']}",
                            "banknote",
                            "text-green-600",
                            "Ingresos en moneda local",
                        ),
                        stat_card(
                            "Transacciones Hoy",
                            f"{StatsState.today_metrics['count']}",
                            "activity",
                            "text-purple-600",
                            "Pagos registrados hoy",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 no-print",
                    ),
                    rx.el.div(revenue_chart(), class_name="no-print"),
                    closing_report_table(),
                    class_name="p-8 max-w-[1600px] mx-auto print-content",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden bg-gray-50/50",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900 overflow-hidden",
    )