"""
CLI entry point for Multi-AI Debate Agent.
Provides command-line interface for debate operations.
"""

import asyncio
import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from typing import Optional
from debate.engine import DebateEngine
from debate.protocol import DebateConfig
from memory.store import MemoryStore
from config import config

app = typer.Typer(help="Multi-AI Debate Agent - AI辩论系统")
console = Console()


@app.command()
def start(
    topic: str = typer.Argument(..., help="辩论主题"),
    max_rounds: int = typer.Option(3, "--rounds", "-r", help="最大辩论轮次"),
    pro_model: str = typer.Option("mimo", "--pro", help="正方模型"),
    con_model: str = typer.Option("deepseek", "--con", help="反方模型"),
    judge_model: str = typer.Option("mimo", "--judge", help="裁判模型")
):
    """开始一场新的辩论"""
    console.print(Panel(f"开始辩论: {topic}", style="bold blue"))

    # Create debate config
    debate_config = DebateConfig(
        topic=topic,
        max_rounds=max_rounds,
        models={
            "pro": pro_model,
            "con": con_model,
            "judge": judge_model
        }
    )

    # Run debate
    result = asyncio.run(_run_debate(debate_config))

    # Display result
    _display_result(result)


async def _run_debate(config: DebateConfig):
    """Run debate asynchronously."""
    memory_store = MemoryStore()
    engine = DebateEngine(memory_store=memory_store)

    # Set up message callback for real-time display
    async def on_message(message):
        role_name = "正方" if message.role == "pro" else "反方" if message.role == "con" else "裁判"
        style = "green" if message.role == "pro" else "red" if message.role == "con" else "yellow"
        console.print(Panel(
            message.content,
            title=f"{role_name} (第{message.round_number}轮)",
            style=style
        ))

    engine.set_on_message_callback(on_message)

    return await engine.start_debate(config)


def _display_result(result):
    """Display debate result."""
    console.print("\n" + "="*50)
    console.print(Panel("辩论结果", style="bold magenta"))

    # Display verdict
    if result.verdict:
        console.print(f"推荐方案: {result.verdict.recommendation}")
        console.print(f"胜出方: {result.verdict.winner}")
        console.print(f"信心度: {result.verdict.confidence:.0%}")

        if result.verdict.action_plan:
            console.print("\n执行计划:")
            for i, step in enumerate(result.verdict.action_plan, 1):
                console.print(f"  {i}. {step}")

    # Ask for execution
    if typer.confirm("\n是否执行推荐方案?"):
        console.print("执行功能开发中...", style="yellow")


@app.command()
def history(
    limit: int = typer.Option(10, "--limit", "-l", help="显示数量")
):
    """查看历史辩论记录"""
    console.print(Panel("历史辩论记录", style="bold blue"))
    # TODO: Implement history display
    console.print("历史记录功能开发中...", style="yellow")


@app.command()
def memories(
    query: Optional[str] = typer.Argument(None, help="搜索关键词"),
    limit: int = typer.Option(10, "--limit", "-l", help="显示数量")
):
    """查看记忆库"""
    console.print(Panel("记忆库", style="bold blue"))
    # TODO: Implement memories display
    console.print("记忆库功能开发中...", style="yellow")


@app.command()
def review(
    debate_id: str = typer.Argument(..., help="辩论ID")
):
    """查看辩论详情"""
    console.print(Panel(f"辩论详情: {debate_id}", style="bold blue"))
    # TODO: Implement review display
    console.print("查看详情功能开发中...", style="yellow")


@app.command()
def execute(
    debate_id: str = typer.Argument(..., help="辩论ID")
):
    """执行辩论推荐方案"""
    console.print(Panel(f"执行方案: {debate_id}", style="bold blue"))
    # TODO: Implement execution
    console.print("执行功能开发中...", style="yellow")


if __name__ == "__main__":
    app()
