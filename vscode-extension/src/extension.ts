import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    const config = vscode.workspace.getConfiguration('jarvis');
    const apiUrl = config.get<string>('apiUrl', 'http://localhost:5000');
    
    // Generate Code Command
    const generateCodeCommand = vscode.commands.registerCommand('jarvis.generateCode', async () => {
        const prompt = await vscode.window.showInputBox({
            prompt: 'Describe the code you want to generate',
            placeHolder: 'e.g., Python function to sort a list'
        });
        
        if (!prompt) {
            return;
        }
        
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "JARVIS: Generating Code",
            cancellable: false
        }, async (progress) => {
            try {
                const response = await axios.post(`${apiUrl}/api/ai/generate-code`, {
                    prompt: prompt,
                    language: getCurrentLanguage()
                });
                
                const code = response.data.code;
                const editor = vscode.window.activeTextEditor;
                
                if (editor) {
                    const position = editor.selection.active;
                    editor.edit(editBuilder => {
                        editBuilder.insert(position, code);
                    });
                } else {
                    // Create new file
                    const doc = await vscode.workspace.openTextDocument({
                        content: code,
                        language: getCurrentLanguage()
                    });
                    await vscode.window.showTextDocument(doc);
                }
                
                vscode.window.showInformationMessage('Code generated successfully!');
            } catch (error: any) {
                vscode.window.showErrorMessage(`JARVIS Error: ${error.message}`);
            }
        });
    });
    
    // Explain Code Command
    const explainCodeCommand = vscode.commands.registerCommand('jarvis.explainCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor');
            return;
        }
        
        const selection = editor.document.getText(editor.selection);
        if (!selection) {
            vscode.window.showWarningMessage('Please select code to explain');
            return;
        }
        
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "JARVIS: Explaining Code",
            cancellable: false
        }, async (progress) => {
            try {
                const response = await axios.post(`${apiUrl}/api/ai/explain-code`, {
                    code: selection,
                    language: editor.document.languageId
                });
                
                const explanation = response.data.explanation;
                
                // Show explanation in new document
                const doc = await vscode.workspace.openTextDocument({
                    content: `Code Explanation:\n\n${explanation}\n\n---\n\nOriginal Code:\n${selection}`,
                    language: 'markdown'
                });
                await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
                
                vscode.window.showInformationMessage('Code explanation generated!');
            } catch (error: any) {
                vscode.window.showErrorMessage(`JARVIS Error: ${error.message}`);
            }
        });
    });
    
    // Fix Bugs Command
    const fixBugsCommand = vscode.commands.registerCommand('jarvis.fixBugs', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }
        
        const selection = editor.document.getText(editor.selection) || editor.document.getText();
        
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "JARVIS: Fixing Bugs",
            cancellable: false
        }, async (progress) => {
            try {
                const response = await axios.post(`${apiUrl}/api/ai/fix-bugs`, {
                    code: selection,
                    language: editor.document.languageId
                });
                
                const fixedCode = response.data.fixed_code;
                const issues = response.data.issues;
                
                // Replace code
                if (editor.selection.isEmpty) {
                    const fullRange = new vscode.Range(
                        editor.document.positionAt(0),
                        editor.document.positionAt(editor.document.getText().length)
                    );
                    editor.edit(editBuilder => {
                        editBuilder.replace(fullRange, fixedCode);
                    });
                } else {
                    editor.edit(editBuilder => {
                        editBuilder.replace(editor.selection, fixedCode);
                    });
                }
                
                vscode.window.showInformationMessage(`Fixed ${issues.length} issues!`);
            } catch (error: any) {
                vscode.window.showErrorMessage(`JARVIS Error: ${error.message}`);
            }
        });
    });
    
    // Refactor Command
    const refactorCommand = vscode.commands.registerCommand('jarvis.refactor', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }
        
        const selection = editor.document.getText(editor.selection);
        if (!selection) {
            vscode.window.showWarningMessage('Please select code to refactor');
            return;
        }
        
        const refactorType = await vscode.window.showQuickPick([
            'Improve readability',
            'Optimize performance',
            'Extract function',
            'Simplify logic'
        ], {
            placeHolder: 'Select refactoring type'
        });
        
        if (!refactorType) {
            return;
        }
        
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "JARVIS: Refactoring Code",
            cancellable: false
        }, async (progress) => {
            try {
                const response = await axios.post(`${apiUrl}/api/ai/refactor`, {
                    code: selection,
                    language: editor.document.languageId,
                    refactor_type: refactorType
                });
                
                const refactoredCode = response.data.refactored_code;
                
                editor.edit(editBuilder => {
                    editBuilder.replace(editor.selection, refactoredCode);
                });
                
                vscode.window.showInformationMessage('Code refactored successfully!');
            } catch (error: any) {
                vscode.window.showErrorMessage(`JARVIS Error: ${error.message}`);
            }
        });
    });
    
    // Ask Question Command
    const askQuestionCommand = vscode.commands.registerCommand('jarvis.askQuestion', async () => {
        const question = await vscode.window.showInputBox({
            prompt: 'Ask JARVIS a question',
            placeHolder: 'e.g., How do I implement a binary search?'
        });
        
        if (!question) {
            return;
        }
        
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "JARVIS: Thinking...",
            cancellable: false
        }, async (progress) => {
            try {
                const response = await axios.post(`${apiUrl}/api/chat`, {
                    message: question
                });
                
                const answer = response.data.response;
                
                // Show answer in output channel
                const outputChannel = vscode.window.createOutputChannel('JARVIS');
                outputChannel.appendLine(`Q: ${question}`);
                outputChannel.appendLine(`A: ${answer}`);
                outputChannel.show();
            } catch (error: any) {
                vscode.window.showErrorMessage(`JARVIS Error: ${error.message}`);
            }
        });
    });
    
    // Register all commands
    context.subscriptions.push(
        generateCodeCommand,
        explainCodeCommand,
        fixBugsCommand,
        refactorCommand,
        askQuestionCommand
    );
    
    vscode.window.showInformationMessage('JARVIS AI Assistant is now active!');
}

function getCurrentLanguage(): string {
    const editor = vscode.window.activeTextEditor;
    return editor?.document.languageId || 'python';
}

export function deactivate() {}
