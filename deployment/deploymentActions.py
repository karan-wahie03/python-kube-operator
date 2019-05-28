from kubernetes import client, config
from os import path
import argparse
import time



def createDeploymentConfig(name, namespace, replicas, image):
    container = client.V1Container(
        name="nginx",
        image="nginx:1.7.9",
        ports= [client.V1ContainerPort(container_port=80)]
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"name":name}),
        spec=client.V1PodSpec(containers=[container])
    )

    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=3,
        template=template
    )
    
    deployemnt = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec
    )

    return deployemnt


def createDeployment(apiInstance, deployment, namespace):
    apiResponse = apiInstance.create_namespaced_deployment(
        body=deployment,
        namespace="velero"
    )
    print("Deployment Created. Status = '%s'" %str(apiResponse.status))

def deleteDeployment(apiInstance, name, namespace):
    gracePeriodSeconds = 6
    apiVersion = "extensions/v1beta1"
    propagationPolicy = "Foreground"
    body = client.V1DeleteOptions(grace_period_seconds=gracePeriodSeconds,
                                     propagation_policy=propagationPolicy)
    try:
        apiResponse = apiInstance.delete_namespaced_deployment(name=name, namespace=namespace, body=body)
        print ("Deployment is deleting. Status = '%s'" %str(apiResponse.status))
    except:
        print "Error Deleting Deployment"   




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

    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    deployment = createDeploymentConfig()

    createDeployment(extensions_v1beta1, deployment)
    time.sleep(10)
    deleteDeployment(extensions_v1beta1, args.resourceName, args.namespace)


if __name__ == "__main__":
    main()