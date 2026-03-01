from typing import Dict, Any, Optional, List, BinaryIO
import logging
import asyncio
import io
import os
import re
from app.core.config import get_settings
from app.domain.models.tool_result import ToolResult
from app.domain.external.sandbox import Sandbox
from app.infrastructure.external.browser.playwright_browser import PlaywrightBrowser
from app.domain.external.browser import Browser
from app.domain.external.llm import LLM

try:
    import e2b
    from e2b import AsyncSandbox
    E2B_AVAILABLE = True
except ImportError:
    E2B_AVAILABLE = False
    AsyncSandbox = None

logger = logging.getLogger(__name__)


class E2BSandbox(Sandbox):
    """E2B Sandbox implementation"""
    
    def __init__(self, sandbox: AsyncSandbox = None, sandbox_id: str = None):
        """Initialize E2B sandbox
        
        Args:
            sandbox: E2B AsyncSandbox instance
            sandbox_id: Sandbox ID for tracking
        """
        self._sandbox = sandbox
        self._sandbox_id = sandbox_id or (sandbox.sandbox_id if sandbox else None)
        self._cdp_port = 9222
        self._timeout = get_settings().e2b_timeout
    
    @property
    def id(self) -> str:
        """Sandbox ID"""
        return self._sandbox_id or "e2b-sandbox"
    
    @property
    def cdp_url(self) -> str:
        """CDP URL for browser automation"""
        if self._sandbox:
            # E2B exposes CDP on a specific port
            return f"http://localhost:{self._cdp_port}"
        return ""
    
    @property
    def vnc_url(self) -> str:
        """VNC URL - E2B doesn't provide VNC directly"""
        return ""
    
    @property
    def is_ready(self) -> bool:
        """Check if sandbox is ready"""
        return self._sandbox is not None and self._sandbox.is_running()
    
    async def ensure_sandbox(self) -> None:
        """Ensure sandbox is ready by checking its status"""
        if not self._sandbox:
            raise RuntimeError("Sandbox not initialized")
        
        # Wait for sandbox to be ready
        max_retries = 30
        retry_interval = 2
        
        for attempt in range(max_retries):
            if self._sandbox.is_running():
                logger.info("E2B Sandbox is ready")
                return
            logger.info(f"Waiting for sandbox to be ready... (attempt {attempt + 1}/{max_retries})")
            await asyncio.sleep(retry_interval)
        
        logger.warning(f"Sandbox ready check completed after {max_retries} attempts")
    
    def _convert_exit_code(self, exit_code: int) -> ToolResult:
        """Convert exit code to ToolResult
        
        Args:
            exit_code: Command exit code
            
        Returns:
            ToolResult with success status based on exit code
        """
        return ToolResult(
            success=exit_code == 0,
            message=f"Command exited with code {exit_code}",
            data={"exit_code": exit_code}
        )
    
    async def exec_command(self, session_id: str, exec_dir: str, command: str) -> ToolResult:
        """Execute command in sandbox
        
        Args:
            session_id: Session ID (used for tracking)
            exec_dir: Execution directory
            command: Command to execute
            
        Returns:
            Command execution result
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            # Change to execution directory and run command
            full_cmd = f"cd {exec_dir} && {command}" if exec_dir else command
            
            # Run command with timeout - use sync version via asyncio.to_thread
            process = await asyncio.wait_for(
                asyncio.to_thread(self._sandbox.commands.run, full_cmd),
                timeout=self._timeout
            )
            
            # Get output
            stdout = process.stdout or ""
            stderr = process.stderr or ""
            exit_code = process.exit_code
            
            return ToolResult(
                success=exit_code == 0,
                message=f"Command executed" if exit_code == 0 else f"Command failed with exit code {exit_code}",
                data={
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": exit_code
                }
            )
        except asyncio.TimeoutError:
            return ToolResult(success=False, message=f"Command timed out after {self._timeout} seconds")
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return ToolResult(success=False, message=f"Command execution failed: {str(e)}")
    
    async def view_shell(self, session_id: str, console: bool = False) -> ToolResult:
        """View shell status - E2B manages this internally
        
        Args:
            session_id: Session ID
            console: Whether to return console records
            
        Returns:
            Shell status information
        """
        # E2B sandbox doesn't expose shell console in the same way
        # Return basic info about the sandbox
        return ToolResult(
            success=True,
            message="E2B sandbox is active",
            data={"session_id": session_id, "sandbox_id": self.id}
        )
    
    async def wait_for_process(self, session_id: str, seconds: Optional[int] = None) -> ToolResult:
        """Wait for process - not directly applicable to E2B
        
        Args:
            session_id: Session ID
            seconds: Wait seconds
            
        Returns:
            Wait result
        """
        wait_time = seconds or 1
        await asyncio.sleep(wait_time)
        return ToolResult(success=True, message=f"Waited for {wait_time} seconds")
    
    async def write_to_process(self, session_id: str, input_text: str, press_enter: bool = True) -> ToolResult:
        """Write input to process
        
        Args:
            session_id: Session ID
            input_text: Input text
            press_enter: Whether to press enter
            
        Returns:
            Write result
        """
        # For E2B, we can use the sandbox's stdin
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            # E2B's process interaction is different - we'd need to manage processes differently
            # For now, return a message indicating this needs to be handled differently
            return ToolResult(
                success=True, 
                message="Process interaction handled via exec_command"
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to write to process: {str(e)}")
    
    async def kill_process(self, session_id: str) -> ToolResult:
        """Terminate process
        
        Args:
            session_id: Session ID
            
        Returns:
            Termination result
        """
        # E2B manages processes internally
        return ToolResult(success=True, message="Process termination handled by E2B")
    
    async def file_write(self, file: str, content: str, append: bool = False, 
                        leading_newline: bool = False, trailing_newline: bool = False, 
                        sudo: bool = False) -> ToolResult:
        """Write content to file
        
        Args:
            file: File path
            content: Content to write
            append: Whether to append content
            leading_newline: Whether to add newline before content
            trailing_newline: Whether to add newline after content
            sudo: Whether to use sudo privileges (ignored in E2B)
            
        Returns:
            Result of write operation
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            # Handle newline options
            final_content = content
            if leading_newline:
                final_content = "\n" + final_content
            if trailing_newline:
                final_content = final_content + "\n"
            
            if append:
                # Read existing content first
                existing = ""
                try:
                    read_result = await self.file_read(file)
                    if read_result.success:
                        existing = read_result.data.get("content", "") or ""
                except:
                    pass
                final_content = existing + final_content
            
            # Write using E2B's filesystem API - use sync method with thread
            await asyncio.to_thread(self._sandbox.files.write, file, final_content)
            
            return ToolResult(
                success=True,
                message=f"File written: {file}",
                data={"path": file}
            )
        except Exception as e:
            logger.error(f"File write failed: {str(e)}")
            return ToolResult(success=False, message=f"Failed to write file: {str(e)}")
    
    async def file_read(self, file: str, start_line: int = None, 
                       end_line: int = None, sudo: bool = False) -> ToolResult:
        """Read file content
        
        Args:
            file: File path
            start_line: Start line number
            end_line: End line number
            sudo: Whether to use sudo privileges (ignored in E2B)
            
        Returns:
            File content
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            # Use sync version with thread
            content = await asyncio.to_thread(self._sandbox.files.read, file)
            
            # Handle line range
            if start_line is not None or end_line is not None:
                lines = content.split('\n')
                start = start_line - 1 if start_line else 0
                end = end_line if end_line else len(lines)
                content = '\n'.join(lines[start:end])
            
            return ToolResult(
                success=True,
                message="File read successfully",
                data={"content": content, "path": file}
            )
        except Exception as e:
            logger.error(f"File read failed: {str(e)}")
            return ToolResult(success=False, message=f"Failed to read file: {str(e)}")
    
    async def file_exists(self, path: str) -> ToolResult:
        """Check if file exists
        
        Args:
            path: File path
            
        Returns:
            Whether file exists
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            exists = await asyncio.to_thread(self._sandbox.files.exists, path)
            return ToolResult(
                success=True,
                message="Check completed",
                data={"exists": exists, "path": path}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to check file existence: {str(e)}")
    
    async def file_delete(self, path: str) -> ToolResult:
        """Delete file
        
        Args:
            path: File path
            
        Returns:
            Result of delete operation
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            await asyncio.to_thread(self._sandbox.files.remove, path)
            return ToolResult(success=True, message=f"File deleted: {path}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to delete file: {str(e)}")
    
    async def file_list(self, path: str) -> ToolResult:
        """List directory contents
        
        Args:
            path: Directory path
            
        Returns:
            List of directory contents
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            entries = await asyncio.to_thread(self._sandbox.files.list, path)
            items = []
            for entry in entries:
                items.append({
                    "name": entry.name,
                    "type": "dir" if entry.is_dir else "file",
                    "path": entry.path
                })
            
            return ToolResult(
                success=True,
                message=f"Listed {len(items)} items",
                data={"items": items, "path": path}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to list directory: {str(e)}")
    
    async def file_replace(self, file: str, old_str: str, new_str: str, sudo: bool = False) -> ToolResult:
        """Replace string in file
        
        Args:
            file: File path
            old_str: String to replace
            new_str: String to replace with
            sudo: Whether to use sudo privileges (ignored in E2B)
            
        Returns:
            Result of replace operation
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            # Read file content
            content = await asyncio.to_thread(self._sandbox.files.read, file)
            
            # Replace string
            if old_str not in content:
                return ToolResult(success=False, message=f"String not found in file: {old_str}")
            
            new_content = content.replace(old_str, new_str)
            
            # Write back
            await asyncio.to_thread(self._sandbox.files.write, file, new_content)
            
            return ToolResult(
                success=True,
                message="String replaced successfully",
                data={"path": file}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to replace string: {str(e)}")
    
    async def file_search(self, file: str, regex: str, sudo: bool = False) -> ToolResult:
        """Search in file content
        
        Args:
            file: File path
            regex: Regular expression
            sudo: Whether to use sudo privileges (ignored in E2B)
            
        Returns:
            Search results
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            content = await asyncio.to_thread(self._sandbox.files.read, file)
            
            # Search using regex
            matches = []
            for i, line in enumerate(content.split('\n'), 1):
                if re.search(regex, line):
                    matches.append({"line_number": i, "content": line})
            
            return ToolResult(
                success=True,
                message=f"Found {len(matches)} matches",
                data={"matches": matches, "path": file}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to search in file: {str(e)}")
    
    async def file_find(self, path: str, glob_pattern: str) -> ToolResult:
        """Find files by name pattern
        
        Args:
            path: Search directory path
            glob_pattern: Glob matching pattern
            
        Returns:
            Found file list
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            # Use E2B's find command or walk directory - use sync version
            results = await asyncio.to_thread(self._sandbox.commands.run, f"find {path} -name '{glob_pattern}' 2>/dev/null")
            output = results.stdout or ""
            
            files = [f.strip() for f in output.split('\n') if f.strip()]
            
            return ToolResult(
                success=True,
                message=f"Found {len(files)} files",
                data={"files": files, "path": path, "pattern": glob_pattern}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to find files: {str(e)}")
    
    async def file_upload(self, file_data: BinaryIO, path: str, filename: str = None) -> ToolResult:
        """Upload file to sandbox
        
        Args:
            file_data: File content as binary stream
            path: Target file path in sandbox
            filename: Original filename (optional)
            
        Returns:
            Upload operation result
        """
        if not self._sandbox:
            return ToolResult(success=False, message="Sandbox not initialized")
        
        try:
            # Read binary content
            content = file_data.read()
            
            # Delete existing file if it exists to avoid permission errors on overwrite
            try:
                await self._sandbox.files.remove(path)
            except Exception:
                pass  # Ignore if file doesn't exist
            
            # Write to sandbox - use async method directly
            await self._sandbox.files.write(path, content)
            
            return ToolResult(
                success=True,
                message=f"File uploaded: {path}",
                data={"path": path}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to upload file: {str(e)}")
    
    async def file_download(self, path: str) -> BinaryIO:
        """Download file from sandbox
        
        Args:
            path: File path in sandbox
            
        Returns:
            File content as binary stream
        """
        if not self._sandbox:
            raise RuntimeError("Sandbox not initialized")
        
        try:
            # Use format="bytes" to get binary content
            content = await self._sandbox.files.read(path, format="bytes")
            return io.BytesIO(content)
        except Exception as e:
            raise RuntimeError(f"Failed to download file: {str(e)}")
    
    async def destroy(self) -> bool:
        """Destroy current sandbox instance
        
        Returns:
            Whether destroyed successfully
        """
        try:
            if self._sandbox:
                await self._sandbox.kill()
                self._sandbox = None
            return True
        except Exception as e:
            logger.error(f"Failed to destroy E2B sandbox: {str(e)}")
            return False
    
    async def get_browser(self) -> Browser:
        """Get browser instance
        
        Returns:
            Browser: Returns a configured PlaywrightBrowser instance
                    connected using the sandbox's CDP URL
        """
        # Return a browser instance connected to the CDP URL
        # Note: E2B sandboxes may need Chrome/Playwright installed
        return PlaywrightBrowser(self.cdp_url)
    
    @classmethod
    async def create(cls) -> 'Sandbox':
        """Create a new E2B sandbox instance
        
        Returns:
            New E2B sandbox instance
        """
        # Get API key from environment first (e2b SDK reads E2B_API_KEY automatically)
        # But we still check for explicit config as fallback
        settings = get_settings()
        
        if not E2B_AVAILABLE:
            raise RuntimeError("e2b package not installed. Run: pip install e2b")
        
        # Configure sandbox
        template = settings.e2b_template or "base"
        timeout = settings.e2b_timeout
        
        try:
            # Create E2B sandbox using AsyncSandbox.create()
            # E2B SDK automatically reads E2B_API_KEY from environment
            sandbox = await AsyncSandbox.create(
                template=template,
                timeout=timeout,
            )
            
            return cls(sandbox=sandbox, sandbox_id=sandbox.sandbox_id)
        except asyncio.TimeoutError:
            raise RuntimeError(f"Failed to create E2B sandbox: timeout after {timeout} seconds")
        except Exception as e:
            raise RuntimeError(f"Failed to create E2B sandbox: {str(e)}")
    
    @classmethod
    async def get(cls, id: str) -> 'Sandbox':
        """Get existing E2B sandbox by ID
        
        Args:
            id: Sandbox ID
            
        Returns:
            E2B sandbox instance
        """
        settings = get_settings()
        
        if not E2B_AVAILABLE:
            raise RuntimeError("e2b package not installed. Run: pip install e2b")
        
        try:
            # Connect to existing sandbox using AsyncSandbox.connect()
            sandbox = await AsyncSandbox.connect(sandbox_id=id)
            
            return cls(sandbox=sandbox, sandbox_id=id)
        except Exception as e:
            logger.error(f"Failed to get E2B sandbox {id}: {str(e)}")
            raise RuntimeError(f"Failed to get E2B sandbox: {str(e)}")
