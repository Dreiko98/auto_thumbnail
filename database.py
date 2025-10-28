"""
Sistema de base de datos para el generador de thumbnails.
Gestiona usuarios, autenticación y tokens de OpenAI.
"""

import sqlite3
import hashlib
import secrets
import os
from datetime import datetime
from contextlib import contextmanager

# Usar variable de entorno para la ruta de la base de datos (útil para Docker)
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'thumbnail_users.db')

# Asegurar que el directorio existe
db_dir = os.path.dirname(DATABASE_PATH)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)
    print(f"📁 Directorio de base de datos creado: {db_dir}")

@contextmanager
def get_db_connection():
    """Context manager para conexiones a la base de datos."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """Inicializa la base de datos con las tablas necesarias."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                openai_token TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabla de sesiones (opcional, para más control)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                ip_address TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Índices para mejorar rendimiento
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_token ON sessions(session_token)')
        
        print("✅ Base de datos inicializada correctamente")


def hash_password(password, salt=None):
    """
    Hash seguro de contraseñas usando SHA-256 con salt.
    
    Args:
        password (str): Contraseña en texto plano
        salt (str, optional): Salt para el hash. Si no se provee, se genera uno nuevo.
        
    Returns:
        tuple: (password_hash, salt)
    """
    if salt is None:
        salt = secrets.token_hex(32)  # 64 caracteres hexadecimales
    
    # Combinar contraseña con salt y hashear
    password_with_salt = f"{password}{salt}".encode('utf-8')
    password_hash = hashlib.sha256(password_with_salt).hexdigest()
    
    return password_hash, salt


def verify_password(password, stored_hash, salt):
    """
    Verifica si una contraseña coincide con el hash almacenado.
    
    Args:
        password (str): Contraseña a verificar
        stored_hash (str): Hash almacenado en la base de datos
        salt (str): Salt usado para hashear
        
    Returns:
        bool: True si la contraseña es correcta
    """
    password_hash, _ = hash_password(password, salt)
    return password_hash == stored_hash


def create_user(username, password):
    """
    Crea un nuevo usuario en la base de datos.
    
    Args:
        username (str): Nombre de usuario (único)
        password (str): Contraseña en texto plano
        
    Returns:
        dict: Información del usuario creado o None si hubo error
    """
    try:
        # Hash de la contraseña
        password_hash, salt = hash_password(password)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password_hash, salt)
                VALUES (?, ?, ?)
            ''', (username, password_hash, salt))
            
            user_id = cursor.lastrowid
            
            print(f"✅ Usuario '{username}' creado exitosamente (ID: {user_id})")
            
            return {
                'id': user_id,
                'username': username,
                'created_at': datetime.now().isoformat()
            }
            
    except sqlite3.IntegrityError:
        print(f"❌ Error: El usuario '{username}' ya existe")
        return None
    except Exception as e:
        print(f"❌ Error al crear usuario: {str(e)}")
        return None


def authenticate_user(username, password):
    """
    Autentica un usuario verificando sus credenciales.
    
    Args:
        username (str): Nombre de usuario
        password (str): Contraseña en texto plano
        
    Returns:
        dict: Información del usuario si la autenticación es exitosa, None si falla
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, password_hash, salt, openai_token, is_active
                FROM users
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            
            if user is None:
                print(f"❌ Usuario '{username}' no encontrado")
                return None
            
            if not user['is_active']:
                print(f"❌ Usuario '{username}' está desactivado")
                return None
            
            # Verificar contraseña
            if verify_password(password, user['password_hash'], user['salt']):
                # Actualizar último login
                cursor.execute('''
                    UPDATE users
                    SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user['id'],))
                
                print(f"✅ Usuario '{username}' autenticado correctamente")
                
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'openai_token': user['openai_token'],
                    'has_openai_token': user['openai_token'] is not None
                }
            else:
                print(f"❌ Contraseña incorrecta para usuario '{username}'")
                return None
                
    except Exception as e:
        print(f"❌ Error al autenticar usuario: {str(e)}")
        return None


def get_user_by_id(user_id):
    """
    Obtiene información de un usuario por su ID.
    
    Args:
        user_id (int): ID del usuario
        
    Returns:
        dict: Información del usuario o None si no existe
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, openai_token, created_at, last_login
                FROM users
                WHERE id = ? AND is_active = 1
            ''', (user_id,))
            
            user = cursor.fetchone()
            
            if user:
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'openai_token': user['openai_token'],
                    'has_openai_token': user['openai_token'] is not None,
                    'created_at': user['created_at'],
                    'last_login': user['last_login']
                }
            return None
            
    except Exception as e:
        print(f"❌ Error al obtener usuario: {str(e)}")
        return None


def update_openai_token(user_id, openai_token):
    """
    Actualiza el token de OpenAI de un usuario.
    
    Args:
        user_id (int): ID del usuario
        openai_token (str): Token de OpenAI (puede ser None para eliminarlo)
        
    Returns:
        bool: True si se actualizó correctamente
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET openai_token = ?
                WHERE id = ?
            ''', (openai_token, user_id))
            
            if cursor.rowcount > 0:
                action = "actualizado" if openai_token else "eliminado"
                print(f"✅ Token de OpenAI {action} para usuario ID {user_id}")
                return True
            else:
                print(f"❌ Usuario ID {user_id} no encontrado")
                return False
                
    except Exception as e:
        print(f"❌ Error al actualizar token: {str(e)}")
        return False


def get_openai_token(user_id):
    """
    Obtiene el token de OpenAI de un usuario.
    
    Args:
        user_id (int): ID del usuario
        
    Returns:
        str: Token de OpenAI o None si no tiene
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT openai_token
                FROM users
                WHERE id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            return result['openai_token'] if result else None
            
    except Exception as e:
        print(f"❌ Error al obtener token: {str(e)}")
        return None


def change_password(user_id, old_password, new_password):
    """
    Cambia la contraseña de un usuario.
    
    Args:
        user_id (int): ID del usuario
        old_password (str): Contraseña actual
        new_password (str): Nueva contraseña
        
    Returns:
        bool: True si se cambió correctamente
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar contraseña actual
            cursor.execute('''
                SELECT password_hash, salt
                FROM users
                WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            
            if not user:
                print(f"❌ Usuario ID {user_id} no encontrado")
                return False
            
            if not verify_password(old_password, user['password_hash'], user['salt']):
                print(f"❌ Contraseña actual incorrecta")
                return False
            
            # Generar nuevo hash con nuevo salt
            new_hash, new_salt = hash_password(new_password)
            
            cursor.execute('''
                UPDATE users
                SET password_hash = ?, salt = ?
                WHERE id = ?
            ''', (new_hash, new_salt, user_id))
            
            print(f"✅ Contraseña actualizada para usuario ID {user_id}")
            return True
            
    except Exception as e:
        print(f"❌ Error al cambiar contraseña: {str(e)}")
        return False


# Inicializar la base de datos al importar el módulo
if __name__ == '__main__':
    init_database()
    print("\n🗄️  Base de datos lista para usar")
