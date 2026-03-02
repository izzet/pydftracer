from typing import List

from dftracer.python import (
    AGENT_ID_KEY,
    AGENT_ROLE_KEY,
    ERROR_TYPE_KEY,
    FORMAT_KEY,
    FRAMEWORK_KEY,
    LLM,
    LLM_CALL_ID_KEY,
    LOGICAL_PATH_KEY,
    MESSAGE_TYPE_KEY,
    MODEL_NAME_KEY,
    OPERATION_KIND_KEY,
    PARENT_SPAN_ID_KEY,
    PHYSICAL_PATH_KEY,
    RUN_ID_KEY,
    SPAN_ID_KEY,
    STEP_ID_KEY,
    SUCCESS_KEY,
    TOOL_CALL_ID_KEY,
    TRACE_ID_KEY,
    WORKFLOW_ID_KEY,
    Agent,
    AgentCategory,
    AgentData,
    AgentDataEvent,
    AgentStep,
    AgentStepEvent,
    Judge,
    JudgeEvent,
    LLMEvent,
    Message,
    MessageEvent,
    Tool,
    ToolEvent,
    Workflow,
    WorkflowEvent,
    agent,
    agent_data,
    agent_step,
    judge,
    llm,
    message,
    tool,
    workflow,
)
from dftracer.python import (
    data as ai_data,
)


class TestAgentModule:
    def test_agent_categories_exist(self):
        assert isinstance(agent, Agent)
        assert isinstance(workflow, Workflow)
        assert isinstance(agent_step, AgentStep)
        assert isinstance(llm, LLM)
        assert isinstance(tool, Tool)
        assert isinstance(agent_data, AgentData)
        assert isinstance(message, Message)
        assert isinstance(judge, Judge)

    def test_agent_category_children(self):
        assert hasattr(workflow, "run")
        assert hasattr(workflow, "resume")

        assert hasattr(agent_step, "plan")
        assert hasattr(agent_step, "act")
        assert hasattr(agent_step, "observe")
        assert hasattr(agent_step, "reflect")

        assert hasattr(llm, "call")
        assert hasattr(llm, "stream")
        assert hasattr(llm, "parse")

        assert hasattr(tool, "call")
        assert hasattr(tool, "result")

        assert hasattr(agent_data, "load")
        assert hasattr(agent_data, "save")

        assert hasattr(message, "send")
        assert hasattr(message, "receive")
        assert hasattr(message, "stream")

        assert hasattr(judge, "evaluate")
        assert hasattr(judge, "retry")

    def test_agent_decorator_usage(self):
        @workflow.run
        def run_workflow(x: int) -> int:
            return x + 1

        @agent_step.plan
        def plan_step(x: int) -> int:
            return x * 2

        @tool.call
        def call_tool(x: int) -> int:
            return x - 3

        @llm.call
        def call_llm(x: int) -> int:
            return x

        assert run_workflow(3) == 4
        assert plan_step(4) == 8
        assert call_tool(10) == 7
        assert call_llm(5) == 5

    def test_agent_context_manager_usage(self):
        events: List[str] = []

        with workflow.run:
            events.append("workflow")
            with agent_step.act:
                events.append("step")
            with tool.call:
                events.append("tool")
            with judge.evaluate:
                events.append("judge")

        assert events == ["workflow", "step", "tool", "judge"]

    def test_agent_enable_disable_propagation(self):
        agent.enable()
        assert agent.profiler._enable
        assert workflow.profiler._enable
        assert llm.profiler._enable

        agent.disable()
        assert not agent.profiler._enable
        assert not workflow.profiler._enable
        assert not llm.profiler._enable

        agent.enable()
        assert agent.profiler._enable
        assert workflow.profiler._enable
        assert llm.profiler._enable

    def test_agent_derive_cached_children(self):
        child1 = tool.call.derive("weather")
        child2 = tool.call.derive("weather")
        child3 = tool.call.derive("search")

        assert child1 is child2
        assert child1 is not child3

    def test_agent_iter_method(self):
        data_list = [1, 2, 3]
        result = list(agent_step.act.iter(iter(data_list)))
        assert result == data_list

    def test_agent_init_method(self):
        @tool.init
        def setup_tooling() -> str:
            return "ok"

        assert setup_tooling() == "ok"

    def test_agent_update(self):
        # Ensure the API accepts canonical metadata keys via generic args.
        agent.update(
            args={
                TRACE_ID_KEY: "trace-1",
                WORKFLOW_ID_KEY: "wf-1",
                RUN_ID_KEY: "run-1",
                STEP_ID_KEY: "step-1",
                AGENT_ID_KEY: "planner",
                AGENT_ROLE_KEY: "planner",
                SPAN_ID_KEY: "span-1",
                PARENT_SPAN_ID_KEY: "span-0",
                TOOL_CALL_ID_KEY: "tool-1",
                LLM_CALL_ID_KEY: "llm-1",
                FRAMEWORK_KEY: "plain_python",
                MODEL_NAME_KEY: "test-model",
                MESSAGE_TYPE_KEY: "ToolCallRequestEvent",
                LOGICAL_PATH_KEY: "dataset.input",
                PHYSICAL_PATH_KEY: "/tmp/input.npy",
                FORMAT_KEY: "npy",
                OPERATION_KIND_KEY: "tool_call",
                SUCCESS_KEY: 1,
                ERROR_TYPE_KEY: "",
            }
        )

    def test_names_do_not_collide_with_ai_aliases(self):
        assert ai_data is not agent_data


class TestAgentEnumerations:
    def test_agent_category_values(self):
        assert AgentCategory.WORKFLOW == "workflow"
        assert AgentCategory.STEP == "step"
        assert AgentCategory.LLM == "llm"
        assert AgentCategory.TOOL == "tool"
        assert AgentCategory.DATA == "data"
        assert AgentCategory.MESSAGE == "message"
        assert AgentCategory.JUDGE == "judge"

    def test_agent_event_values(self):
        assert WorkflowEvent.RUN == "run"
        assert WorkflowEvent.RESUME == "resume"

        assert AgentStepEvent.PLAN == "plan"
        assert AgentStepEvent.ACT == "act"

        assert LLMEvent.CALL == "call"
        assert LLMEvent.STREAM == "stream"

        assert ToolEvent.CALL == "call"
        assert ToolEvent.RESULT == "result"

        assert AgentDataEvent.LOAD == "load"
        assert AgentDataEvent.SAVE == "save"

        assert MessageEvent.SEND == "send"
        assert MessageEvent.RECEIVE == "receive"

        assert JudgeEvent.EVALUATE == "evaluate"
        assert JudgeEvent.RETRY == "retry"
