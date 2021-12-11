# RESTler

## What is RESTler?

RESTler is a fuzzing tool for automatically finding security and reliability bugs in RESTful services. For a given service
with an OpenAPI/Swagger specification, RESTler analyzes its entire specification, and then generates and executes tests that exercise the service through its REST API.

![RESTler architecture](./docs/user-guide/RESTler-arch.png)

## Setting up the environment

RESTler was designed to run on 64-bit machines with Windows or Linux. Running on macOS is not stable as it is in experimental process.

You need to install Python 3.8.2 (https://www.python.org/downloads/) and [.NET 5.0](https://dotnet.microsoft.com/download/dotnet-core?utm_source=getdotnetcorecli&utm_medium=referral). Be careful about the Python version, as it should be exact the same.

After installing the prerequisites, you should clone the [RESTler repository](https://github.com/microsoft/restler-fuzzer)

Create a folder called ```restler_bin``` in the RESTler directory.

The Server (PetClinic) should be up, so the RESTler can send requests and retrieve the responses. The RESTler produce grammers based on the OAS. You can get PetClinic Open API file from http://localhost:9966/petclinic/v2/api-docs or download it from the repo.
Save this file as ```api-docs.json```
