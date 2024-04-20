import json
import datetime
import os

NOTES_FILE = 'notes.json'

def create_note():
    try:
        note_id = input("Введите ID заметки: ")
        title = input("Введите заголовок заметки: ")
        body = input("Введите содержимое заметки: ")
        created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        note = {
            "id": note_id,
            "title": title,
            "body": body,
            "created_date": created_date
        }
        return note
    except Exception as e:
        print("При создании заметки произошла ошибка:", e)
        return None

def save_notes(notes):
    try:
        with open(NOTES_FILE, 'w') as file:
            json.dump(notes, file, indent=4)
    except Exception as e:
        print("При сохранении заметок произошла ошибка:", e)

def read_notes():
    try:
        if not os.path.exists(NOTES_FILE):
            print("Заметки не найдены.")
            return

        with open(NOTES_FILE) as file:
            notes = json.load(file)
            for note in notes:
                print("ID: ", note["id"])
                print("Заголовок: ", note["title"])
                print("Содержимое: ", note["body"])
                print("Создано: ", note["created_date"])
                print()
    except Exception as e:
        print("При чтении заметок произошла ошибка:", e)


def filter_notes_by_date(date):
    try:
        if not os.path.exists(NOTES_FILE):
            print("Заметки не найдены.")
            return []

        with open(NOTES_FILE) as file:
            notes = json.load(file)
            filtered_notes = [note for note in notes if note["created_date"].split()[0] == date]
            if not filtered_notes:
                print("Заметки не найдены для указанной даты.")
                return []

            print("Заметки найдены для указанной даты:")
            for i, note in enumerate(filtered_notes):
                print(f"{i+1}. ID: {note['id']}, Заголовок: {note['title']}")
            return filtered_notes
    except Exception as e:
        print("При фильтрации заметок по дате произошла ошибка:", e)
        return []


def print_selected_note(filtered_notes):
    try:
        if not filtered_notes:
            return

        choice = int(input("Введите номер заметки для просмотра: "))
        selected_note = filtered_notes[choice - 1]
        print("Выбранная заметка:")
        print("ID: ", selected_note["id"])
        print("Заголовок: ", selected_note["title"])
        print("Содержимое: ", selected_note["body"])
        print("Создано: ", selected_note["created_date"])
    except (IndexError, ValueError):
        print("Неверный ввод. Пожалуйста, введите правильный номер заметки.")

def edit_note(note_id):
    try:
        if not os.path.exists(NOTES_FILE):
            print("Заметки не найдены.")
            return

        with open(NOTES_FILE, 'r') as file:
            notes = json.load(file)

        for note in notes:
            if note["id"] == note_id:
                title = input("Введите новый заголовок: ")
                body = input("Введите новое содержимое: ")
                note["title"] = title
                note["body"] = body
                note["created_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break

        save_notes(notes)
    except Exception as e:
        print("При редактировании заметки произошла ошибка:", e)

def delete_note(note_id):
    try:
        if not os.path.exists(NOTES_FILE):
            print("Заметки не найдены.")
            return

        with open(NOTES_FILE, 'r') as file:
            notes = json.load(file)

        notes = [note for note in notes if note["id"] != note_id]
        save_notes(notes)
    except Exception as e:
        print("При удалении заметки произошла ошибка:", e)

def main():
    while True:
        print("1. Создать новую заметку")
        print("2. Прочитать все заметки")
        print("3. Прочитать заметки по диапазону дат")
        print("4. Вывести выбранную заметку")
        print("5. Редактировать заметку")
        print("6. Удалить заметку")
        print("7. Поиск заметок по дате")
        print("8. Выйти")

        choice = input("Введите ваш выбор: ")

        try:
          if choice == "1":
              note = create_note()
              if note:
                  save_notes([note] if not os.path.exists(NOTES_FILE) else (notes := json.load(open(NOTES_FILE, 'r')) or []) and notes.append(note) or notes)
          elif choice == "2":
              read_notes()
          elif choice == "3":
              start_date, end_date = input("Введите начальную дату (ГГГГ-ММ-ДД): "), input("Введите конечную дату (ГГГГ-ММ-ДД): ")
              filtered_notes = filter_notes_by_date(start_date, end_date)
          elif choice == "4":
              print_selected_note(filtered_notes) if filtered_notes else print("Нет доступных отфильтрованных заметок. Пожалуйста, сначала выполните операцию поиска.")
          elif choice == "5":
              edit_note(input("Введите ID заметки для редактирования: "))
          elif choice == "6":
              delete_note(input("Введите ID заметки для удаления: "))
          elif choice == "7":
              filtered_notes = filter_notes_by_date(input("Введите дату для поиска (ГГГГ-ММ-ДД): "))
          elif choice == "8":
              break
          else:
              print("Неверный выбор. Пожалуйста, попробуйте еще раз.")
        except Exception as e:
            print("Произошла ошибка:", e)


if __name__ == "__main__":
    main()