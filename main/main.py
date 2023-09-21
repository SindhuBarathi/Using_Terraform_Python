from google.cloud import storage
from datetime import datetime

landingBucket = 'landing-bucket1'
rawBucket = 'raw-bucket2'
errorBucket = 'error-bucket3'
StorageClient = storage.Client()
# .from_service_account_json('credentials.json')


def main(event :dict, context):
    filename = event["name"]
    verify = verifyFile(filename)

    if verify:
        print("moved")
    else:
        print("error")


def verifyFile(file :str):
    if file.startswith('customer_details') and file.endswith('.psv') and len(file) == 20:
        moveFile(file,"correct")
        return True
    else:
        moveFile(file, 'error')
    return False

def moveFile(file :str, status :str):
    fileIncurrentBucket = StorageClient.bucket(landingBucket)

    if status == 'error':
        try:
            fileInNextBucket = StorageClient.bucket(errorBucket)
            object = fileIncurrentBucket.blob(file)
            fileIncurrentBucket.copy_blob(object, fileInNextBucket, file)
            fileIncurrentBucket.delete.blob(file)
            return
    
        except:
            print("Error")

    else:
        try:
            fileInNextBucket = StorageClient.bucket(rawBucket)
            object = fileIncurrentBucket.blob(file)
            fileIncurrentBucket.copy_blob(object, fileInNextBucket, newFileName(name=file))
            fileIncurrentBucket.delete_blob(file)
            return
        except:
            print("Error")

def newFileName(name :str) -> str:
    date = datetime.now()

    day = date.date().day
    month = date.date().month
    year = date.date().year
    hour = date.time().hour
    minute = date.time().minute
    second = date.time().second

    split_filename = name.split(" ")
    new_filename = split_filename[0] + str(day) + "_" + str(month) + "_" + str(year) + "_" + str(hour)+ "_" + str(minute) + "_" + str(second)
    return new_filename