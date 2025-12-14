import reflex as rx
from app.components.sidebar import sidebar
from app.states.student_state import StudentState


def student_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(
                        StudentState.is_editing, "Editar Estudiante", "Nuevo Estudiante"
                    ),
                    class_name="text-xl font-bold text-gray-800 mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Nombre Completo",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="name",
                            default_value=StudentState.current_student.get("name", ""),
                            required=True,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Cédula del Estudiante",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="student_dni",
                            placeholder="V-00000000",
                            default_value=StudentState.current_student.get(
                                "student_dni", ""
                            ),
                            required=True,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Grado",
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
                                name="grade",
                                default_value=StudentState.current_student.get(
                                    "grade", "1er Grado"
                                ),
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Sección",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="section",
                                default_value=StudentState.current_student.get(
                                    "section", "A"
                                ),
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="w-24",
                        ),
                        class_name="flex gap-4 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Representante",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="representative",
                                default_value=StudentState.current_student.get(
                                    "representative", ""
                                ),
                                required=True,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Cédula Repr.",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="representative_dni",
                                placeholder="V-00000000",
                                default_value=StudentState.current_student.get(
                                    "representative_dni", ""
                                ),
                                required=True,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="w-1/3",
                        ),
                        class_name="flex gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            type="button",
                            on_click=StudentState.close_dialog,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50",
                        ),
                        rx.el.button(
                            "Guardar",
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    on_submit=StudentState.save_student,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-md z-50",
            ),
        ),
        open=StudentState.is_open,
        on_open_change=StudentState.close_dialog,
    )


def student_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.header(
                rx.el.div(
                    rx.el.h2(
                        "Gestión de Estudiantes",
                        class_name="text-xl font-semibold text-gray-800",
                    ),
                    class_name="flex items-center h-full px-8",
                ),
                class_name="h-20 bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Buscar estudiante...",
                            on_change=StudentState.set_search,
                            class_name="w-full max-w-md px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="w-4 h-4 mr-2"),
                            "Nuevo Estudiante",
                            on_click=StudentState.open_add_dialog,
                            class_name="flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-xl hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Nombre",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Grado/Sección",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Representante",
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
                                    StudentState.filtered_students,
                                    lambda s: rx.el.tr(
                                        rx.el.td(
                                            rx.el.div(
                                                s["name"],
                                                class_name="font-medium text-gray-900",
                                            ),
                                            rx.el.div(
                                                s.get("student_dni", ""),
                                                class_name="text-xs text-gray-500 font-mono",
                                            ),
                                            class_name="px-6 py-4 whitespace-nowrap",
                                        ),
                                        rx.el.td(
                                            rx.el.span(
                                                f'''{s["grade"]} "{s["section"]}"''',
                                                class_name="px-2 py-1 text-xs font-medium bg-blue-50 text-blue-700 rounded-full",
                                            ),
                                            class_name="px-6 py-4 whitespace-nowrap",
                                        ),
                                        rx.el.td(
                                            rx.el.div(
                                                s["representative"],
                                                class_name="text-sm text-gray-900",
                                            ),
                                            rx.el.div(
                                                s.get("representative_dni", ""),
                                                class_name="text-xs text-gray-500 font-mono",
                                            ),
                                            class_name="px-6 py-4 whitespace-nowrap",
                                        ),
                                        rx.el.td(
                                            rx.el.div(
                                                rx.el.button(
                                                    rx.icon(
                                                        "file-text",
                                                        class_name="w-4 h-4 text-gray-500",
                                                    ),
                                                    on_click=rx.redirect(
                                                        f"/students/{s['id']}"
                                                    ),
                                                    class_name="p-2 hover:bg-gray-100 rounded-lg",
                                                    title="Ver Estado de Cuenta",
                                                ),
                                                rx.el.button(
                                                    rx.icon(
                                                        "pencil",
                                                        class_name="w-4 h-4 text-blue-500",
                                                    ),
                                                    on_click=lambda: StudentState.open_edit_dialog(
                                                        s
                                                    ),
                                                    class_name="p-2 hover:bg-blue-50 rounded-lg",
                                                ),
                                                rx.el.button(
                                                    rx.icon(
                                                        "trash-2",
                                                        class_name="w-4 h-4 text-red-500",
                                                    ),
                                                    on_click=lambda: StudentState.delete_student(
                                                        s["id"]
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
                    class_name="p-8 max-w-[1600px] mx-auto",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            student_dialog(),
            class_name="flex flex-col flex-1 h-screen overflow-hidden bg-gray-50/50",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900 overflow-hidden",
    )