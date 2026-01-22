/**
 * Keyboard Shortcuts for JARVIS Dashboard
 */

// Keyboard shortcuts configuration
const shortcuts = {
    'Ctrl+K': {
        action: 'focusCommand',
        description: 'Focus command input'
    },
    'Ctrl+Enter': {
        action: 'executeCommand',
        description: 'Execute command'
    },
    'Escape': {
        action: 'clearResponse',
        description: 'Clear response'
    },
    'Ctrl+/': {
        action: 'showHelp',
        description: 'Show keyboard shortcuts'
    },
    'Ctrl+H': {
        action: 'showHistory',
        description: 'Show command history'
    },
    'Ctrl+S': {
        action: 'saveCommand',
        description: 'Save current command'
    }
};

// Initialize keyboard shortcuts
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        const key = e.key;
        const ctrl = e.ctrlKey || e.metaKey;
        const shift = e.shiftKey;
        const alt = e.altKey;
        
        // Build shortcut string
        let shortcut = '';
        if (ctrl) shortcut += 'Ctrl+';
        if (shift) shortcut += 'Shift+';
        if (alt) shortcut += 'Alt+';
        shortcut += key;
        
        // Check if shortcut exists
        if (shortcuts[shortcut]) {
            e.preventDefault();
            executeShortcut(shortcuts[shortcut].action);
        }
    });
    
    // Show shortcuts help
    showShortcutsHelp();
}

function executeShortcut(action) {
    switch(action) {
        case 'focusCommand':
            document.getElementById('command').focus();
            break;
        case 'executeCommand':
            if (typeof executeCommand === 'function') {
                executeCommand();
            }
            break;
        case 'clearResponse':
            document.getElementById('response').innerHTML = '';
            break;
        case 'showHelp':
            showShortcutsHelp();
            break;
        case 'showHistory':
            // Show command history
            break;
        case 'saveCommand':
            // Save current command
            break;
    }
}

function showShortcutsHelp() {
    // Create help overlay
    const helpHtml = `
        <div id="shortcutsHelp" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); background:var(--card-bg); padding:20px; border-radius:8px; z-index:10000; max-width:500px;">
            <h2>Keyboard Shortcuts</h2>
            <table style="width:100%; margin-top:10px;">
                ${Object.entries(shortcuts).map(([key, data]) => `
                    <tr>
                        <td><kbd>${key}</kbd></td>
                        <td>${data.description}</td>
                    </tr>
                `).join('')}
            </table>
            <button onclick="document.getElementById('shortcutsHelp').style.display='none'" style="margin-top:15px; padding:8px 16px;">Close</button>
        </div>
    `;
    
    if (!document.getElementById('shortcutsHelp')) {
        document.body.insertAdjacentHTML('beforeend', helpHtml);
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initKeyboardShortcuts);
} else {
    initKeyboardShortcuts();
}
