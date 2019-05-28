from kubernetes import client, config
from os import path
import argparse
import time

def createService(apiInstance, namespace, name):
    spec = client.V1ServiceSpec(
        ports=[client.V1ServicePort(port=80,protocol="TCP",target_port=80)],
        selector={"name":name},
        type="ClusterIP"
    )
    body = client.V1Service(
        metadata=client.V1ObjectMeta(name="nginx"),
        spec=spec
    )
    apiResponse = apiInstance.create_namespaced_service(namespace="velero", body=body)


def main():
    config.load_kube_config()
    parser = argparse.ArgumentParser(description="Contains the resource type and action that has to be performed")
    parser.add_argument('--resourceType', help="Resource Type that has to be Used")
    parser.add_argument('--actionType', help="Resource action that has to performed")
    parser.add_argument('--resourceName', help="Resource Name")
    parser.add_argument('--imageName', help="Image Name that has to be deployed")
    parser.add_argument('--namespace', help="Kubernetes Namespace")
    parser.add_argument('--imageTag', help="Image Tag")

    args = parser.parse_args()
    print args.actionType
    api_instance = client.CoreV1Api()

    createService(api_instance, args.resourceName, args.namespace)
if __name__ == "__main__":
    main()