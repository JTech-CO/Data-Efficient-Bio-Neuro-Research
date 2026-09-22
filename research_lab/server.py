"""Loopback-only research server. Static mode remains usable on GitHub Pages."""
from __future__ import annotations
import json, threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from .contracts import RunConfig
from .runner import run_experiment, ROOT

_RUN_LOCK=threading.Lock()

class LabHandler(SimpleHTTPRequestHandler):
    def send_json(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,allow_nan=False).encode('utf-8')
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)

    def trusted_host(self):
        port=self.server.server_address[1]
        return self.headers.get('Host') in (f'127.0.0.1:{port}',f'localhost:{port}')

    def do_GET(self):
        if not self.trusted_host():return self.send_json(403,{'error':'Loopback Host header required'})
        if self.path=='/api/status':
            return self.send_json(200,{'mode':'local-research','research_only':True,'real_data_enabled':False,'version':'0.1.0'})
        return super().do_GET()

    def do_POST(self):
        if not self.trusted_host():return self.send_json(403,{'error':'Loopback Host header required'})
        if self.path!='/api/run':return self.send_json(404,{'error':'Unknown endpoint'})
        host=self.headers.get('Host','')
        if self.headers.get('Origin') not in (None,f'http://{host}'):
            return self.send_json(403,{'error':'Same-origin request required'})
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':
            return self.send_json(415,{'error':'JSON required'})
        try: size=int(self.headers.get('Content-Length','0'))
        except ValueError:return self.send_json(400,{'error':'Invalid length'})
        if not 0<size<=4096:return self.send_json(413,{'error':'Body size must be 1..4096 bytes'})
        try:
            body=json.loads(self.rfile.read(size))
            allowed={'scenario','policy','seed','budget','observer'}
            if not isinstance(body,dict) or not set(body)<=allowed:
                raise ValueError('Only experiment settings are accepted; uploads and paths are not supported')
            cfg=RunConfig(**body)
        except (ValueError,TypeError,KeyError) as exc:
            return self.send_json(400,{'error':str(exc)})
        if not _RUN_LOCK.acquire(blocking=False):return self.send_json(409,{'error':'Another local run is in progress'})
        try:
            self.send_json(200,run_experiment(cfg))
        except Exception:
            self.send_json(500,{'error':'Experiment failed; inspect the local terminal'})
            raise
        finally:_RUN_LOCK.release()

    def log_message(self,fmt,*args):
        # Local process console only. No telemetry or remote logging.
        super().log_message(fmt,*args)

def make_server(port=8765):
    return ThreadingHTTPServer(('127.0.0.1',port),partial(LabHandler,directory=str(ROOT)))

def serve(port=8765):
    server=make_server(port)
    print(f'Research-only server: http://127.0.0.1:{server.server_address[1]}/research_lab/web/',flush=True)
    print('No external network, uploads, model downloads, or real experiment execution.',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
