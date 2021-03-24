from zeep import Client
from bases.lib_database import getDBEnvFlag
from web_service.base_data import base_data


class itrequest_ws(base_data):
    url = "http://{bpm_url}:8086/NaNaWeb/services/WorkflowService?wsdl"
    url = url.format(bpm_url=base_data.bpm_url)
    client = None

    def __init__(self):
        self.client = Client(self.url)

    def initial_satisfaction_form(self, pProcessId, pUserId, pOrgUnitId, pSubject):
        print(self.client.service.findFormOIDsOfProcess(pProcessId))
        pFormOID = self.client.service.findFormOIDsOfProcess(pProcessId)
        self.client.service.invokeProcess(pProcessId, pUserId, pOrgUnitId, pFormOID, pFormFieldValue, pSubject)

pProcessId = 'TIPTOPPROCESSPKG_apmt420'
pUserId = '2018100202'
pOrgUnitId = '00110300'
pSubject =  'IT Request Form Satisfaction Survey'

itform = itrequest_ws()
itform.initial_satisfaction_form(pProcessId, pUserId, pOrgUnitId, pSubject)
