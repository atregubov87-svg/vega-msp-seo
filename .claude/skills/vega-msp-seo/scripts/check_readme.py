#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка README.md публичного кейса vega-msp-seo.

Запуск из корня репозитория:
    python .claude/skills/vega-msp-seo/scripts/check_readme.py
"""
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## 1. Название",
    "## 2. Проблема",
    "## 3. Пользователь",
    "## 4. Основная функция",
    "## 5. Формат результата",
    "## 6. Минимальный функционал",
    "## 7. Технологии",
    "## Результаты в цифрах",
    "## Безопасность публикации",
    "## Автор",
]

FORBIDDEN = [
    ("секретный заголовок API", r"X-Vega"),
    ("слово Secret в значении", r"\bSecret\b"),
    ("внутренний IP", r"\b192\.168\."),
    ("endpoint WordPress", r"wp-json"),
    ("внутреннее представление МИС", r"v_kiosk"),
    ("внутренняя схема БД", r"\bdbo\."),
    ("ID счётчика Метрики", r"\b114093862\b"),
    ("служебный IP", r"\b89\.22\."),
    ("присваивание пароля", r"(?i)(password|пароль)\s*[:=]"),
    ("присваивание токена", r"(?i)(token|токен)\s*[:=]"),
    ("присваивание API-ключа", r"(?i)api[_-]?key\s*[:=]"),
    ("служебный email", r"(?i)\b(info|it)@"),
    ("локальный путь", r"(?i)[A-Z]:[\\/](?:ClaudeCode|Users)[\\/]"),
    ("старый GitHub username", r"atregubov87(?!-svg)"),
]


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("README.md")
    if not path.exists():
        print(f"ERROR: файл не найден: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    errors = []

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"нет обязательного раздела: {heading}")

    for label, pattern in FORBIDDEN:
        for match in re.finditer(pattern, text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{label}: строка {line}: {match.group(0)[:60]!r}")

    if errors:
        print(f"ERROR: найдено {len(errors)} проблем:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: {path} — структура и проверки пройдены")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
