import reflex as rx
from app.components.sidebar import sidebar
from app.states.config_state import ConfigState


def settings_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.header(
                rx.el.div(
                    rx.el.h2(
                        "Configuración del Sistema",
                        class_name="text-xl font-semibold text-gray-800",
                    ),
                    class_name="flex items-center h-full px-8",
                ),
                class_name="h-20 bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Tasa de Cambio",
                            class_name="text-lg font-bold text-gray-800 mb-1",
                        ),
                        rx.el.p(
                            "Gestione la tasa de cambio para la conversión automática de pagos.",
                            class_name="text-sm text-gray-500 mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "Tasa Activa en Sistema",
                                    class_name="text-xs font-medium text-gray-500 uppercase tracking-wider block mb-2",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        "Bs. ",
                                        class_name="text-2xl text-gray-400 font-light",
                                    ),
                                    rx.el.span(
                                        ConfigState.active_rate,
                                        class_name="text-4xl font-bold text-blue-600",
                                    ),
                                    class_name="flex items-baseline",
                                ),
                                class_name="bg-blue-50 border border-blue-100 p-6 rounded-xl mb-8",
                            ),
                            rx.el.div(
                                rx.el.h4(
                                    "Configuración de Tasa",
                                    class_name="font-medium text-gray-900 mb-4",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.div(
                                            rx.el.span(
                                                "Tasa Oficial BCV",
                                                class_name="text-sm font-medium text-gray-700 block",
                                            ),
                                            rx.el.span(
                                                f"Última actualización: {ConfigState.last_updated}",
                                                class_name="text-xs text-gray-400",
                                            ),
                                        ),
                                        rx.el.button(
                                            rx.cond(
                                                ConfigState.is_loading_rate,
                                                rx.spinner(size="1"),
                                                rx.icon(
                                                    "refresh-cw",
                                                    class_name="w-4 h-4 mr-2",
                                                ),
                                            ),
                                            "Actualizar Ahora",
                                            disabled=ConfigState.is_loading_rate,
                                            on_click=ConfigState.fetch_bcv_rate,
                                            class_name="flex items-center px-3 py-2 bg-white border border-gray-200 text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-50 transition-colors",
                                        ),
                                        class_name="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-200 mb-4",
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            rx.el.input(
                                                type="checkbox",
                                                checked=ConfigState.use_manual_rate,
                                                on_change=ConfigState.toggle_manual_mode,
                                                class_name="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500",
                                            ),
                                            rx.el.span(
                                                "Usar tasa manual personalizada",
                                                class_name="ml-2 text-sm text-gray-700",
                                            ),
                                            class_name="flex items-center mb-4",
                                        ),
                                        rx.cond(
                                            ConfigState.use_manual_rate,
                                            rx.el.div(
                                                rx.el.label(
                                                    "Tasa Manual (Bs/$)",
                                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                                ),
                                                rx.el.input(
                                                    type="number",
                                                    step="0.01",
                                                    default_value=ConfigState.manual_rate,
                                                    on_blur=ConfigState.set_manual_rate,
                                                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                                                ),
                                                class_name="animate-in fade-in slide-in-from-top-2 duration-200",
                                            ),
                                        ),
                                    ),
                                    class_name="space-y-4",
                                ),
                            ),
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h4(
                                    "Gestión de Conceptos y Montos",
                                    class_name="font-medium text-gray-900 mb-2",
                                ),
                                rx.el.p(
                                    "Configure los montos de las mensualidades, inscripciones y otros aranceles en dólares (USD).",
                                    class_name="text-sm text-gray-500 mb-4",
                                ),
                                rx.el.button(
                                    rx.icon("external-link", class_name="w-4 h-4 mr-2"),
                                    "Ir a Configuración de Conceptos",
                                    on_click=rx.redirect("/concepts"),
                                    class_name="flex items-center justify-center w-full px-4 py-2 bg-blue-50 text-blue-600 text-sm font-medium rounded-lg hover:bg-blue-100 transition-colors border border-blue-100",
                                ),
                                class_name="pt-6 border-t border-gray-100",
                            ),
                            class_name="mt-2",
                        ),
                        class_name="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 max-w-2xl",
                    ),
                    class_name="p-8 max-w-[1600px] mx-auto",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden bg-gray-50/50",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900 overflow-hidden",
    )