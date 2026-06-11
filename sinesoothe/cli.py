from __future__ import annotations

from pathlib import Path

import click

from sinesoothe.engine import export_hunter_report, plot_before_after, process_audio
from sinesoothe.presets import get_preset, list_presets


@click.group()
def cli() -> None:
    """ONDASINUS88 / BlackMamba SineSoothe CLI."""


@cli.command("process")
@click.argument("input_path", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(dir_okay=False),
    default="output.wav",
    show_default=True,
)
@click.option("--preset", type=str, default=None, help="Preset name to load.")
@click.option("--depth", type=float, default=0.4, show_default=True)
@click.option("--sharpness", type=float, default=0.7, show_default=True)
@click.option("--mix", type=float, default=1.0, show_default=True)
@click.option("--max-reduction-db", type=float, default=9.0, show_default=True)
@click.option("--plot", is_flag=True, help="Generate before/after spectrogram.")
@click.option("--json-report", is_flag=True, help="Export processing report as JSON.")
def process_command(
    input_path: str,
    output_path: str,
    preset: str | None,
    depth: float,
    sharpness: float,
    mix: float,
    max_reduction_db: float,
    plot: bool,
    json_report: bool,
) -> None:
    """Process an audio file and suppress harsh resonances."""

    if preset:
        selected = get_preset(preset)
        depth = selected.depth
        sharpness = selected.sharpness
        mix = selected.mix
        max_reduction_db = selected.max_reduction_db
        click.echo(f"Preset loaded: {selected.name} [{selected.mode}]")

    result = process_audio(
        input_path=input_path,
        output_path=output_path,
        depth=depth,
        sharpness=sharpness,
        mix=mix,
        max_reduction_db=max_reduction_db,
    )

    click.echo("ONDASINUS88 / BlackMamba SineSoothe")
    click.echo(f"Input:       {result.input_path}")
    click.echo(f"Output:      {result.output_path}")
    click.echo(f"Sample rate: {result.sample_rate}")
    click.echo(f"Duration:    {result.duration_seconds:.2f}s")
    click.echo(f"Depth:       {result.depth:.2f}")
    click.echo(f"Sharpness:   {result.sharpness:.2f}")
    click.echo(f"Mix:         {result.mix:.2f}")
    click.echo(f"Max GR:      {result.max_reduction_db:.2f} dB")
    click.echo(f"Avg GR:      {result.avg_reduction_db:.2f} dB")
    click.echo(f"Venom:       {result.venom_level_score:.1f}/100")

    output = Path(output_path)

    if json_report:
        json_path = output.with_suffix(".json")
        export_hunter_report(result, json_path)
        click.echo(f"JSON report: {json_path}")

    if plot:
        plot_path = output.with_suffix(".png")
        plot_before_after(input_path, output_path, plot_path)
        click.echo(f"Plot:        {plot_path}")


@cli.group("presets")
def presets_group() -> None:
    """Preset utilities."""


@presets_group.command("list")
def presets_list_command() -> None:
    """List available presets."""

    for preset in list_presets():
        click.echo(preset)


@presets_group.command("show")
@click.argument("name")
def presets_show_command(name: str) -> None:
    """Show preset parameters."""

    preset = get_preset(name)
    click.echo(f"name: {preset.name}")
    click.echo(f"mode: {preset.mode}")
    click.echo(f"depth: {preset.depth}")
    click.echo(f"sharpness: {preset.sharpness}")
    click.echo(f"max_reduction_db: {preset.max_reduction_db}")
    click.echo(f"mix: {preset.mix}")


if __name__ == "__main__":
    cli()
