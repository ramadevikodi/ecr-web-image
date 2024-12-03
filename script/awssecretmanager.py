import boto3
import json

def initialize_secret_store(secrets, env, region_name):
    client = boto3.client('secretsmanager', region_name=region_name)
    responses = []
    
    for secret_name, secret_value in secrets.items():
        full_secret_name = f"/epo/core-services/{env}/{secret_name}"
        try:
            response = client.create_secret(
                Name=full_secret_name,
                SecretString=json.dumps(secret_value)
            )
            responses.append(response)
        except client.exceptions.ResourceExistsException:
            response = update_secret(full_secret_name, secret_value, region_name)
            responses.append(response)
        except Exception as e:
            responses.append(str(e))
    
    return responses

def add_delta_secrets(delta_secrets, env, region_name):
    client = boto3.client('secretsmanager', region_name=region_name)
    responses = []
    
    for secret_name, secret_value in delta_secrets.items():
        full_secret_name = f"/epo/core-services/{env}/{secret_name}"
        try:
            response = client.create_secret(
                Name=full_secret_name,
                SecretString=json.dumps(secret_value)
            )
            responses.append(response)
        except client.exceptions.ResourceExistsException:
            # If the secret already exists, skip it
            responses.append(f"Secret {full_secret_name} already exists.")
        except Exception as e:
            responses.append(str(e))
    
    return responses

def update_secret(secret_name, new_secret_value, region_name):
    client = boto3.client('secretsmanager', region_name=region_name)
    
    try:
        response = client.update_secret(
            SecretId=secret_name,
            SecretString=json.dumps(new_secret_value)
        )
        return response
    except Exception as e:
        return str(e)

# Example usage
env = "dev"
region_name = "us-west-2"

# Initialize the secret store from scratch
initial_secrets = {
    "db_username": "admin",
    "db_password": "password123"
}
initialize_responses = initialize_secret_store(initial_secrets, env, region_name)
print("Initialize Responses:", initialize_responses)

# Add only delta secrets during subsequent run
delta_secrets = {
    "api_key": "new_api_key_456"
}
delta_responses = add_delta_secrets(delta_secrets, env, region_name)
print("Delta Responses:", delta_responses)

# Update values of existing secrets
update_responses = []
for secret_name, new_secret_value in initial_secrets.items():
    full_secret_name = f"/epo/core-services/{env}/{secret_name}"
    response = update_secret(full_secret_name, new_secret_value, region_name)
    update_responses.append(response)

print("Update Responses:", update_responses)
def delete_secret(secret_name, region_name):
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        # Delete the secret
        response = client.delete_secret(
            SecretId=secret_name,
            ForceDeleteWithoutRecovery=True  # This permanently deletes the secret
        )
        return response
    except Exception as e:
        return str(e)

# Define the secret name and region
secret_name = "/epo/core-services/dev/db_password"
region_name = "us-east-1"  # Specify the AWS region

# Delete the secret and load the response
response = delete_secret(secret_name, region_name)
print(response)
