################################################## 
# HemeraService_services.py 
#
##################################################



import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# The web service Locator classe used by clients
# to access the web service.
class HemeraServiceLocator:
    HemeraPortType_address = "http://169.254.3.230:8080/HemeraService"
    def getHemeraPortTypeAddress(self):
        return HemeraServiceLocator.HemeraPortType_address
    def getHemeraPortType(self, url=None, **kw):
        return HemeraBindingSOAP(url or HemeraServiceLocator.HemeraPortType_address, **kw)

# SOAP useful methods implemented as python classes.
class HemeraBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: prove
    def prove(self, request):
        if isinstance(request, proveRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://169.254.3.230:8080/HemeraService/prove", **kw)
        # no output wsaction
        response = self.binding.Receive(proveResponse.typecode)
        return response

# The SOAP Request
class proveRequest:
    def __init__(self):
        self._formula = None
        return
proveRequest.typecode = Struct(pname=("http://169.254.3.230:8080/HemeraService","prove"), ofwhat=[ZSI.TC.String(pname="formula", aname="_formula", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=proveRequest, encoded="http://169.254.3.230:8080/HemeraService")

# The SOAP Response
class proveResponse:
    def __init__(self):
        self._return = None
        return
proveResponse.typecode = Struct(pname=("http://169.254.3.230:8080/HemeraService","proveResponse"), ofwhat=[ZSI.TC.String(pname="return", aname="_return", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=proveResponse, encoded="http://169.254.3.230:8080/HemeraService")
