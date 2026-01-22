"""
Database Connectors - MySQL, PostgreSQL, MongoDB
"""
import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class DatabaseConnector:
    """Base database connector"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self) -> Dict:
        """Connect to database"""
        raise NotImplementedError
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute a query"""
        raise NotImplementedError
    
    def close(self):
        """Close connection"""
        if self.connection:
            self.connection.close()


class MySQLConnector(DatabaseConnector):
    """MySQL database connector"""
    
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        connection_string = f"mysql://{user}:{password}@{host}:{port}/{database}"
        super().__init__(connection_string)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def connect(self) -> Dict:
        """Connect to MySQL"""
        try:
            import mysql.connector
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return {"success": True, "message": "Connected to MySQL"}
        except ImportError:
            return {"error": "mysql-connector-python not installed. Install with: pip install mysql-connector-python"}
        except Exception as e:
            return {"error": str(e)}
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute MySQL query"""
        if not self.connection:
            return [{"error": "Not connected to database"}]
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or {})
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
            else:
                self.connection.commit()
                results = [{"rows_affected": cursor.rowcount}]
            
            cursor.close()
            return results
        except Exception as e:
            return [{"error": str(e)}]


class PostgreSQLConnector(DatabaseConnector):
    """PostgreSQL database connector"""
    
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        super().__init__(connection_string)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def connect(self) -> Dict:
        """Connect to PostgreSQL"""
        try:
            import psycopg2
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return {"success": True, "message": "Connected to PostgreSQL"}
        except ImportError:
            return {"error": "psycopg2 not installed. Install with: pip install psycopg2-binary"}
        except Exception as e:
            return {"error": str(e)}
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute PostgreSQL query"""
        if not self.connection:
            return [{"error": "Not connected to database"}]
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or {})
            
            if query.strip().upper().startswith('SELECT'):
                columns = [desc[0] for desc in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                self.connection.commit()
                results = [{"rows_affected": cursor.rowcount}]
            
            cursor.close()
            return results
        except Exception as e:
            return [{"error": str(e)}]


class MongoDBConnector(DatabaseConnector):
    """MongoDB database connector"""
    
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        connection_string = f"mongodb://{user}:{password}@{host}:{port}/{database}"
        super().__init__(connection_string)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def connect(self) -> Dict:
        """Connect to MongoDB"""
        try:
            from pymongo import MongoClient
            client = MongoClient(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password
            )
            self.connection = client[self.database]
            return {"success": True, "message": "Connected to MongoDB"}
        except ImportError:
            return {"error": "pymongo not installed. Install with: pip install pymongo"}
        except Exception as e:
            return {"error": str(e)}
    
    def execute_query(self, collection: str, query: Dict = None, 
                     operation: str = "find", data: Optional[Dict] = None) -> List[Dict]:
        """Execute MongoDB query"""
        if not self.connection:
            return [{"error": "Not connected to database"}]
        
        try:
            coll = self.connection[collection]
            
            if operation == "find":
                results = list(coll.find(query or {}))
                # Convert ObjectId to string
                for result in results:
                    if '_id' in result:
                        result['_id'] = str(result['_id'])
                return results
            elif operation == "insert_one":
                result = coll.insert_one(data or {})
                return [{"inserted_id": str(result.inserted_id)}]
            elif operation == "update_one":
                result = coll.update_one(query or {}, {"$set": data or {}})
                return [{"modified_count": result.modified_count}]
            elif operation == "delete_one":
                result = coll.delete_one(query or {})
                return [{"deleted_count": result.deleted_count}]
            else:
                return [{"error": f"Unknown operation: {operation}"}]
        except Exception as e:
            return [{"error": str(e)}]
