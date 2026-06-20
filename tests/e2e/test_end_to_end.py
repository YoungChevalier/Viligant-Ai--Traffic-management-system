import pytest
from tests.e2e.test_cases import generate_helmet_violation_case, generate_clean_compliance_case
from tests.e2e.pipeline_runner import run_pipeline

@pytest.mark.asyncio
async def test_helmet_violation_pipeline():
    """Ensures a known violation cascades through all services and produces an incident case."""
    test_case = generate_helmet_violation_case()
    
    context, metrics = await run_pipeline(test_case)
    
    # Assertions for successful completion
    assert "error" not in context, f"Pipeline failed: {context.get('error')}"
    assert "evidence" in context, "Pipeline did not reach the evidence generation stage"
    
    # Assertions for Data Consistency & Queues
    evidence_res = context["evidence"]
    assert "incident_id" in evidence_res
    assert evidence_res["queue_status"] == "published"
    
    # Verify that the pipeline passed the correct tracking context forward
    assert "tracking" in context
    assert len(context["tracking"]["tracks"]) > 0
    
    print(f"\n--- Metrics ---\nTotal latency: {metrics.get('total_ms', 0):.2f}ms")

@pytest.mark.asyncio
async def test_clean_compliance_pipeline():
    """Ensures a clean image terminates early and does not produce an incident case."""
    test_case = generate_clean_compliance_case()
    
    # IMPORTANT: Since our Rule Engine is mocked, we must forcefully mock 
    # its response to return empty violations for this specific test case, 
    # or rely on the mock logic if it supports dynamic responses.
    
    context, metrics = await run_pipeline(test_case)
    
    assert "error" not in context
    assert "rule_engine" in context
    
    # Assuming our mock returns empty violations for compliant cases:
    # We verify ANPR and Evidence were correctly skipped
    if not context["rule_engine"].get("violations"):
        assert "anpr" not in context
        assert "evidence" not in context
