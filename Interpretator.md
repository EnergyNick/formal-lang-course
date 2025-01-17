# Интерпретатор

Позволяет выполнять код программы сформированный языком графовых запросов.
Описание языка находится [в файле Language](Language.md)

## Система типов

Система типов является строгой динамической, не ленивой.
Переменные являются не изменяемые и любые модифицирующие операции создают копии значений.

Доступные типы перечислены ниже:
- `Int` = Универсальное целое число
- `Bool` = Булевое значение
- `String` = Строковое значение
- `EpsilonNFA` = Недетерминированный конечный автомат, реализация из `pyformlang`.
- `Set` = Универсальное множество типовых значений

Язык поддерживает множество различных типовых операций:
- Числовую арифметику
- Операции пересечения/объединений над НКА
- Получение информации об элементах НКА
- и др.

## Запуск

Программа воспринимает аргументы переданные её из командной строки.
Возможно передать как путь до файла, так и текст программы целиком.

Пример программы из файла `test.lang`.
```
var temp = "Hello, Formals!";
show temp;
```

Чтобы запустить программу в консоли необходимо выполнить:

```shell
python -m project test.lang
```

либо

```shell
cat test.lang | python -m project -
```
