import urllib.parse

from superwise import Superwise

sw = Superwise()


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
      event['Records'][0]['s3']['object']['key'], encoding='utf-8'
    )
    path = f"s3://{bucket}/{key}"
    try:
      sw.data.log_file(path)
    except Exception as e:
        print(e)
        print('Error notify superwise - file {}'.format(path))
