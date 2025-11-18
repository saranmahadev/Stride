from click.testing import CliRunner
from stride.cli.main import cli

runner = CliRunner()

with runner.isolated_filesystem():
    result = runner.invoke(cli, [
        "init",
        "--name", "TestProject",
        "--agents", "claude,copilot",
        "--no-interactive"
    ])
    
    print("Exit code:", result.exit_code)
    print("\nOutput:")
    print(result.output)
    print("\nException:")
    if result.exception:
        import traceback
        traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
