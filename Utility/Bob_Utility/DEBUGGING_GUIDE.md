# 🐛 Debugging Guide - Enterprise Payload Utility Toolkit

## 🎯 How to Start the Application with Debugger

### Method 1: Using VS Code Debugger (Recommended)

1. **Stop the Current Server**
   - Go to the terminal where the server is running
   - Press `Ctrl+C` to stop it

2. **Open Debug Panel**
   - Press `Ctrl+Shift+D` (or click the Debug icon in the left sidebar)
   - Or go to: View → Run

3. **Select Debug Configuration**
   - At the top of the Debug panel, you'll see a dropdown
   - Select **"Python: FastAPI"**

4. **Start Debugging**
   - Press `F5` (or click the green play button)
   - The application will start with the debugger attached

5. **Verify It's Running**
   - You should see debug controls at the top (pause, step over, step into, etc.)
   - Check the Debug Console for output
   - Visit http://localhost:8000 to confirm it's working

### Method 2: Using VS Code Debug Console

1. **Open Command Palette**
   - Press `Ctrl+Shift+P`

2. **Type and Select**
   - Type: "Debug: Start Debugging"
   - Select it from the list

3. **Choose Configuration**
   - Select "Python: FastAPI"

### Method 3: Manual Debug Attach

If you want to keep the server running and attach the debugger:

1. **Install debugpy** (if not already installed):
   ```bash
   pip install debugpy
   ```

2. **Modify app/main.py** to add debug support:
   ```python
   # Add at the top of app/main.py
   import debugpy
   
   # Add before if __name__ == "__main__":
   if settings.debug:
       debugpy.listen(("0.0.0.0", 5678))
       print("Waiting for debugger attach...")
       debugpy.wait_for_client()
   ```

3. **Create attach configuration** in `.vscode/launch.json`:
   ```json
   {
       "name": "Python: Attach",
       "type": "debugpy",
       "request": "attach",
       "connect": {
           "host": "localhost",
           "port": 5678
       }
   }
   ```

## 🔍 Setting Breakpoints

### How to Set Breakpoints

1. **Open a Python file** (e.g., `app/main.py`)

2. **Click in the gutter** (left of line numbers)
   - A red dot will appear
   - This is your breakpoint

3. **Or use F9** while cursor is on a line

### Strategic Breakpoint Locations

**In app/main.py:**
```python
@app.get("/")
async def root() -> dict:
    # Set breakpoint here to debug root endpoint
    return {
        "name": settings.app_name,
        ...
    }
```

**In app/services/xml/parser.py:**
```python
def parse(self, content: str) -> etree._Element:
    try:
        # Set breakpoint here to debug XML parsing
        root = etree.fromstring(content.encode("utf-8"), parser=self.parser)
        ...
```

**In app/core/file_handler.py:**
```python
def read_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    # Set breakpoint here to debug file operations
    file_path = Path(file_path)
    ...
```

## 🎮 Debug Controls

Once debugging is active:

| Key | Action | Description |
|-----|--------|-------------|
| `F5` | Continue | Resume execution until next breakpoint |
| `F10` | Step Over | Execute current line, don't enter functions |
| `F11` | Step Into | Enter into function calls |
| `Shift+F11` | Step Out | Exit current function |
| `Ctrl+Shift+F5` | Restart | Restart the debugger |
| `Shift+F5` | Stop | Stop debugging |

## 📊 Debug Views

### Variables View
- Shows all variables in current scope
- Expand objects to see their properties
- Right-click to copy value or add to watch

### Watch View
- Add expressions to monitor
- Example: `settings.app_name`
- Example: `len(xml_content)`

### Call Stack View
- Shows the execution path
- Click on any frame to see its variables

### Debug Console
- Execute Python code in current context
- Example: `print(settings.debug)`
- Example: `type(root)`

## 🧪 Testing with Debugger

### Test API Endpoints

1. **Set breakpoint** in endpoint function

2. **Start debugger** (F5)

3. **Make request** using:
   - Browser: http://localhost:8000
   - cURL: `curl http://localhost:8000/health`
   - Postman/Insomnia
   - Python requests library

4. **Debugger will pause** at your breakpoint

5. **Inspect variables** and step through code

### Example Debug Session

```python
# In app/main.py, set breakpoint here:
@app.get("/health")
async def health_check() -> dict:
    # Breakpoint on next line
    return {
        "status": "healthy",
        "version": settings.app_version,
    }
```

**Steps:**
1. Start debugger (F5)
2. Open browser: http://localhost:8000/health
3. Debugger pauses at breakpoint
4. Inspect `settings.app_version` in Variables view
5. Press F5 to continue
6. See response in browser

## 🔧 Debug Configuration Details

Your current configuration (`.vscode/launch.json`):

```json
{
    "name": "Python: FastAPI",
    "type": "debugpy",
    "request": "launch",
    "module": "uvicorn",
    "args": [
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ],
    "jinja": true,
    "justMyCode": false,
    "env": {
        "PYTHONPATH": "${workspaceFolder}"
    },
    "console": "integratedTerminal"
}
```

**Key Settings:**
- `justMyCode: false` - Debug into library code
- `--reload` - Auto-restart on code changes
- `console: integratedTerminal` - Output in VS Code terminal

## 🚨 Common Issues

### Issue: Debugger Won't Start

**Solution:**
1. Check Python interpreter is correct (Ctrl+Shift+P → "Python: Select Interpreter")
2. Ensure uvicorn is installed: `pip list | findstr uvicorn`
3. Check no other process is using port 8000

### Issue: Breakpoints Not Hit

**Solution:**
1. Ensure code is actually executed (make a request to that endpoint)
2. Check breakpoint is on an executable line (not comments/blank lines)
3. Verify `justMyCode` is set to `false` in launch.json

### Issue: Can't See Variables

**Solution:**
1. Ensure you're paused at a breakpoint
2. Check the Variables view is expanded
3. Try adding expression to Watch view

## 💡 Pro Tips

1. **Conditional Breakpoints**
   - Right-click breakpoint → Edit Breakpoint
   - Add condition: `xml_content.startswith("<?xml")`

2. **Logpoints**
   - Right-click in gutter → Add Logpoint
   - Log message without stopping: `XML parsed: {len(root)}`

3. **Exception Breakpoints**
   - In Debug panel, check "Raised Exceptions"
   - Debugger will pause on any exception

4. **Debug Console Commands**
   ```python
   # Evaluate expressions
   settings.app_name
   
   # Call functions
   parser.validate(xml_content)
   
   # Import modules
   import json
   json.dumps({"test": "data"})
   ```

## 📚 Quick Reference

**Start Debugging**: `F5`
**Stop Debugging**: `Shift+F5`
**Toggle Breakpoint**: `F9`
**Step Over**: `F10`
**Step Into**: `F11`
**Step Out**: `Shift+F11`

## ✅ Verification Checklist

Before debugging:
- [ ] Server is stopped (no other instance running)
- [ ] Correct Python interpreter selected
- [ ] Dependencies installed
- [ ] `.vscode/launch.json` exists
- [ ] Breakpoints set in code you want to debug

## 🎯 Next Steps

1. **Stop the current server** (Ctrl+C in terminal)
2. **Press F5** to start debugging
3. **Set breakpoints** in code you want to inspect
4. **Make requests** to trigger breakpoints
5. **Inspect variables** and step through code

Happy Debugging! 🐛🔍