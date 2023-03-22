# импортирование нужных библиотек
import threading
import boto3
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

# определение эндпоинта и учетных данных
S3_ENDPOINT_URL = ''
S3_ACCESS_KEY_ID = ''
S3_SECRET_ACCESS_KEY = ''

# создание S3 клиента
s3_client = boto3.client('s3',
                         endpoint_url=S3_ENDPOINT_URL,
                         aws_access_key_id=S3_ACCESS_KEY_ID,
                         aws_secret_access_key=S3_SECRET_ACCESS_KEY)


# обработка и загрузка файлов
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        # получение файла
        uploaded_file = request.FILES.get('file')

        # создание нового объекта в памяти с помощью Django Storage API
        file_object = default_storage.open('temp', 'w')
        file_object.write(uploaded_file.read())
        file_object.close()

        # Определяем размер файла в байтах
        file_size = uploaded_file.size

        # создание нового потока для загрузки файла в S3
        upload_thread = threading.Thread(target=upload_file_to_s3, args=(file_size,))
        upload_thread.start()

        # Возвращаем JSON
        return JsonResponse({'status': 'File upload started'})

    # Если метод запроса не POST или файл не был загружен
    return HttpResponseBadRequest()


# Загрузка файла в S3 в отдельном потоке
def upload_file_to_s3(file_size):
    s3_bucket = ''
    s3_key = ''

    # Достаем объект из памяти с помощью Django storage API
    file_object = default_storage.open('temp', 'r')

    # Передача файла в S3
    multipart_upload = s3_client.create_multipart_upload(Bucket=s3_bucket, Key=s3_key)
    part_number = 1
    while True:
        data = file_object.read(settings.FILE_UPLOAD_MAX_MEMORY_SIZE)
        if not data:
            break
        response = s3_client.upload_part(Body=data, Bucket=s3_bucket, Key=s3_key,
                                         UploadId=multipart_upload['UploadId'], PartNumber=part_number)
        part_number += 1

    # завершение загрузки
    s3_client.complete_multipart_upload(Bucket=s3_bucket, Key=s3_key,
                                        UploadId=multipart_upload['UploadId'],
                                        MultipartUpload={'Parts': [{'ETag': response['ETag'], 'PartNumber': i}
                                                                   for i in range(1, part_number)]})

    # удаление объекта из памяти
    default_storage.delete('temp')
