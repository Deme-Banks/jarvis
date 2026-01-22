"""
Database Optimization using SQLite for Faster Queries
"""
import sqlite3
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from contextlib import contextmanager


class OptimizedMemory:
    """SQLite-based memory system for faster queries"""
    
    def __init__(self, db_path: str = "./memory/jarvis.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    assistant_response TEXT NOT NULL,
                    context TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    confidence INTEGER DEFAULT 1,
                    learned_at TEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Knowledge table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    information TEXT NOT NULL,
                    source TEXT DEFAULT 'user',
                    confidence REAL DEFAULT 1.0,
                    timestamp TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patterns (
                    pattern TEXT PRIMARY KEY,
                    outcome TEXT NOT NULL,
                    count INTEGER DEFAULT 1,
                    last_used TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for faster queries
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_knowledge_topic ON knowledge(topic)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_patterns_count ON patterns(count)')
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def save_conversation(self, user_input: str, assistant_response: str, 
                         context: Optional[Dict] = None):
        """Save conversation (faster than JSON)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (timestamp, user_input, assistant_response, context)
                VALUES (?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                user_input,
                assistant_response,
                json.dumps(context) if context else None
            ))
            conn.commit()
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations (faster query)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM conversations
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def save_preference(self, key: str, value: Any):
        """Save preference (upsert)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO preferences (key, value, confidence, learned_at)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    confidence = confidence + 1,
                    updated_at = CURRENT_TIMESTAMP
            ''', (key, json.dumps(value), datetime.now().isoformat()))
            conn.commit()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get preference (fast lookup)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM preferences WHERE key = ?', (key,))
            row = cursor.fetchone()
            if row:
                return json.loads(row['value'])
            return default
    
    def add_knowledge(self, topic: str, information: str, source: str = "user"):
        """Add knowledge (with deduplication)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Check for duplicates
            cursor.execute('''
                SELECT id FROM knowledge
                WHERE topic = ? AND information = ?
            ''', (topic, information))
            
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO knowledge (topic, information, source, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (topic, information, source, datetime.now().isoformat()))
                conn.commit()
    
    def get_knowledge(self, topic: str, limit: int = 10) -> List[Dict]:
        """Get knowledge about topic (indexed query)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM knowledge
                WHERE topic = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (topic, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def save_pattern(self, pattern: str, outcome: str):
        """Save pattern (upsert with count)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO patterns (pattern, outcome, count, last_used)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(pattern) DO UPDATE SET
                    count = count + 1,
                    last_used = excluded.last_used
            ''', (pattern, outcome, datetime.now().isoformat()))
            conn.commit()
    
    def get_best_pattern(self, pattern: str) -> Optional[str]:
        """Get best pattern (fast query with index)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT outcome FROM patterns
                WHERE pattern LIKE ?
                ORDER BY count DESC
                LIMIT 1
            ''', (f"{pattern}%",))
            
            row = cursor.fetchone()
            if row and row['outcome']:
                return row['outcome']
            return None
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            cursor.execute('SELECT COUNT(*) as count FROM conversations')
            stats['conversations'] = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM preferences')
            stats['preferences'] = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM knowledge')
            stats['knowledge'] = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM patterns')
            stats['patterns'] = cursor.fetchone()['count']
            
            # Database size
            if os.path.exists(self.db_path):
                stats['db_size_mb'] = os.path.getsize(self.db_path) / (1024 * 1024)
            
            return stats
