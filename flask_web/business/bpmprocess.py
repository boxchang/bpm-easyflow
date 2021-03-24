from bases.database import tiptop_database, bpm_database
import json

from bases.lib_common import json_format


class bpmprocess(object):
    bpmdb = None

    def __init__(self):
        self.bpmdb = bpm_database()

    def pr_process(self):
        sql = """SELECT a.processInstanceName,a.subject,f.workItemName,u.userName,format(f.createdTime,'yyyy-MM-dd HH:mm:ss')createdTime,
                Datediff(mi,f.createdTime,GETDATE())/60 qtime,c.limits FROM ProcessInstance a , ParticipantActivityInstance b, ActivityDefinition c,ProcessContext d, ProcessPackage_ProcessDef e,WorkItem f,WorkAssignment wa,Users u
                WHERE 1=1 AND a.contextOID = b.contextOID AND b.definitionId = c.id
                AND a.contextOID = d.OID AND d.processPackageOID = e.ProcessPackageOID
                AND e.ProcessDefinitionOID = c.containerOID AND b.OID = f.containerOID
                AND completedTime IS NULL AND f.OID = wa.workItemOID AND wa.assigneeOID = u.OID
                AND processDefinitionId IN ('TIPTOPPROCESSPKG_apmt420',
                'TIPTOPPROCESSPKG_apmt540',
                'TIPTOPPROCESSPKG_apmt910',
                'TIPTOPPROCESSPKG_aapt120',
                'TIPTOPPROCESSPKG_aapt110',
                'TIPTOPPROCESSPKG_aapt150',
                'TIPTOPPROCESSPKG_aapt330')  
                order by f.createdTime"""
        cursor = self.bpmdb.execute_select_sql(sql)
        result = str(json.dumps(json_format(cursor)))

        return result


# bp = bpmprocess()
# xx = bp.pr_process()
# print(xx)