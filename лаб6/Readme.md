1.Запустіть Docker Desktop.
2.Відкрийте термінал (PowerShell) і перейдіть у вашу папку з проєктом:
    cd "C:\Users\userPC\Desktop\2 курс 1 сем\патерни проектування\лаб6"
3.Виконайте команду запуску:
    docker-compose up
4.щоб вийти контрл + С

Додаток (Frontend): http://localhost:8000/api/v1/
Документація API: http://localhost:8000/docs
База Даних: http://localhost:8081/ (логін: admin, пароль: pass)

                                                                            Тести
1.Запустіть все у фоновому режимі:
    docker-compose up -d
2.Тепер виконайте команду для тестів:
    docker-compose exec -e PYTHONPATH=. app pytest -q
3.Вийти з фоновго редиму
    docker-compose down