# Пример данных
buildings = [
    {"id": 1, "name": "Здание A", "image": r"C:\Users\ratmi\PycharmProjects\employee_adaptation_project\application\tg_bot\office_maps\personal_actions\floor.png"},
    {"id": 2, "name": "Здание B", "image": r"C:\Users\ratmi\PycharmProjects\employee_adaptation_project\application\tg_bot\office_maps\personal_actions\floor.png"},
]

floors = {
    1: [{"id": 1, "name": "Этаж 1", "image": r"C:\Users\ratmi\PycharmProjects\employee_adaptation_project\application\tg_bot\office_maps\personal_actions\floor.png"}, {"id": 2, "name": "Этаж 2", "image": r"C:\Users\ratmi\PycharmProjects\employee_adaptation_project\application\tg_bot\office_maps\personal_actions\floor.png"}],
    2: [{"id": 1, "name": "Этаж 1", "image": r"C:\Users\ratmi\PycharmProjects\employee_adaptation_project\application\tg_bot\office_maps\personal_actions\floor.png"}, {"id": 2, "name": "Этаж 2", "image": r"C:\Users\ratmi\PycharmProjects\employee_adaptation_project\application\tg_bot\office_maps\personal_actions\floor.png"}],
}

sections = {
    (1, 1): [{"id": 1, "name": "Отдел кадров"}, {"id": 2, "name": "Бухгалтерия"}],
    (1, 2): [{"id": 3, "name": "IT отдел"}, {"id": 4, "name": "Маркетинг"}],
    (2, 1): [{"id": 5, "name": "Отдел продаж"}, {"id": 6, "name": "Логистика"}],
    (2, 2): [{"id": 7, "name": "HR"}, {"id": 8, "name": "Финансы"}],
}