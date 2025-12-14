import reflex as rx


def sidebar_item(icon: str, label: str, url: str, active: bool = False) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon,
            class_name=f"w-5 h-5 mr-3 {('text-blue-600' if active else 'text-gray-500')}",
        ),
        rx.el.span(
            label,
            class_name=f"font-medium {('text-blue-700' if active else 'text-gray-600')}",
        ),
        href=url,
        class_name=f"\n            flex items-center px-4 py-3 rounded-xl cursor-pointer transition-all duration-200\n            {('bg-blue-50 shadow-sm' if active else 'hover:bg-gray-50')}\n        ",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("graduation-cap", class_name="w-8 h-8 text-white"),
                    class_name="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-200",
                ),
                rx.el.div(
                    rx.el.h1(
                        "EduPay",
                        class_name="text-xl font-bold text-gray-800 leading-tight",
                    ),
                    rx.el.span(
                        "Gestión Escolar",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    class_name="flex flex-col ml-3",
                ),
                class_name="flex items-center px-2 mb-10",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.el.span(
                        "PRINCIPAL",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 px-4 block",
                    ),
                    sidebar_item(
                        "layout-dashboard", "Registro de Pagos", "/", active=True
                    ),
                    sidebar_item("users", "Estudiantes", "/students"),
                    sidebar_item("banknote", "Conceptos", "/concepts"),
                    sidebar_item("layers", "Pagos Extra", "/extra-payments"),
                    class_name="flex flex-col gap-1 mb-8",
                ),
                rx.el.div(
                    rx.el.span(
                        "REPORTES",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 px-4 block",
                    ),
                    sidebar_item("bar-chart-2", "Reportes y Estadísticas", "/reports"),
                    class_name="flex flex-col gap-1 mb-8",
                ),
                rx.el.div(
                    rx.el.span(
                        "CONFIGURACIÓN",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 px-4 block",
                    ),
                    sidebar_item("settings", "Configuración", "/settings"),
                    class_name="flex flex-col gap-1",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex flex-col w-64 bg-white border-r border-gray-100 h-screen sticky top-0 p-6 shrink-0 z-20",
    )