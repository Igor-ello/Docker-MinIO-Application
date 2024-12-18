# Вспомогалка

## Запуск
```
minikube start
kubectl apply -f minio-deployment.yaml
kubectl apply -f app1/flask-app1-deployment.yaml
kubectl apply -f app2/flask-app2-deployment.yaml
```

## Пересборка
```
delete -f app1/flask-app1-deployment.yaml
kubectl apply -f app1/flask-app1-deployment.yaml

delete -f app2/flask-app2-deployment.yaml
kubectl apply -f app2/flask-app2-deployment.yaml
```

## Проверка статуса контейнеров
```
minikube status
kubectl get pods
kubectl get services
kubectl get nodes -o wide 
```

## Проброс порта
```
kubectl port-forward svc/flask-app1-service 5000:5000
```

## Пуш на DockerHub
```
docker tag flask-app1:latest ig0rello/flask-app1:latest
docker push ig0rello/flask-app1:latest
docker tag flask-app2:latest ig0rello/flask-app2:latest
docker push ig0rello/flask-app2:latest
```
