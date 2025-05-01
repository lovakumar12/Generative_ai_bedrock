import boto3
import botocore.config
import json

from datetime import datetime

##<s> start with and for llama3 models will USE [INST]
def blog_generate_using_bedrock(blogtopic:str)-> str:
    prompt=f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
    Assistant:[/INST]
    """
    
    body={
        "prompt":prompt,
        "max_gen_len":512,
        "temperature" :0.6,
        "top_p": 0.9
    }
    try:
        bedrock=boto3.client('bedrock-runtime',region="us-east-1",
        config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3}))
        
        response=bedrock.invoke_model(body=json.dumps(body),modelId="meta.llama3-70b-instruct-v1:0")
        
        response_content=response.get("body").read()
        response_data=json.loads(response_content)
        print(response_data)
        blog_details=response_data['generaton']
        return blog_details
    except Exception as e:
        print(f"error at generating blog {e}")
        return ""
    
    
def save_blog_details_s3(s3_key,s3_bucket,generate_blog):   
    s3=s3.bucket('s3')
    
    
    
def lanbda_handler(event,context):
    event=json.loads(event['body'])
    blog_topic=event['blog_topic']
    generate_blog=blog_generate_using_bedrock(blogtopic=blog_topic)
    if generate_blog:
        current_time=datetime.now().strftime('%H%M%S')
        s3_key=f"blog-output/{current_time}.txt"
        s3_bucket='aws_bedrock_course1'
        save_blog_details_s3(s3_key,s3_bucket,generate_blog)
        
        
    else:
        print("no blog was generated")

    return {
        "statusCode": 200,
        "body": json.dumps("blog generated successfully")
    }