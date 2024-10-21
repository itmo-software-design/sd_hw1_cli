# Задача про CLI

___

## Задача

### Задачи текущей итерации

Реализовать простой интерпретатор командной строки, поддерживающий команды:

- [x] cat [FILE] — вывести на экран содержимое файла
- [x] echo — вывести на экран свой аргумент (или аргументы)
- [x] wc [FILE] — вывести количество строк, слов и байт в файле
- [x] pwd — распечатать текущую директорию
- [x] exit — выйти из интерпретатора

- [x] Должны поддерживаться одинарные и двойные кавычки (full and weak quoting)
- [x] Окружение (команды вида “имя=значение”), оператор $
- [x] Вызов внешней программы через Process (или его аналоги)
- [ ] Команды должны поддерживать код возврата
- [ ] Классы команд должны быть разделены по отдельным файлам

### Задачи последующих итераций

- [ ] Пайплайны (оператор “|”)

___

## Состав команды

- Могилевский Матвей
- Можаев Андрей
- Шадрин Михаил
- Яценко Кирилл

___

## Запуск

Перед запуском приложения необходимо установить необходимые для работы приложения зависимости:

```shell
poetry env use python3.12
poetry install
```

Для запуска приложения из корневой директории проекта используйте команду:

```shell
poetry run python ./cli_interpreter/cli_repl.py
```

Для запуска тестов используйте команду:

```shell
poetry run pytest -vv --showlocals
```

___

## Архитектура

![image](docs/class_schema.png)

### CliInterpreter

Главный модуль системы и точка входа. Оркеструет работу приложения и реализует Read-Execute-Print Loop.
Алгоритм работы:

- Считывает строку, поданную пользователем на вход;
- Передает строку на обработку модулю `UserInpurParser`, который превращает строку в последовательность команд,
  представленных наследниками абстрактного класса `Command`;
- Передает полученную последовательность команд на вход модулю `CommandExecutor`, который исполняет последовательность
  команд;
- Выводит результат исполнения на экран;
- Повторяет цикл.

Модуль не должен заканчивать работу аварийно, все необработанные исключения должны быть отловлены в процессе его работы,
содержимое стандартного вывода ошибок должно быть отражено на экране.

Прекращение работы допустимо посредством передачи на вход одиночной команды `exit`.

### UserInputParser

Модуль отвечает за преобразование входной строки в набор команд для последующего их исполнения.
Алгоритм работы:

- Принимает на вход строку, которую ввел пользователь;
- Разделяет строку на строки-команды по оператору `|`;
- Для каждой строки команды разделяет её на токены по пробельным символам и символам открывающих и закрывающих кавычек.
  Таким образом, каждый токен будет представлять собой литерал, состояший из символов `[$_a-zA-Z0-9]`, либо строку,
  ограниченную парой однотипных кавычек `"` или `'`;
- Для токенов, где встречается специальный символ `$`, выполняет подстановку значений переменных окружения с помощью
  `CliContext.get(variable)`, если этот токен не ограничен парой одинарных кавычек `'`;
- По полученным токенам определяет тип каждой команды и набор её аргументов, оборачивая каждую из команд в один из
  наследников класса `Command`.

### Command

Абстрактный класс, описывающий команду. Содержит в себе список аргументов команды и потоки ввода и вывода, если таковые
отличаются от стандартных.
Также содержит абстрактный метод `Command.execute()`, который отвечает за выполнение команды на основе хранящихся в её
полях данных.
Реализованные наследники:

- `CatCommand` - выводит содержимое файла на экран
- `EchoCommand` - выводит полученные на вход аргументы на экран
- `WcCommand` - выводит количество строк, слов и байт в переданном на вход файле
- `PwdCommand` - выводит текущую рабочую директорию
- `ExitCommand` - завершает работу интерпретатора
- `AssignCommand` - сохраняет в переменные окружения указанную переменную с указанным значением
- `UknownCommand` - передает выполнение неизвестной команды ядру ОС

### CommandExecutor

Принимает последовательность команд от `UserInputParser`. По длине последовательности определяет, кто должен выполнять
обработку команд:

- `SingleCommandExecutor` - исполняет одиночную команду, полученную на вход, и возвращает результат её работы;
- `PipeExecutor` - последовательно выполняет команды в последовательности команд, передавая поток вывода
  каждой команды в поток ввода следующей, и возвращает результат работы последней команды.

### CliContext

Хранит данные о текущих значениях переменных окружения. Поддерживает два метода:

- `get(variable)` - возвращает значение переменной окружения `variable`. Если такой переменной нет в контексте,
  возвращает пустую строку;
- `set(variable, value)` - присваивает переменной окружения `variable` значение `value`. Если переменной с таким
  названием нет, то создаст новую, иначе перетрет старое значение переданным.

___

## Дополнительные требования

### Строки

- Зарезервированные символы: `$`, `|`

- Weak Quoting (Слабое квотирование)\
  Используется двойными кавычками (`"`). Переменные окружения всё ещё могут быть подставлены внутри двойных кавычек.
  Например, `"Hello, $USER"` будет заменено на `Hello, username`, если переменная `USER` задана значением `username`.

- Full Quoting (Полное квотирование)\
  Используется одинарными кавычками (`'`). Все символы внутри одинарных кавычек воспринимаются буквально. Подстановка
  переменных и интерпретация специальных символов не производится. Это позволяет сохранять точное содержание строки без
  замены.

### Переменные окружения

Название переменной окружения обычно состоит из следующих символов:

- Буквы: Латинские буквы от A до Z (как заглавные, так и строчные — однако, в Unix-подобных системах обычно используются
  заглавные).
- Цифры: От 0 до 9. Однако цифры не могут стоять на первом месте в имени переменной.
- Знак подчеркивания (_): Часто используется для разделения слов в названии переменной.

Дополнительно:

* Имя переменной окружения не должно начинаться с цифры. Оно должно начинаться с буквы или знака подчеркивания
* Создание Переменной окружения возможно только отдельной командой
* Ее нельзя создать в рамках вызова pipe

### Исполнение встроенных и внешних команд:

После разбиения на команды и анализа, какие из них встроенные, а какие внешние:

- Если команда встроенная (например, `echo`, `cat`, `wc`), оркестратор напрямую вызывает ее исполнение, передавая ей
  параметры.
  ``` Command result = echoCommand.execute(); ```

- Если команда внешняя (например, системная утилита, как ls или grep), оркестратор запускает её как внешний процесс с
  помощью, например, fork

