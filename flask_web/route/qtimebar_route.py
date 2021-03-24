from flask import Blueprint
from flask_cors import cross_origin

from bases.database import bpm_database
from chart.barchart import BarChartJS

qtimebar_bp = Blueprint('qtimebar_bp',__name__)


@qtimebar_bp.route('/qtimebar')
@cross_origin()
def qtimebar():
    msdb = bpm_database()
    msdb.create_connection()

    sql = """SELECT COUNT(processInstanceName) result, processInstanceName label FROM (
                SELECT a.processInstanceName,a.subject,f.workItemName,u.userName,format(f.createdTime,'yyyy-MM-dd HH:mm:ss') createdTime,
                Datediff(mi,f.createdTime,GETDATE())/60 qtime,c.limits FROM ProcessInstance a , ParticipantActivityInstance b, ActivityDefinition c,ProcessContext d, ProcessPackage_ProcessDef e,WorkItem f,WorkAssignment wa,Users u 
                WHERE 1=1 AND a.contextOID = b.contextOID AND b.definitionId = c.id 
                AND a.contextOID = d.OID AND d.processPackageOID = e.ProcessPackageOID 
                AND e.ProcessDefinitionOID = c.containerOID AND b.OID = f.containerOID 
                AND completedTime IS NULL AND f.OID = wa.workItemOID AND wa.assigneeOID = u.OID 
                AND Datediff(mi,f.createdTime,GETDATE()) >=1440 ) A GROUP BY processInstanceName"""
    cursor = msdb.execute_select_sql(sql)

    chartjs = BarChartJS()
    ajax_data = chartjs.BarChartByCursor(cursor)

    return ajax_data