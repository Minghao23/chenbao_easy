from hash_ring import HashRing
from kazoo.client import KazooClient
import requests
import json
import os

ZK_SERVERS = '192.168.1.15:2181'
ZK_APP_NODE = '/cn/yottabyte/kpi_analyzer'
MY_HOST = '127.0.0.1'
MY_PORT = '8014'
MAX_RETRIES = 3


class Node(object):

    def __init__(self, name, host=None, port=None, partition=None):
        self.name = name
        self.host = host
        self.port = port
        self.partition = partition

    def gen_url(self, path):
        return "http://%s:%s/%s" % (self.host, self.port, path.strip('/'))


class RequestDispatcher(object):

    def __init__(self):
        self._zk = KazooClient(hosts=ZK_SERVERS)
        self._zk.start()
        # check if app node exists, or initialize node
        self.heartbeat_node = os.path.join(ZK_APP_NODE, 'heartbeat')
        self._zk.ensure_path(self.heartbeat_node)
        self._register_zk()

        self.nodes = {}
        self.hash_ring = None
        self._update_nodes()

    def _register_zk(self):
        import uuid
        # generate a random node name
        self.node_name = 'KPIA_ephemeral_node_%s' % uuid.uuid1()
        node_path = os.path.join(self.heartbeat_node, self.node_name)
        value = json.dumps({'host': MY_HOST, 'port': MY_PORT})
        self._zk.create(node_path, value, ephemeral=True)

    def _update_nodes(self, event=None):
        """
        Use zookeeper watcher to listen the change of heartbeat children nodes
        Notice that watcher will be cancelled after being triggered, so define the watcher recursively
        :param event: default to None, means monitoring node creation or deletion
        """
        nodes_unicode = self._zk.get_children(self.heartbeat_node, watch=self._update_nodes)
        nodes_str = map(str, nodes_unicode)
        self.nodes.clear()
        for node in nodes_str:
            node_value = json.loads(self._zk.get(os.path.join(self.heartbeat_node, node))[0])
            self.nodes[node] = Node(node, node_value['host'], node_value['port'])
        self._update_hash_ring()

    def _update_hash_ring(self):
        self.hash_ring = HashRing(self.nodes.keys())

    def get_node(self, key):
        target_node_name = self.hash_ring.get_node(key)
        if target_node_name is None:
            return None
        return self.nodes[target_node_name]

    def _request_redirect(self, request, target_node):
        """
        Dispatch request to another distributed node and return corresponding HttpResponse
        """
        if target_node.name == self.node_name:
            raise RuntimeError("Can't dispatch request to self node")
        from django.http import HttpResponse
        body = request.body
        headers = {'content-type': request.content_type}
        url = target_node.gen_url(request.path)
        response = requests.request("POST", url, data=body, headers=headers)
        return HttpResponse(response.content, content_type=response.headers['content-type'])

    def dispatch(self, request, key, view_func):
        target_node = self.get_node(key)
        if target_node is None:
            raise RuntimeError("No available node to handle request, request failed.")
        if target_node.name == self.node_name:
            return view_func(request)
        i = 0
        while i < MAX_RETRIES:
            try:
                resp = self._request_redirect(request, target_node)
                print "Request %s with key=%s is dispatched into <Node %s:%s> based on hashing rules." \
                      % (request.path, key, target_node.host, target_node.port)
                return resp
            except requests.exceptions.RequestException:
                i += 1
        if i == MAX_RETRIES:
            # case that target node has broken down
            del self.nodes[target_node.name]
            self._update_hash_ring()
            print "Max retries exceeded with url: %s, target node: <Node %s:%s>, try another node..." \
                  % (request.path, target_node.host, target_node.port)
            return self.dispatch(request, key, view_func)


# Initialize dispatcher
# req_disp = RequestDispatcher()


# def test_distribution(request):
#     id = json.loads(request.body)['id']
#     from views import test_distribution as view_test_distribution
#     return req_disp.dispatch(request, 'model_%d' % id, view_test_distribution)


# RequestDispatcher()
# import time
# time.sleep(1000)
zk = KazooClient(hosts='192.168.1.15:2181')
zk.start()
print zk.get_children('/cn/yottabyte/kpi_analyzer/heartbeat')
# print zk.get('/cn/yottabyte/kpi_analyzer/heartbeat/KPIA_ephemeral_node_6fd3bc10-3849-11ea-ab8b-5254001a71c4')
# print zk.get('/cn/yottabyte/kpi_analyzer/heartbeat/KPIA_ephemeral_node_c40045c0-384b-11ea-830b-8c8590a405aa')