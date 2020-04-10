import argparse
import logging

from kubernetes import client, config
from kubernetes.client.rest import ApiException

# https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
# All Containers in the Pod have terminated in success, and will not be restarted.
POD_SUCCEEDED = 'succeeded'

# All Containers in the Pod have terminated, and at least one Container has terminated in failure.
# That is, the Container either exited with non-zero status or was terminated by the system.
POD_FAILED = 'failed'

# https://kubernetes.io/docs/tasks/administer-cluster/out-of-resource/
POD_REASON_EVICTED = 'evicted'
# If pod is failed and
# restartPolicy is:
# * Always: Restart Container; Pod phase stays Running.
# * OnFailure: Restart Container; Pod phase stays Running.
# * Never: Pod phase becomes Failed.
POD_RESTART_POLICY_NEVER = 'never'


def delete_pod(name, namespace):
    core_v1 = client.CoreV1Api()
    delete_options = client.V1DeleteOptions()
    logging.warning('Deleting POD "{name}" from "{namespace}" namespace'.format(
        name=name, namespace=namespace
    ))
    api_response = core_v1.delete_namespaced_pod(
        name=name,
        namespace=namespace,
        body=delete_options)
    logging.warning(api_response)


def cleanup(namespace):
    logging.info('Loading Kubernetes configuration')
    config.load_incluster_config()
    logging.debug('Initializing Kubernetes client')
    core_v1 = client.CoreV1Api()
    logging.info('Listing namespaced pods in namespace {namespace}'.format(namespace=namespace))
    pod_list = core_v1.list_namespaced_pod(namespace)
    for pod in pod_list.items:
        logging.info('Inspecting pod {pod}'.format(pod=pod.metadata.name))
        pod_phase = pod.status.phase.lower()
        pod_reason = pod.status.reason.lower() if pod.status.reason else ''
        pod_restart_policy = pod.spec.restart_policy.lower()

        if (pod_phase == POD_SUCCEEDED or
           (pod_phase == POD_FAILED and pod_restart_policy == POD_RESTART_POLICY_NEVER) or
           (pod_reason == POD_REASON_EVICTED)):

            logging.info('Deleting pod "{}" phase "{}" and reason "{}", restart policy "{}"'.format(
                pod.metadata.name, pod_phase, pod_reason, pod_restart_policy)
            )
            try:
                delete_pod(pod.metadata.name, namespace)
            except ApiException as e:
                logging.error("can't remove POD: {}".format(e))
                continue
        logging.info('No action take on pod {pod}'.format(pod=pod.metadata.name))


def main():
    parser = argparse.ArgumentParser(description='Clean up k8s pods in evicted/failed/succeeded states.')
    parser.add_argument('--namespace', dest='namespace', default='default', type=str,
                        help='Namespace')
    args = parser.parse_args()
    cleanup(args.namespace)
