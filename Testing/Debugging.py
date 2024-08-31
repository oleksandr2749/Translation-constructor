import Process
from Process import run
import ModificationClass
from pathlib import Path
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

data, file_type = Process.def_process(Process.read_xml('/home/oleksandr/294100/2975771801/1.5/Defs/NetDefs/NeutroamineNet.xml'))
for i in data.iter():
    print(i.tag)
Process.xml_file_write(data, Path('/home/oleksandr/Desktop/MyProgram')/file_type, name='Тест')
