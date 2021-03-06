##################################################
# HemeraService_services_server.py
#
##################################################

from HemeraService_services import *
from ZSI.ServiceContainer import ServiceSOAPBinding

class HemeraService(ServiceSOAPBinding):
    soapAction = {}
    root = {}
    _wsdl = """<?xml version=\"1.0\" ?>
<definitions name=\"HemeraService\" targetNamespace=\"http://169.254.3.230:8080/HemeraService\" xmlns=\"http://schemas.xmlsoap.org/wsdl/\" xmlns:soap=\"http://schemas.xmlsoap.org/wsdl/soap/\" xmlns:tns=\"http://169.254.3.230:8080/HemeraService\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">

    <message name=\"proveRequest\">
        <part name=\"formula\" type=\"xsd:string\"/>
    </message>
    <message name=\"proveResponse\">
        <part name=\"return\" type=\"xsd:string\"/>
    </message>

    <portType name=\"HemeraPortType\">
        <operation name=\"prove\">
            <documentation> the prove method </documentation>
            <input message=\"tns:proveRequest\"/>
            <output message=\"tns:proveResponse\"/>
        </operation>
    </portType>

    <binding name=\"HemeraBinding\" type=\"tns:HemeraPortType\">
        <soap:binding style=\"rpc\" transport=\"http://schemas.xmlsoap.org/soap/http\"/>
        <operation name=\"prove\">
            <soap:operation soapAction=\"http://169.254.3.230:8080/HemeraService/prove\"/>
            <input>
                <soap:body namespace=\"http://169.254.3.230:8080/HemeraService\" use=\"literal\"/>
            </input>
            <output>
                <soap:body namespace=\"http://169.254.3.230:8080/HemeraService\" use=\"literal\"/>
            </output>
        </operation>
    </binding>

    <service name=\"HemeraService\">
        <documentation>Try to prove a theorem</documentation>
        <port binding=\"tns:HemeraBinding\" name=\"HemeraPort\">
            <soap:address location=\"http://169.254.3.230:8080/HemeraService\"/>
        </port>
    </service>

</definitions>"""

    def __init__(self, post='/HemeraService', **kw):
        ServiceSOAPBinding.__init__(self, post)

    def soap_prove(self, ps):
        self.request = ps.Parse(proveRequest.typecode)
        return proveResponse()

    soapAction['http://169.254.3.230:8080/HemeraService/prove'] = 'soap_prove'
    root[(proveRequest.typecode.nspname,proveRequest.typecode.pname)] = 'soap_prove'

