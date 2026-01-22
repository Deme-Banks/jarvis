"""
VS Code Extension Integration
"""
import json
import os
from typing import Dict, List, Optional
from pathlib import Path


class VSCodeExtension:
    """VS Code extension integration for JARVIS"""
    
    def __init__(self):
        self.vscode_paths = self._find_vscode_paths()
    
    def _find_vscode_paths(self) -> List[Path]:
        """Find VS Code installation paths"""
        paths = []
        
        # Windows
        if os.name == 'nt':
            appdata = os.getenv('APPDATA')
            if appdata:
                paths.append(Path(appdata) / 'Code' / 'User')
            localappdata = os.getenv('LOCALAPPDATA')
            if localappdata:
                paths.append(Path(localappdata) / 'Programs' / 'Microsoft VS Code')
        
        # Linux/Mac
        else:
            home = Path.home()
            paths.append(home / '.config' / 'Code' / 'User')
            paths.append(home / '.vscode')
        
        return [p for p in paths if p.exists()]
    
    def create_extension_manifest(self, extension_name: str = "jarvis-assistant") -> Dict:
        """Create VS Code extension manifest"""
        manifest = {
            "name": extension_name,
            "displayName": "JARVIS Assistant",
            "description": "AI-powered coding assistant with voice commands",
            "version": "1.0.0",
            "publisher": "jarvis",
            "engines": {
                "vscode": "^1.80.0"
            },
            "categories": [
                "Other",
                "Machine Learning",
                "AI"
            ],
            "activationEvents": [
                "onCommand:jarvis.activate",
                "onCommand:jarvis.chat",
                "onCommand:jarvis.generateCode"
            ],
            "main": "./out/extension.js",
            "contributes": {
                "commands": [
                    {
                        "command": "jarvis.activate",
                        "title": "Activate JARVIS"
                    },
                    {
                        "command": "jarvis.chat",
                        "title": "Chat with JARVIS"
                    },
                    {
                        "command": "jarvis.generateCode",
                        "title": "Generate Code"
                    },
                    {
                        "command": "jarvis.explainCode",
                        "title": "Explain Code"
                    },
                    {
                        "command": "jarvis.fixCode",
                        "title": "Fix Code Issues"
                    }
                ],
                "keybindings": [
                    {
                        "command": "jarvis.activate",
                        "key": "ctrl+shift+j",
                        "mac": "cmd+shift+j"
                    }
                ],
                "configuration": {
                    "title": "JARVIS",
                    "properties": {
                        "jarvis.apiUrl": {
                            "type": "string",
                            "default": "http://localhost:5000",
                            "description": "JARVIS API URL"
                        },
                        "jarvis.enableVoice": {
                            "type": "boolean",
                            "default": True,
                            "description": "Enable voice commands"
                        }
                    }
                }
            }
        }
        
        return manifest
    
    def generate_extension_code(self) -> str:
        """Generate VS Code extension TypeScript code"""
        code = '''import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    const config = vscode.workspace.getConfiguration('jarvis');
    const apiUrl = config.get<string>('apiUrl', 'http://localhost:5000');
    
    // Activate JARVIS
    const activateCommand = vscode.commands.registerCommand('jarvis.activate', async () => {
        vscode.window.showInformationMessage('JARVIS Activated!');
    });
    
    // Chat with JARVIS
    const chatCommand = vscode.commands.registerCommand('jarvis.chat', async () => {
        const input = await vscode.window.showInputBox({
            prompt: 'Ask JARVIS anything...',
            placeHolder: 'Type your question'
        });
        
        if (input) {
            try {
                const response = await axios.post(`${apiUrl}/api/chat`, {
                    message: input
                });
                vscode.window.showInformationMessage(response.data.response);
            } catch (error) {
                vscode.window.showErrorMessage('JARVIS error: ' + error);
            }
        }
    });
    
    // Generate Code
    const generateCodeCommand = vscode.commands.registerCommand('jarvis.generateCode', async () => {
        const description = await vscode.window.showInputBox({
            prompt: 'Describe the code you want to generate',
            placeHolder: 'e.g., Python function to sort a list'
        });
        
        if (description) {
            try {
                const response = await axios.post(`${apiUrl}/api/generate-code`, {
                    description: description,
                    language: 'python'
                });
                
                const editor = vscode.window.activeTextEditor;
                if (editor) {
                    editor.edit(editBuilder => {
                        editBuilder.insert(editor.selection.active, response.data.code);
                    });
                }
            } catch (error) {
                vscode.window.showErrorMessage('Code generation error: ' + error);
            }
        }
    });
    
    // Explain Code
    const explainCodeCommand = vscode.commands.registerCommand('jarvis.explainCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor');
            return;
        }
        
        const selectedText = editor.document.getText(editor.selection);
        if (!selectedText) {
            vscode.window.showWarningMessage('No code selected');
            return;
        }
        
        try {
            const response = await axios.post(`${apiUrl}/api/explain-code`, {
                code: selectedText
            });
            
            const panel = vscode.window.createWebviewPanel(
                'jarvisExplanation',
                'JARVIS Code Explanation',
                vscode.ViewColumn.Beside,
                {}
            );
            panel.webview.html = `<h1>Code Explanation</h1><p>${response.data.explanation}</p>`;
        } catch (error) {
            vscode.window.showErrorMessage('Explanation error: ' + error);
        }
    });
    
    context.subscriptions.push(activateCommand, chatCommand, generateCodeCommand, explainCodeCommand);
}

export function deactivate() {}
'''
        return code
    
    def install_extension(self, extension_path: str) -> Dict:
        """Install VS Code extension"""
        try:
            import subprocess
            result = subprocess.run(
                ['code', '--install-extension', extension_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {"error": str(e)}
