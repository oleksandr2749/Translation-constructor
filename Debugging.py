from Process import run
import ModificationClass
import pathlib
import logging

logging.addLevelName(logging.DEBUG, 'НАЛАГОДЖЕННЯ')
logging.addLevelName(logging.INFO, 'ІНФ.')
logging.addLevelName(logging.WARNING, 'УВАГА')
logging.addLevelName(logging.ERROR, 'ПОМИЛКА')
logging.addLevelName(logging.CRITICAL, 'КРИТИЧНА ПОМИЛКА')
logging.basicConfig(
    filename='program.log',
    encoding='utf-8',
    filemode='w',

    format='{asctime} {levelname} - {message}',
    style='{',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.DEBUG
)

# logging.debug('Перевірка')
# logging.info('Перевірка')
# logging.warning('Перевірка')
# logging.error('Перевірка')
# logging.critical('Перевірка')
# logging.debug("name=%s", name)

ModList = ModificationClass.create_mod_list(ModificationClass.search_294100_folder())

for mod in ModList:
    if mod.published_file_Id == '3262718980':
        run(modification=mod,
            export_path=pathlib.Path('/home/oleksandr/Desktop/MyProgram'))
