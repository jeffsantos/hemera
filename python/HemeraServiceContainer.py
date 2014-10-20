#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

# ZSI 2.1 Infrastructure
from optparse import OptionParser
from ZSI.wstools import logging
from ZSI.ServiceContainer import AsServer
# ZSI 2.1 Generated Service Skeleton
from HemeraService_server import HemeraService
# Prover modules 
from Sequent import *
from svg import *
from grammar import SyntaxError
# Other libs
from datetime import date

# Create a Server implementation by inheritance
class HemeraServiceContainer(HemeraService):

    # Make WSDL available for HTTP GET
    _wsdl = "".join(open("HemeraService.wsdl").readlines())
    _proverMap = {}      

    '''
    SOAP Implementations:
    =======================================
    '''
    def soap_check_syntax(self, ps, **kw):
        request, response = HemeraService.soap_check_syntax(self, ps, **kw)
        response._return, response._msg = self.check_syntax(request._spec)
        return request, response
    
    def soap_start(self, ps, **kw):
        request, response = HemeraService.soap_start(self, ps, **kw)
        response._return, response._proofRepr, response._msg = self.start(request._id, request._spec)
        return request, response    
    
    def soap_step(self, ps, **kw):
        request, response = HemeraService.soap_step(self, ps, **kw)
        response._return, response._proofRepr, response._msg = self.step(request._id)
        return request, response
    
    def soap_run(self, ps, **kw):
        request, response = HemeraService.soap_run(self, ps, **kw)
        response._return, response._proofRepr, response._msg = self.run(request._id)
        return request, response    
    
    def soap_get_rules(self, ps, **kw):
        request, response = HemeraService.soap_get_rules(self, ps, **kw)
        response._return = self.get_rules(request._id, request._goal)
        return request, response    
    
    def soap_apply_rule(self, ps, **kw):
        request, response = HemeraService.soap_apply_rule(self, ps, **kw)
        response._return, response._proofRepr, response._msg = self.apply_rule(request._id, request._goal, request._ruleId)
        return request, response            
    
    def soap_prove(self, ps, **kw):
        request, response = HemeraService.soap_prove(self, ps, **kw)
        response._return = self.prove(request._formula)
        return request, response        

    '''
    Delegates:
    =======================================
    '''
    def check_syntax(self, spec):
        print "Checking Syntax of the following specification: " + spec
        try:
            s = "read " + spec
            cmd = yacc.parse(s)
        except SyntaxError, e:
            msg = e.value
            return False, msg
        else:
            return True, ""        
        
    def start(self, id, spec):
        print "Starting proof process for user_id " + id + ". Trying to prove " + spec
        ret, msg = self.check_syntax(spec)
        if ret:
            return self.exec_prover_cmd(id, "read " + spec)
        else:                   
            return ret, "", msg            
        
    def step(self, id):
        print "Running a step of the prover process for user_id " + id
        return self.exec_prover_cmd(id, "step")         
    
    def run(self, id):        
        print "Running all steps of the prover process for user_id " + id
        return self.exec_prover_cmd(id, "run")   
     
    def get_rules(self, id, goal):        
        print "Getting applicable rules in goal " + goal + " for user_id " + id
        prover = self.get_prover_instance(id)
        rules = prover.get_goal_applicable_rules(goal)
        return rules 

    def apply_rule(self, id, goal, ruleId):        
        print "Applying rule in goal " + goal + " for user_id " + id
        try:
            prover = self.get_prover_instance(id)
            prover.apply_rule_to_goal(goal, ruleId)
            cmdParsed = yacc.parse("print")
            proofRepr = prover.eval(cmdParsed)            
        except Exception, inst:
            msg = inst.__str__()
            return False, "", msg 
        else:
            return True, parseToSVG(proofRepr), prover.finalStatus                
    
    
    '''
    Helpers:
    =======================================
    '''    
    def get_prover_instance(self, id):
        if (id in self._proverMap): 
            prover = self._proverMap[id]
        else:
            prover = SequentProver()
            self._proverMap[id] = prover
        return prover
    
    def exec_prover_cmd(self, id, cmd):
        try:
            prover = self.get_prover_instance(id)
            cmdParsed = yacc.parse(cmd)            
            prover.eval(cmdParsed)  
            cmdParsed = yacc.parse("print")
            proofRepr = prover.eval(cmdParsed)                       
        except Exception, inst:
            msg = inst.__str__()
            return False, "", msg 
        else:
            return True, parseToSVG(proofRepr), prover.finalStatus                        

    '''
    Deprecated:
    =======================================
    '''
    def prove(self, formula):
        print "formula to prove: ", formula        
        ret = ""
        
        prover = self.get_prover_instance("id")
        
        try:
            s = "read " + formula  
            cmd = yacc.parse(s)
            prover.eval(cmd)
        except SyntaxError:
            ret = "Error: Syntax Error" 
        else:
            s = "run"
            cmd = yacc.parse(s)
            prover.eval(cmd)
        
            s = "print"
            cmd = yacc.parse(s)
            proof = prover.eval(cmd)
        
            ret = parseToSVG(proof)       
           
        return ret

# Setup log information
op = OptionParser(usage="%prog [options]")
op.add_option("-l", "--loglevel", help="loglevel (DEBUG, WARN)", metavar="LOGLEVEL")
op.add_option("-p", "--port", help="HTTP port", metavar="PORT", default=8081, type="int")
options, args = op.parse_args()

# set the loglevel according to cmd line arg
if options.loglevel:
    loglevel = eval(options.loglevel, logging.__dict__)
    logger = logging.getLogger("")
    logger.setLevel(loglevel)

# Run the server with a given list services
AsServer(port=options.port, services=[HemeraServiceContainer(),])