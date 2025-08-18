#!/usr/bin/env python3


def test_batch_logic():
    lines = ["Короткая", "Средняя строка", "Длинная строка с текстом"]
    batch = []
    current_length = 0
    BATCH_LIMIT = 1200

    for i, line in enumerate(lines):
        line_length = len(line)
        batch.append({"line_number": i + 1, "line": line})
        current_length += line_length

        if current_length > BATCH_LIMIT:
            batch.pop()
            break

    print(f"Батч: {batch}")
    print(f"Длина: {current_length}")


if __name__ == "__main__":
    test_batch_logic()
