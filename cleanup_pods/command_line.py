import argparse
from kubernetes import client, config


def delete_pod(name, namespace):
    core_v1 = client.CoreV1Api()
    delete_options = client.V1DeleteOptions()
    api_response = core_v1.delete_namespaced_pod(
        name=name,
        namespace=namespace,
        body=delete_options)
    print(api_response)


def cleanup(args):
    config.load_kube_config()
    core_v1 = client.CoreV1Api()
    pod_list = core_v1.list_namespaced_pod(args.namespace)
    for pod in pod_list.items:
        if pod.status.phase.lower() in ['failed', 'success'] or (
                pod.status.reason and pod.status.reason.lower() == 'evicted'):
            print(pod.status.phase)
            print(pod.status.reason)
            delete_pod(pod.name, args.namespace)


def main():
    parser = argparse.ArgumentParser(description='Clean up k8s pods in evicted/failed/succeeded states.')
    parser.add_argument('--namespace', dest='namespace', default='default', type=str,
                        help='Namespace')
    args = parser.parse_args()
    cleanup(args)
