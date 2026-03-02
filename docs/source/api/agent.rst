Agent API
=========

This section documents the agent tracing namespace and its event model.

Agent Module
------------

The ``agent`` module provides decorators and utilities for tracing agentic workflows.

.. automodule:: dftracer.python.agent
   :members:
   :undoc-members:

Agent Categories
----------------

.. autoclass:: dftracer.python.AgentCategory
   :members:
   :undoc-members:

Agent Components
----------------

.. autoclass:: dftracer.python.Workflow
   :members:
   :undoc-members:

.. autoclass:: dftracer.python.AgentStep
   :members:
   :undoc-members:

.. autoclass:: dftracer.python.LLM
   :members:
   :undoc-members:

.. autoclass:: dftracer.python.Tool
   :members:
   :undoc-members:

.. autoclass:: dftracer.python.AgentData
   :members:
   :undoc-members:

.. autoclass:: dftracer.python.Message
   :members:
   :undoc-members:

.. autoclass:: dftracer.python.Judge
   :members:
   :undoc-members:

Agent Instance
--------------

.. autoclass:: dftracer.python.Agent
   :members:
   :undoc-members:

Convenience aliases:

- ``agent`` - Main agent tracing instance
- ``workflow`` - Workflow tracing category
- ``agent_step`` - Agent step tracing category
- ``llm`` - LLM tracing category
- ``tool`` - Tool tracing category
- ``agent_data`` - Data operation tracing category
- ``message`` - Message/event tracing category
- ``judge`` - Evaluation/retry tracing category

LangGraph Adapter
-----------------

Utilities for tracing LangGraph-style node and workflow invocation boundaries:

.. autofunction:: dftracer.python.get_or_init_trace_context
.. autofunction:: dftracer.python.traced_node
.. autofunction:: dftracer.python.trace_invoke
