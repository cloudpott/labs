import json
import boto3
import xlrd
from io import BytesIO

s3_resource = boto3.client('s3')

def lambda_handler(event, context):
    id = event["id"]
    bucket_name = event["bucket_name"]
    file_path = event["file_path"]
    
    result = s3_resource.get_object(Bucket=bucket_name, Key=file_path)
    
    data = result["Body"].read()
    excel_bytes = BytesIO(data)
    book = xlrd.open_workbook(file_contents=excel_bytes.read())
    sheet = book.sheet_by_index(0)
    for row in range(1, sheet.nrows):
        id_actual = int(sheet.cell_value(row, 0))
        if id==id_actual:
            price = sheet.cell_value(row, 2) 
            return {
                'statusCode': 200,
                'body': {"precio": price}
            }
    return {
        'statusCode': 200,
        'body': json.dumps('Product id not found')
    }
