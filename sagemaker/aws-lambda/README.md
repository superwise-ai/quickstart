# Superwise.ai Python SDK - AWS Lambda integration

### A python SDK to integrate with superwise.ai via AWS lambda function

In order to use this library you need:

```
python > 3.0
```

### Install

1. Create an Amazon S3 bucket
2. Create a Lambda function based on `s3-get-object-python` blueprint
3. S3 trigger configuration:
    - Bucket - Choose the S3 bucket that you created previously
    - Event type - `All object create events`
    - Suffix - Depends on the type of files (`.paruqet`, `.csv`)
4. After creating the Lambda function, upload the the `artifacts/sw-aws-lambda.zip` file
5. Config the following env vars - `SUPERWISE_CLIENT_ID`, `SUPERWISE_SECRET`, `SUPERWISE_CLIENT_NAME`
    
AWS reference: https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
    

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).


For getting started, HOWTOs, jupyter notebooks examples etc, use Superwise documentation portal:  https://docs.superwise.ai/


## License
The Superwise.ai SDK released under MIT licence (See LICENSE file)