from unittest import mock

from cleanup_pods.command_line import delete_pod


@mock.patch('kubernetes.client.CoreV1Api.delete_namespaced_pod')
def test_delete_pod(delete_namespaced_pod):
    delete_pod('dummy', 'awesome-namespace')
    delete_namespaced_pod.assert_called_with(
        body=mock.ANY, name='dummy', namespace='awesome-namespace'
    )
