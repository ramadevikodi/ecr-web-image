import boto3
import json

ssm = boto3.client('ssm')

def initialize_parameters(parameters, env):
    for name, value in parameters.items():
        parameter_name = f"/epo/core-services/{env}/{name}"
        ssm.put_parameter(
            Name=parameter_name,
            Value=value,
            Type='String',
            Overwrite=True
        )
    print("Parameter store initialized.")

def add_delta_parameters(parameters, env):
    for name, value in parameters.items():
        parameter_name = f"/epo/core-services/{env}/{name}"
        try:
            ssm.get_parameter(Name=parameter_name)
            print(f"Parameter {parameter_name} already exists. Skipping.")
        except ssm.exceptions.ParameterNotFound:
            ssm.put_parameter(
                Name=parameter_name,
                Value=value,
                Type='String'
            )
            print(f"Parameter {parameter_name} added.")

def update_parameters(parameters, env):
    for name, value in parameters.items():
        parameter_name = f"/epo/core-services/{env}/{name}"
        ssm.put_parameter(
            Name=parameter_name,
            Value=value,
            Type='String',
            Overwrite=True
        )
        print(f"Parameter {parameter_name} updated.")

# Example usage
parameters = {
    "dbmsurl": "http://localhost:5433",
    "port": "5433"
}
env = "dev"

initialize_parameters(parameters, env)
add_delta_parameters(parameters, env)
update_parameters(parameters, env)
def delete_parameters(parameter_names, env):
    for name in parameter_names:
        parameter_name = f"/epo/core-services/{env}/{name}"
        try:
            ssm.delete_parameter(Name=parameter_name)
            print(f"Parameter {parameter_name} deleted.")
        except ssm.exceptions.ParameterNotFound:
            print(f"Parameter {parameter_name} not found. Skipping.")

# Example usage
parameters_to_delete = ["dbmsurl", "port"]
env = "dev"

delete_parameters(parameters_to_delete, env)
