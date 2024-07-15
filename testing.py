from pathlib import Path


def search_294100_folder():
    # Створюємо список кореневих каталогів для пошуку
    root_paths = []
    for p in Path('/').glob('*'):
        if p.is_dir():
            root_paths.append(Path(p))
            print(p)

    for root in root_paths:
        for path in root.rglob('Steam/steamapps/workshop/content/294100'):
            return path.resolve()

    return None  # Повертаємо None, якщо шлях не знайдено


print(search_294100_folder())
