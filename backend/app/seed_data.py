from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Edge, Node, NodeTag, Roadmap, RoadmapStep, Tag


NODE_SEED = [
    {"title": "ChatGPT", "type": "tool", "description": "通用 AI 助手，适合问答、写作、分析和轻量自动化", "tags": ["AI助手", "通用工具"], "status": "used", "importance": 5, "businessValue": 4},
    {"title": "Claude", "type": "tool", "description": "擅长长文本理解、写作、代码协作与严谨分析", "tags": ["AI助手", "长文本"], "status": "used", "importance": 5, "businessValue": 5},
    {"title": "Cursor", "type": "tool", "description": "面向开发者的 AI 编程工具，适合代码生成、修改和理解", "tags": ["编程", "IDE"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "Dify", "type": "tool", "description": "用于搭建 AI 应用和知识库问答的低代码平台", "tags": ["应用搭建", "RAG"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "n8n", "type": "tool", "description": "面向自动化流程编排的工作流平台", "tags": ["自动化", "工作流"], "status": "learning", "importance": 4, "businessValue": 5},
    {"title": "GPT-4.1", "type": "model", "description": "适合复杂推理、工具调用和稳定任务执行", "tags": ["推理", "通用模型"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "GPT-4o", "type": "model", "description": "强调多模态和实时交互能力", "tags": ["多模态", "实时"], "status": "learning", "importance": 4, "businessValue": 4},
    {"title": "o3", "type": "model", "description": "更偏复杂分析和高质量推理任务", "tags": ["深度推理", "分析"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "Claude Sonnet 4", "type": "model", "description": "适合代码、文档、分析和日常生产任务", "tags": ["代码", "写作"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "Gemini 2.5 Pro", "type": "model", "description": "适合长上下文、多步骤理解和综合任务", "tags": ["长上下文", "综合能力"], "status": "learning", "importance": 4, "businessValue": 4},
    {"title": "LangChain", "type": "framework", "description": "用于构建 LLM 应用和工具链整合的框架", "tags": ["LLM应用", "编排"], "status": "todo", "importance": 4, "businessValue": 4},
    {"title": "LangGraph", "type": "framework", "description": "面向多步骤 agent 和状态流的编排框架", "tags": ["Agent", "流程编排"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "LlamaIndex", "type": "framework", "description": "偏知识库接入、检索和 RAG 应用搭建", "tags": ["RAG", "检索"], "status": "learning", "importance": 4, "businessValue": 5},
    {"title": "AutoGen", "type": "framework", "description": "用于多 agent 协作与对话式任务拆解", "tags": ["多Agent", "协作"], "status": "todo", "importance": 4, "businessValue": 4},
    {"title": "FastAPI", "type": "framework", "description": "用于快速搭建 AI 工具后端服务接口", "tags": ["后端", "API"], "status": "used", "importance": 5, "businessValue": 4},
    {"title": "知识库问答", "type": "use_case", "description": "基于文档和知识源进行检索增强回答", "tags": ["RAG", "企业场景"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "AI 客服", "type": "use_case", "description": "面向客户咨询、常见问题和服务流程自动化", "tags": ["服务", "自动回复"], "status": "learning", "importance": 4, "businessValue": 5},
    {"title": "工作流自动化", "type": "use_case", "description": "连接多系统并自动执行重复流程", "tags": ["流程", "集成"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "代码助手", "type": "use_case", "description": "辅助写代码、改代码、查问题和解释实现", "tags": ["研发", "效率"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "多 Agent 协作", "type": "use_case", "description": "把复杂任务拆成多个角色并行完成", "tags": ["协作", "复杂任务"], "status": "learning", "importance": 5, "businessValue": 4},
    {"title": "Hagsyn Graph", "type": "project", "description": "个人 AI 工具路线图与知识图谱工作台", "tags": ["知识图谱", "工作台"], "status": "todo", "importance": 5, "businessValue": 5},
    {"title": "企业知识库助手", "type": "project", "description": "面向团队文档问答和知识检索的交付型项目", "tags": ["企业", "知识库"], "status": "todo", "importance": 5, "businessValue": 5},
    {"title": "AI 工具导航站", "type": "project", "description": "汇总 AI 工具、模型、框架和应用场景的网站", "tags": ["导航", "内容产品"], "status": "todo", "importance": 4, "businessValue": 4},
    {"title": "个人工作流自动化系统", "type": "project", "description": "把日常信息处理和任务流转自动化", "tags": ["自动化", "个人效率"], "status": "todo", "importance": 4, "businessValue": 5},
    {"title": "多 Agent 研发助手", "type": "project", "description": "面向研发场景的拆任务、查代码、生成修改建议工具", "tags": ["研发", "Agent"], "status": "todo", "importance": 5, "businessValue": 5},
    {"title": "Prompt Engineering", "type": "skill", "description": "设计高质量提示词以提升模型输出稳定性", "tags": ["提示词", "基础能力"], "status": "learning", "importance": 5, "businessValue": 4},
    {"title": "RAG Design", "type": "skill", "description": "设计检索、召回、重排和回答链路", "tags": ["RAG", "检索设计"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "Agent Orchestration", "type": "skill", "description": "设计 agent 角色、状态和执行流", "tags": ["Agent", "编排"], "status": "learning", "importance": 5, "businessValue": 5},
    {"title": "Workflow Automation", "type": "skill", "description": "把工具、表单、消息和 API 串起来", "tags": ["自动化", "集成"], "status": "learning", "importance": 4, "businessValue": 5},
    {"title": "API Integration", "type": "skill", "description": "把外部系统能力接入到自己的产品里", "tags": ["API", "集成"], "status": "learning", "importance": 4, "businessValue": 4},
    {"title": "OpenAI Docs", "type": "resource", "description": "OpenAI 官方开发文档", "tags": ["官方文档", "OpenAI"], "status": "used", "importance": 5, "businessValue": 4, "url": "https://platform.openai.com/docs"},
    {"title": "Anthropic Docs", "type": "resource", "description": "Anthropic 官方开发文档", "tags": ["官方文档", "Anthropic"], "status": "used", "importance": 4, "businessValue": 4, "url": "https://docs.anthropic.com/"},
    {"title": "LangChain Docs", "type": "resource", "description": "LangChain 官方文档与示例", "tags": ["官方文档", "LangChain"], "status": "used", "importance": 4, "businessValue": 4, "url": "https://python.langchain.com/"},
    {"title": "Hugging Face", "type": "resource", "description": "模型、数据集和社区资源平台", "tags": ["模型", "社区"], "status": "used", "importance": 4, "businessValue": 4, "url": "https://huggingface.co/"},
    {"title": "GitHub", "type": "resource", "description": "代码托管、开源项目和技术协作平台", "tags": ["代码托管", "开源"], "status": "used", "importance": 5, "businessValue": 4, "url": "https://github.com/"},
    {"title": "AI 工具学习路线", "type": "roadmap", "description": "从工具认知到实际使用的学习路径", "tags": ["学习路线", "工具认知"], "status": "todo", "importance": 4, "businessValue": 4},
    {"title": "RAG 落地路线", "type": "roadmap", "description": "从知识源整理到问答系统上线的路径", "tags": ["RAG", "实施路径"], "status": "todo", "importance": 5, "businessValue": 5},
    {"title": "Agent 产品化路线", "type": "roadmap", "description": "从单 agent 到多 agent 产品能力的推进路线", "tags": ["Agent", "产品化"], "status": "todo", "importance": 5, "businessValue": 5},
    {"title": "调研流程", "type": "roadmap", "description": "工具选型、对比、记录和结论沉淀流程", "tags": ["调研", "方法"], "status": "todo", "importance": 4, "businessValue": 4},
    {"title": "Demo 构建流程", "type": "roadmap", "description": "从想法到可展示原型的最短实施路径", "tags": ["Demo", "原型"], "status": "todo", "importance": 4, "businessValue": 5},
]

EDGE_SEED = [
    {"source": "Hagsyn Graph", "target": "FastAPI", "relation": "uses", "note": "后端接口服务基于 FastAPI"},
    {"source": "Hagsyn Graph", "target": "ChatGPT", "relation": "uses", "note": "作为日常 AI 工具参考对象"},
    {"source": "Hagsyn Graph", "target": "Claude", "relation": "uses", "note": "作为日常 AI 工具参考对象"},
    {"source": "Hagsyn Graph", "target": "AI 工具学习路线", "relation": "good_for", "note": "适合沉淀学习路径"},
    {"source": "企业知识库助手", "target": "知识库问答", "relation": "good_for", "note": "核心交付场景"},
    {"source": "企业知识库助手", "target": "Dify", "relation": "uses", "note": "适合快速搭建问答流程"},
    {"source": "企业知识库助手", "target": "RAG Design", "relation": "depends_on", "note": "需要先完成检索链路设计"},
    {"source": "个人工作流自动化系统", "target": "工作流自动化", "relation": "good_for", "note": "面向个人效率场景"},
    {"source": "个人工作流自动化系统", "target": "n8n", "relation": "uses", "note": "工作流编排核心工具"},
    {"source": "个人工作流自动化系统", "target": "Workflow Automation", "relation": "depends_on", "note": "依赖自动化设计能力"},
    {"source": "多 Agent 研发助手", "target": "多 Agent 协作", "relation": "good_for", "note": "目标是复杂任务协同"},
    {"source": "多 Agent 研发助手", "target": "Agent Orchestration", "relation": "depends_on", "note": "依赖 agent 编排能力"},
    {"source": "多 Agent 研发助手", "target": "代码助手", "relation": "alternative_to", "note": "相对单助手方案的升级形态"},
    {"source": "Cursor", "target": "代码助手", "relation": "good_for", "note": "面向研发场景"},
    {"source": "Claude", "target": "代码助手", "relation": "good_for", "note": "适合代码理解和修改"},
    {"source": "ChatGPT", "target": "代码助手", "relation": "good_for", "note": "适合通用研发辅助"},
    {"source": "Dify", "target": "知识库问答", "relation": "good_for", "note": "适合搭建企业问答 demo"},
    {"source": "n8n", "target": "工作流自动化", "relation": "good_for", "note": "适合系统集成与自动化"},
    {"source": "LangChain", "target": "知识库问答", "relation": "supports", "note": "可作为问答链路底层框架"},
    {"source": "LangGraph", "target": "多 Agent 协作", "relation": "supports", "note": "适合状态化 agent 流程"},
    {"source": "LlamaIndex", "target": "知识库问答", "relation": "supports", "note": "适合知识库接入"},
    {"source": "AutoGen", "target": "多 Agent 协作", "relation": "supports", "note": "适合多角色对话协作"},
    {"source": "Prompt Engineering", "target": "RAG Design", "relation": "next_step", "note": "提示词之后进入检索设计"},
    {"source": "RAG Design", "target": "Agent Orchestration", "relation": "next_step", "note": "RAG 完成后进入 agent 编排"},
]

ROADMAP_SEED = [
    {
        "title": "AI 工具学习路线",
        "description": "从工具认知到高频实战的学习路径",
        "targetUser": "独立开发者",
        "goal": "建立稳定的 AI 工具认知和使用习惯",
        "steps": [
            {"title": "熟悉 ChatGPT 与 Claude", "status": "learning", "node": "ChatGPT"},
            {"title": "上手 Cursor 与代码助手场景", "status": "todo", "node": "Cursor"},
            {"title": "形成个人工具选型清单", "status": "todo", "node": "AI 工具导航站"},
        ],
    },
    {
        "title": "RAG 落地路线",
        "description": "从知识源整理到问答系统上线的实施路径",
        "targetUser": "AI 应用构建者",
        "goal": "完成一个能交付的知识库问答 demo",
        "steps": [
            {"title": "梳理知识源和标签体系", "status": "todo", "node": "知识库问答"},
            {"title": "完成 RAG Design 方案", "status": "learning", "node": "RAG Design"},
            {"title": "用 Dify 搭建问答 demo", "status": "todo", "node": "Dify"},
        ],
    },
    {
        "title": "Agent 产品化路线",
        "description": "从单助手到多 Agent 产品能力的推进路线",
        "targetUser": "AI 产品设计者",
        "goal": "完成一个具备协作能力的 agent 产品原型",
        "steps": [
            {"title": "掌握 Prompt Engineering", "status": "learning", "node": "Prompt Engineering"},
            {"title": "研究 LangGraph 和 Agent Orchestration", "status": "todo", "node": "LangGraph"},
            {"title": "完成多 Agent 研发助手原型", "status": "todo", "node": "多 Agent 研发助手"},
        ],
    },
]


def _sync_tags(db: Session, node: Node, tags: Iterable[str]) -> None:
    node.tags.clear()
    seen = set()
    for raw_name in tags:
        name = raw_name.strip()
        if not name or name in seen:
            continue
        seen.add(name)
        tag = db.scalar(select(Tag).where(Tag.name == name))
        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
            db.flush()
        node.tags.append(NodeTag(tag=tag))


def seed_demo_data(db: Session) -> dict[str, int]:
    node_index = {node.title: node for node in db.scalars(select(Node)).all()}
    for item in NODE_SEED:
        node = node_index.get(item["title"])
        if node is None:
            node = Node(
                title=item["title"],
                type=item["type"],
                description=item.get("description"),
                url=item.get("url"),
                status=item.get("status", "todo"),
                importance=item.get("importance", 3),
                business_value=item.get("businessValue", 3),
                note=item.get("note"),
            )
            db.add(node)
            db.flush()
            node_index[node.title] = node
        _sync_tags(db, node, item.get("tags", []))

    existing_edges = {
        (edge.source_id, edge.target_id, edge.relation)
        for edge in db.scalars(select(Edge)).all()
    }
    for item in EDGE_SEED:
        source_id = node_index[item["source"]].id
        target_id = node_index[item["target"]].id
        edge_key = (source_id, target_id, item["relation"])
        if edge_key in existing_edges:
            continue
        db.add(
            Edge(
                source_id=source_id,
                target_id=target_id,
                relation=item["relation"],
                note=item.get("note"),
            )
        )
        existing_edges.add(edge_key)

    roadmap_index = {roadmap.title: roadmap for roadmap in db.scalars(select(Roadmap)).all()}
    for roadmap_item in ROADMAP_SEED:
        roadmap = roadmap_index.get(roadmap_item["title"])
        if roadmap is None:
            roadmap = Roadmap(
                title=roadmap_item["title"],
                description=roadmap_item.get("description"),
                target_user=roadmap_item.get("targetUser"),
                goal=roadmap_item.get("goal"),
            )
            db.add(roadmap)
            db.flush()
            roadmap_index[roadmap.title] = roadmap
        existing_step_titles = {step.title for step in roadmap.steps}
        for index, step_item in enumerate(roadmap_item.get("steps", []), start=1):
            if step_item["title"] in existing_step_titles:
                continue
            db.add(
                RoadmapStep(
                    roadmap_id=roadmap.id,
                    node_id=node_index.get(step_item.get("node")).id if step_item.get("node") in node_index else None,
                    title=step_item["title"],
                    description=step_item.get("description"),
                    step_order=index,
                    status=step_item.get("status", "todo"),
                )
            )

    db.commit()
    return {
        "nodes": db.query(Node).count(),
        "edges": db.query(Edge).count(),
        "roadmaps": db.query(Roadmap).count(),
    }
