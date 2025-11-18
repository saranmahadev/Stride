from click.testing import CliRunner
from stride.cli.main import cli

runner = CliRunner()

with runner.isolated_filesystem():
    # First init
    result1 = runner.invoke(cli, [
        "init",
        "--name", "FirstProject",
        "--agents", "claude",
        "--no-interactive"
    ])
    
    print("First init exit code:", result1.exit_code)
    print("First init output:", result1.output)
    
    # Second init with force
    result2 = runner.invoke(cli, [
        "init",
        "--name", "SecondProject",
        "--agents", "copilot",
        "--force",
        "--no-interactive"
    ])
    
    print("\nSecond init (with force) exit code:", result2.exit_code)
    print("Second init output:", result2.output)
    
    if result2.exception:
        import traceback
        traceback.print_exception(type(result2.exception), result2.exception, result2.exception.__traceback__)
