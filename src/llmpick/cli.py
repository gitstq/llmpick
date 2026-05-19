"""命令行接口模块"""

from __future__ import annotations

from typing import Optional

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from llmpick import __version__
from llmpick.core import LLMPick
from llmpick.hardware import HardwareDetector
from llmpick.models import ModelDatabase

app = typer.Typer(
    name="llmpick",
    help="🎯 智能本地LLM选型助手 - Intelligent Local LLM Selector",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """版本回调"""
    if value:
        console.print(f"[bold cyan]LLMPick[/bold cyan] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True,
        help="显示版本信息",
    ),
) -> None:
    """LLMPick - 智能本地LLM选型助手"""
    pass


@app.command()
def detect() -> None:
    """🔍 检测硬件信息"""
    console.print(Panel.fit(
        "[bold cyan]🔍 正在检测硬件信息...[/bold cyan]",
        border_style="cyan",
    ))
    
    detector = HardwareDetector()
    hardware = detector.detect()
    
    console.print("")
    console.print(detector.format_hardware_info(hardware))
    console.print("")


@app.command()
def recommend(
    top: int = typer.Option(5, "--top", "-n", help="显示前N个推荐"),
    chinese: bool = typer.Option(True, "--chinese/--no-chinese", help="优先中文模型"),
    json_output: bool = typer.Option(False, "--json", help="JSON格式输出"),
) -> None:
    """🎯 推荐适合的LLM模型"""
    console.print(Panel.fit(
        "[bold cyan]🎯 正在分析硬件并推荐最佳LLM模型...[/bold cyan]",
        border_style="cyan",
    ))
    
    picker = LLMPick()
    recommendations = picker.recommend(top_k=top, prefer_chinese=chinese)
    
    if json_output:
        import json
        data = [
            {
                "rank": i + 1,
                "model_id": rec.model.id,
                "model_name": rec.model.name,
                "score": rec.score,
                "fit_type": rec.fit_type,
                "vram_usage_gb": rec.vram_usage_gb,
                "estimated_speed": rec.estimated_tokens_per_sec,
                "reason": rec.reason,
            }
            for i, rec in enumerate(recommendations)
        ]
        console.print_json(json.dumps(data, ensure_ascii=False, indent=2))
        return
    
    if not recommendations:
        console.print("[yellow]⚠️ 未找到适合您硬件的模型[/yellow]")
        return
    
    # 创建表格
    table = Table(
        title="🎯 推荐模型列表",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("排名", justify="center", style="bold", width=4)
    table.add_column("模型", style="bright_white", min_width=20)
    table.add_column("参数量", justify="center", width=8)
    table.add_column("大小", justify="right", width=8)
    table.add_column("评分", justify="right", style="bold green", width=8)
    table.add_column("适配度", justify="center", width=10)
    table.add_column("预估速度", justify="right", width=12)
    table.add_column("推荐理由", style="dim", min_width=20)
    
    fit_colors = {
        "perfect": "[bold green]完美[/bold green]",
        "good": "[green]良好[/green]",
        "partial": "[yellow]部分[/yellow]",
        "tight": "[red]紧张[/red]",
        "cpu_only": "[dim]CPU[/dim]",
    }
    
    for i, rec in enumerate(recommendations, 1):
        model = rec.model
        
        # 模型名称（带中文标识）
        name_text = model.name
        if model.is_chinese_optimized:
            name_text += " [CN]"
        
        table.add_row(
            str(i),
            name_text,
            model.parameters,
            f"{model.size_gb:.1f}GB",
            f"{rec.score:.1f}",
            fit_colors.get(rec.fit_type, rec.fit_type),
            f"{rec.estimated_tokens_per_sec:.1f} t/s",
            rec.reason,
        )
    
    console.print("")
    console.print(table)
    console.print("")
    
    # 显示最佳推荐详情
    if recommendations:
        best = recommendations[0]
        console.print(Panel(
            f"[bold green]⭐ 最佳推荐: {best.model.name}[/bold green]\n\n"
            f"[cyan]模型ID:[/cyan] {best.model.id}\n"
            f"[cyan]HuggingFace:[/cyan] {best.model.repo_id}\n"
            f"[cyan]描述:[/cyan] {best.model.description}\n"
            f"[cyan]上下文长度:[/cyan] {best.model.context_length:,} tokens\n\n"
            f"[bold]安装命令:[/bold]\n"
            f"[dim]Ollama:[/dim] [yellow]{picker.get_model_download_command(best.model, 'ollama')}[/yellow]\n"
            f"[dim]运行命令:[/dim] [yellow]{picker.get_model_run_command(best.model, 'ollama')}[/yellow]",
            title="详细信息",
            border_style="green",
        ))


@app.command()
def list_models(
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="按标签过滤"),
    chinese_only: bool = typer.Option(False, "--chinese-only", "-c", help="仅显示中文模型"),
    code_only: bool = typer.Option(False, "--code-only", help="仅显示代码优化模型"),
) -> None:
    """📋 列出所有可用模型"""
    db = ModelDatabase()
    models = db.get_all_models()
    
    # 过滤
    if chinese_only:
        models = [m for m in models if m.is_chinese_optimized]
    if code_only:
        models = [m for m in models if m.is_code_optimized]
    if tag:
        models = [m for m in models if tag.lower() in [t.lower() for t in m.tags]]
    
    table = Table(
        title=f"📋 可用模型列表 ({len(models)}个)",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("ID", style="dim", min_width=15)
    table.add_column("名称", style="bright_white", min_width=18)
    table.add_column("参数量", justify="center", width=8)
    table.add_column("大小", justify="right", width=8)
    table.add_column("量化", justify="center", width=8)
    table.add_column("中文", justify="center", width=6)
    table.add_column("代码", justify="center", width=6)
    table.add_column("评分", justify="right", width=8)
    
    for model in models:
        table.add_row(
            model.id,
            model.name,
            model.parameters,
            f"{model.size_gb:.1f}GB",
            model.quantization.value,
            "✓" if model.is_chinese_optimized else "",
            "✓" if model.is_code_optimized else "",
            f"{model.benchmark_score:.1f}" if model.benchmark_score else "N/A",
        )
    
    console.print("")
    console.print(table)
    console.print("")


@app.command()
def info(model_id: str = typer.Argument(..., help="模型ID")) -> None:
    """ℹ️ 查看模型详细信息"""
    db = ModelDatabase()
    model = db.get_model_by_id(model_id)
    
    if not model:
        console.print(f"[red]❌ 未找到模型: {model_id}[/red]")
        console.print(f"[dim]使用 [cyan]llmpick list[/cyan] 查看所有可用模型[/dim]")
        raise typer.Exit(1)
    
    picker = LLMPick()
    
    # 构建特性标签
    features = []
    if model.is_chinese_optimized:
        features.append("[green]中文优化[/green]")
    if model.is_code_optimized:
        features.append("[blue]代码优化[/blue]")
    if model.is_multimodal:
        features.append("[magenta]多模态[/magenta]")
    
    content = f"""[bold cyan]{model.name}[/bold cyan]

[cyan]模型ID:[/cyan] {model.id}
[cyan]HuggingFace:[/cyan] {model.repo_id}
[cyan]描述:[/cyan] {model.description}
[cyan]参数量:[/cyan] {model.parameters}
[cyan]模型大小:[/cyan] {model.size_gb:.1f} GB
[cyan]量化方式:[/cyan] {model.quantization.value}
[cyan]上下文长度:[/cyan] {model.context_length:,} tokens
[cyan]格式:[/cyan] {model.format.value}
[cyan]评分:[/cyan] {model.benchmark_score:.1f}/100

[bold]特性:[/bold] {' | '.join(features) if features else '通用模型'}

[bold]标签:[/bold] {', '.join(model.tags)}

[bold]安装命令:[/bold]
  [dim]Ollama:[/dim]   [yellow]{picker.get_model_download_command(model, 'ollama')}[/yellow]
  [dim]LM Studio:[/dim] [yellow]{picker.get_model_download_command(model, 'lmstudio')}[/yellow]

[bold]运行命令:[/bold]
  [dim]Ollama:[/dim]   [yellow]{picker.get_model_run_command(model, 'ollama')}[/yellow]
"""
    
    console.print("")
    console.print(Panel(content, border_style="cyan"))
    console.print("")


@app.command()
def compare(
    model_ids: list[str] = typer.Argument(..., help="要对比的模型ID（至少2个）"),
) -> None:
    """🔍 对比多个模型"""
    if len(model_ids) < 2:
        console.print("[red]❌ 请提供至少2个模型ID进行对比[/red]")
        raise typer.Exit(1)
    
    db = ModelDatabase()
    models = []
    for mid in model_ids:
        model = db.get_model_by_id(mid)
        if model:
            models.append(model)
        else:
            console.print(f"[yellow]⚠️ 未找到模型: {mid}[/yellow]")
    
    if len(models) < 2:
        console.print("[red]❌ 有效模型不足2个，无法对比[/red]")
        raise typer.Exit(1)
    
    table = Table(
        title="🔍 模型对比",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("属性", style="bold", min_width=12)
    for model in models:
        table.add_column(model.name, justify="center", min_width=15)
    
    # 对比行
    table.add_row("参数量", *[m.parameters for m in models])
    table.add_row("模型大小", *[f"{m.size_gb:.1f}GB" for m in models])
    table.add_row("量化", *[m.quantization.value for m in models])
    table.add_row("上下文", *[f"{m.context_length/1000:.0f}K" for m in models])
    table.add_row("中文优化", *["✓" if m.is_chinese_optimized else "✗" for m in models])
    table.add_row("代码优化", *["✓" if m.is_code_optimized else "✗" for m in models])
    table.add_row("多模态", *["✓" if m.is_multimodal else "✗" for m in models])
    table.add_row("评分", *[f"{m.benchmark_score:.1f}" if m.benchmark_score else "N/A" for m in models])
    
    console.print("")
    console.print(table)
    console.print("")


def main_entry() -> None:
    """入口函数"""
    app()


if __name__ == "__main__":
    main_entry()
