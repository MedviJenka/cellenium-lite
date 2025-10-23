#!/bin/bash

namespace="hello-namespace"
minikube start
kubectl create deployment bini-cluster --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8081
kubectl get pods
kubectl expose deployment bini-cluster --type=NodePort --port=8081
kubectl get services
minikube enable metric-service

kubectl get pod, svc -n kube-system
kubectk top pods
