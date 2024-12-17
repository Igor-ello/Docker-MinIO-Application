# Вспомогалка

## Запуск
```
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
kubectl get pods
```

## Проброс порта
```
kubectl port-forward svc/flask-app1-service 5000:5000
```