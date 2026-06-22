import sys
import asyncio
import datetime
from unittest.mock import patch

sys.path.insert(0, r'services\dashboard-api')

from app.services.incident_queries import _incident_store
from app.services.review_workflow import get_review_queue, assign_incident, submit_decision, get_incident_audit_log, escalate_incident
from app.api.schemas import ReviewAssignmentRequest, ReviewDecisionRequest, EscalationRequest

async def run():
    _incident_store['inc-1'] = {'incident_id': 'inc-1', 'status': 'OPEN', 'primary_violation': 'RED_LIGHT', 'confidence': 0.55}
    
    queue = await get_review_queue()
    print('Queue Length:', queue['total'])
    
    assign_res = await assign_incident('inc-1', ReviewAssignmentRequest())
    print('Assign:', assign_res)
    
    q2 = await get_review_queue()
    print('Queue length after assign (auto-escalation triggers on queue load due to low conf!):', q2['total'])
    
    # Incident status will be ESCALATED now because 0.55 < 0.60 threshold
    print("Status after queue fetch:", _incident_store['inc-1']['status'])
    
    esc_res = await escalate_incident('inc-1', EscalationRequest(reviewer_id='auto', reason='complex', target_tier='ADMIN'))
    print('Manual Escalate:', esc_res)
    
    dec_res = await submit_decision('inc-1', ReviewDecisionRequest(reviewer_id='admin', action='REJECT', notes='bad detection'))
    print('Decision:', dec_res)
    
    logs = await get_incident_audit_log('inc-1')
    print('Audit logs:', [log['action_type'] for log in logs])

if __name__ == "__main__":
    with patch('libs.common_utils.time_utils.utc_now', return_value=datetime.datetime.now()), \
         patch('libs.common_utils.id_utils.build_incident_id', return_value="inc-test"):
        asyncio.run(run())

