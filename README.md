# Test Task
[![vvs](https://c.tenor.com/R8wjCxS2MCgAAAAC/oreki-black-and-white-wind.gif)]()
## Usage:
you can clone this GitHub repository by using `gh repo clone vvsalwayscodin/uploading_large_files_to_S3_Django`

install requirements by using `pip install requirements.txt`

## Что я сделал?
1. Использовал библиотеку Dropzone.js для того чтобы отправлять файл из браузера клиента сразу в S3, чтобы уменшить нагрузку на серверную часть Django
2. Бэкенд эндпоинт получает файл и сразу отправляет его в S3, не сохраняя его на диск ВМ
3. Использовал несколько потоков для загрузки файла
