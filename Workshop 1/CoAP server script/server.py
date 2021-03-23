import sys
import getopt
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
from threading import Thread
from coapthon.server.coap import CoAP
from exampleresources import BasicResource


class Sensor(Resource):

    def __init__(self,name="Sensor",coap_server=None):
        super(Sensor,self).__init__(name,coap_server,visible=True,observable=True,allow_children=True)
        self.resource_type = "rt1"
        self.interface_type = "if1"
        self.payload = " "
        #self.resource_type = "rt1"
        self.content_type = "text/plain"
        #self.interface_type = "if1"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, BasicResource())
        return res

    def render_DELETE(self, request):
        return True

class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self,(host,port),multicast)
        self.add_resource('sensor/',Sensor())
        print("CoAP server started on {}:{}".format(str(host),str(port)))
        #print self.root.dump()


def main():
    ip = "192.168.1.101"
    port = 5683 
    multicast=False
    
    
    server = CoAPServer(ip,port)

    try:
        server.listen(10)
        print("executed after listen")
    except KeyboardInterrupt:
        print(server.root.dump())
        server.close()
        sys.exit()

if __name__=="__main__":
    main()
