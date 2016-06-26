import json
import traceback

from twisted.web import resource

from pygear.logging import log


class JsonResource(resource.Resource):
    json_encoder = json.JSONEncoder()

    def render(self, txrequest):
        r = resource.Resource.render(self, txrequest)
        return self.render_object(r, txrequest)

    def render_object(self, obj, txrequest):
        r = self.json_encoder.encode(obj) + "\n"
        txrequest.setHeader('Content-Type', 'application/json')
        txrequest.setHeader('Access-Control-Allow-Origin', '*')
        txrequest.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE')
        txrequest.setHeader('Access-Control-Allow-Headers', ' X-Requested-With')
        txrequest.setHeader('Content-Length', len(r))
        return r


class WsResource(JsonResource):
    def __init__(self, root):
        JsonResource.__init__(self)
        self.root = root
        if not hasattr(root, 'nodename'):
            self.root.nodename = 'JsonWebservice'

    def render(self, txrequest):
        try:
            return JsonResource.render(self, txrequest)
        except Exception as e:
            if self.root.debug:
                return traceback.format_exc()
            log.err()
            r = {"node_name": self.root.nodename, "status": "error", "message": str(e)}
            return self.render_object(r, txrequest)