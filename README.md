# ResearchProject
Mlops, cloud, cybersecurity

Sure! Here's a simple `README.md` file for your project:

```markdown
# My Flask App

This is a Flask application that serves the ML model.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Docker installed on your machine

### Building the Docker Image

To build the Docker image for the Flask app, run the following command:

```sh
docker build -t my_flask_app .
```

### Running the Docker Container

To run the Docker container, use the following command:

```sh
docker run -it -p 5000:5000 my_flask_app
```

This will start the Flask app and make it accessible at `http://localhost:5000`. http://192.168.0.103:8080/

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used

```sh
docker build -t my_flask_app .
docker tag my_flask_app rpcybersecurityappacr.azurecr.io/my_flask_app:v1
docker push rpcybersecurityappacr.azurecr.io/my_flask_app:v1

kubectl exec -it flask-app-549bfb6f4c-twltl -- curl http://localhost:5000

az aks stop --resource-group flaskAppResourceGroup --name flaskAppAKSCluster

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl get services
kubectl get svc -n monitoring
kubectl get nodes -o wide
kubectl logs flask-app-549bfb6f4c-7gx8k
http://135.237.7.218

```