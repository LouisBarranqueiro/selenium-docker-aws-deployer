# selenium-docker-aws-deployer

A script using selenium API to deploy on AWS an application embedded in a Docker container. **It deploy your application for free in minutes without commands only via the interfaces of web applications** :)

## General

* Author : Louis Barranqueiro

## Requirements

* Python v2.7 
* PIP
* A GitHub account
* A DockerHub account
* A Tutum account
* An AWS account with a credit card configured  (**your card will not be used during this process**)

## Deployment setup

```json
{
    "gitHub":    {
        "url":               "https://github.com/",
        "credentials":       {
            "name":     "",
            "password": ""
        },
        "repository": {
            "name":  "django-docker-starter",
            "owner": "lbsb"
        }
    },
    "dockerHub": {
        "url":         "https://hub.docker.com/",
        "credentials": {
            "name":     "",
            "password": ""
        },
        "repository":  {
            "name":       "django-app-starter",
            "visibility": "public"
        }
    },
    "tutum":     {
        "url":         "",
        "credentials": {
            "email":    "",
            "password": ""
        },
        "node":        {
            "name": "django-node"
        },
        "service":     {
            "name": "django-starter-app",
            "port": "80"
        }
    },
    "aws":       {
        "url":         "http://console.aws.amazon.com/",
        "credentials": {
            "email":    "",
            "password": ""
        }
    }
}
```

Edit `config.json` to configure the deployer.
* **gitHub** :
    * **url** : URL of GitHub webapp
    * **credentials** :
        * **email** : your GitHub account email
        * **password** : your GitHub account password
    * **repository** : Repository which contains Dockerfile and app to be deployed
        * **owner** : owner of the starter repository
        * **name** : name of the starter repository
* **dockerHub** :
    * **url** : URL of DockerHub webapp
    * **credentials** :
        * **email** : your DockerHub account email
        * **password** : your DockerHub account password
    * **repository** :
        * **name** : name of the automated build repository
        * **visibility** : visibility of the automated build repository (private or public)
* **tutum** :
    * **url** : URL of Tutum webapp
    * **credentials** :
        * **email** : your Tutum account email
        * **password** : your Tutum account password
    * **node** : A node is a cluster. It can contains multiple services and containers
        * **name** : name of the node cluster
    * **service** : Multiple containers can be launched from a service
        * **name** : name of the service 
        * **port** : port of the service
* **aws** :
    * **url** : URL of AWS webapp
    * **credentials** :
        * **email** : your AWS account email
        * **password** : your AWS account password

## Steps

1. Login into GitHub
2. Fork the starter repository
3. Login into DockerHub
4. Create an automated build repository based on GitHub starter repository just forked
5. Login into AWS
6. Create tutum user in IAM AWS service and attach Full Access to EC2 AWS service
7. Login into Tutum
8. Link Tutum user created on AWS to Tutum account
9. Create a node (cluster) on EC2 AWS service (t2.micro [1 CPUs, 1GB RAM]) via Tutum 
10. Create a service with DockerHub image previously built via Tutum
11. Go on node ip to watch application just deployed on EC2 AWS service in live 

## License 

selenium-docker-aws-deployer is under [MIT License](https://github.com/LouisBarranqueiro/selenium-docker-aws-deployer/blob/master/LICENSE)
