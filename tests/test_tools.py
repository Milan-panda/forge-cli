import os
import pytest
from src.tools.shell import ShellTool
from src.tools.files import ReadFileTool, WriteFileTool

def test_shell_tool():
    tool = ShellTool()
    output = tool.run("echo 'hello world'")
    assert "hello world" in output

def test_file_tools(tmp_path):
    write_tool = WriteFileTool()
    read_tool = ReadFileTool()
    
    file_path = tmp_path / "test.txt"
    str_path = str(file_path)
    
    # Test Write
    result = write_tool.run(str_path, "content")
    assert "Successfully wrote" in result
    assert file_path.read_text() == "content"
    
    # Test Read
    content = read_tool.run(str_path)
    assert content == "content"
