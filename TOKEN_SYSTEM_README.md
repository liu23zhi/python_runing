# Token-Based Authentication System

## Overview

This system implements a secure token-based authentication mechanism for non-guest users with the following features:

- **2048-bit cryptographic tokens** using Python's `secrets` module
- **Cookie-based storage** with 1-hour expiration
- **Automatic token refresh** on user activity
- **Multi-device login detection** with automatic session invalidation
- **Persistent token storage** for session recovery

## Architecture

### Backend Components

#### 1. TokenManager Class (`main.py`)
Located after the `AuthSystem` class, manages all token operations:

```python
class TokenManager:
    def __init__(self, tokens_dir)
    def generate_token()              # Generate 2048-bit token
    def create_token(username, session_id)
    def verify_token(username, session_id, token)
    def refresh_token(username, session_id)
    def invalidate_token(username, session_id)
    def get_active_sessions(username)
    def detect_multi_device_login(username, new_session_id)
    def cleanup_expired_tokens(username)
```

#### 2. Token Storage
- **Directory**: `tokens/`
- **Format**: `{username_hash}_tokens.json`
- **Structure**:
```json
{
  "session-uuid-1": {
    "token": "2048-bit hex string",
    "session_id": "uuid",
    "created_at": 1234567890.0,
    "expires_at": 1234571490.0,
    "last_activity": 1234567890.0
  }
}
```

#### 3. Modified Endpoints

**`/auth/login` (POST)**
- Generates 2048-bit token for non-guest users
- Detects multi-device logins
- Kicks out old sessions
- Sets httponly cookies (`auth_token`, `session_id`)
- Returns: `{token, kicked_sessions_count, multi_device_warning}`

**`/api/<method>` (GET/POST)**
- Verifies token from cookie on each request
- Refreshes token expiration (extends 1 hour)
- Returns 401 with `need_login: true` on token failure
- Returns `logged_out_elsewhere: true` if kicked by another device

**`/auth/logout` (POST)**
- Invalidates token in backend
- Clears cookies
- Calls `cleanup_session()`

### Frontend Components

#### 1. Login Handler (`handleAuthLogin`)
```javascript
// Shows multi-device warnings
// Displays token generation confirmation
// Handles kicked_sessions_count
```

#### 2. API Call Handler (`callPythonAPI`)
```javascript
// Includes credentials: 'include' for cookies
// Detects token errors (need_login, logged_out_elsewhere)
// Shows appropriate error messages
// Auto-redirects to login on token failure
```

## Security Features

### Token Generation
- Uses `secrets.token_hex(256)` for cryptographically secure randomness
- 2048 bits = 256 bytes = 512 hex characters
- Collision probability: ~1 in 2^2048

### Cookie Security
- `httponly: True` - Prevents JavaScript access (XSS protection)
- `samesite: 'Lax'` - CSRF protection
- `secure: False` - Set to `True` in production (HTTPS only)
- `max_age: 3600` - 1 hour expiration

### Multi-Device Protection
1. When user logs in, system checks for existing active sessions
2. All old sessions are invalidated (tokens deleted)
3. Old devices receive `logged_out_elsewhere: true` error
4. User sees: "账号在别的地方登录，此地已自动登出"

## Usage Flow

### 1. User Login (Non-Guest)
```
1. User enters credentials in auth-login-container
2. POST /auth/login with username + password
3. Backend:
   - Authenticates user
   - Generates 2048-bit token
   - Stores token in tokens/{hash}.json
   - Detects old sessions
   - Invalidates old tokens
   - Returns success with token
4. Frontend:
   - Receives token in response
   - Browser stores token in httponly cookie
   - Shows multi-device warning if applicable
   - Redirects to session picker
```

### 2. API Calls (Authenticated User)
```
1. User performs action (e.g., load tasks)
2. Frontend calls callPythonAPI(method, args)
3. Request includes:
   - X-Session-ID header
   - auth_token cookie (automatic)
4. Backend:
   - Extracts token from cookie
   - Verifies token validity
   - Checks expiration
   - Refreshes expiration (+1 hour)
   - Updates last_activity
   - Returns response with refreshed cookie
```

### 3. Token Expiration
```
1. User inactive for >1 hour
2. Next API call:
   - Token verification fails (expired)
   - Returns 401 with need_login: true
3. Frontend:
   - Detects error
   - Shows "令牌已过期，请重新登录"
   - Redirects to login page after 2 seconds
```

### 4. Multi-Device Login
```
Device A (Old):
1. User logged in, has active token
2. User logs in on Device B
3. Device A's next API call:
   - Token invalid (was deleted)
   - Returns logged_out_elsewhere: true
4. Device A shows:
   - "您的账号已在其他设备登录，本设备已自动登出"
   - Redirects to login

Device B (New):
1. Login successful
2. Receives new token
3. Sees: "检测到该账号在其他 1 个设备上登录，已自动登出旧设备"
```

### 5. User Logout
```
1. User clicks logout button
2. POST /auth/logout
3. Backend:
   - Invalidates token
   - Deletes from storage
   - Clears session
4. Response sets cookies with max_age=0
5. Browser deletes cookies
6. Redirects to login page
```

## Token Lifecycle

```
[Login] -> Generate Token -> Store in File
                           -> Set Cookie (1h)
                           
[Activity] -> Verify Token -> Refresh Expiration (+1h)
                           -> Update Cookie
                           
[Logout] -> Invalidate Token -> Delete from File
                             -> Clear Cookie
                             
[Expire] -> Verify Fails -> Return 401
                         -> Redirect to Login
                         
[Multi-Device] -> Invalidate Old Tokens
               -> Kick Old Sessions
               -> Show Warning on Old Device
```

## Error Handling

### Token Not Found
- **Cause**: Cookie missing or session not found
- **Response**: `{"success": false, "message": "未找到认证令牌", "need_login": true}`
- **Action**: Redirect to login

### Token Expired
- **Cause**: More than 1 hour since last activity
- **Response**: `{"success": false, "message": "令牌已过期", "need_login": true}`
- **Action**: Show expiration message, redirect to login

### Token Mismatch
- **Cause**: Another device logged in (multi-device)
- **Response**: `{"success": false, "message": "令牌验证失败", "need_login": true, "logged_out_elsewhere": true}`
- **Action**: Show multi-device warning, redirect to login

## File Structure

```
python_running/
├── main.py                    # Backend implementation
│   ├── TokenManager class
│   ├── /auth/login endpoint
│   ├── /api/<method> endpoint
│   └── /auth/logout endpoint
├── index.html                 # Frontend implementation
│   ├── handleAuthLogin()
│   ├── callPythonAPI()
│   └── Token error handling
├── tokens/                    # Token storage (gitignored)
│   └── {username_hash}_tokens.json
└── .gitignore                 # Excludes tokens/
```

## Configuration

### Production Deployment
When deploying to production, update these settings in `main.py`:

```python
# In /auth/login endpoint
response.set_cookie(
    'auth_token',
    value=token,
    max_age=3600,
    httponly=True,
    secure=True,      # Change to True for HTTPS
    samesite='Strict' # Optional: stricter CSRF protection
)
```

### Token Expiration
To change token expiration time, update in `TokenManager`:

```python
def create_token(self, username, session_id):
    expires_at = created_at + 7200  # Change to 2 hours (7200 seconds)
```

And in the cookie setting:

```python
response.set_cookie(
    'auth_token',
    max_age=7200,  # Match the token expiration
    ...
)
```

## Testing

### Manual Test Checklist

1. **Login Test**
   - [ ] Register new user
   - [ ] Login with credentials
   - [ ] Verify token in browser cookies (DevTools > Application > Cookies)
   - [ ] Check token file in `tokens/` directory

2. **Token Refresh Test**
   - [ ] Make API calls
   - [ ] Verify cookie expiration extends
   - [ ] Check last_activity updates in token file

3. **Expiration Test**
   - [ ] Login
   - [ ] Wait >1 hour (or manually change expires_at)
   - [ ] Try API call
   - [ ] Verify redirect to login with expiration message

4. **Multi-Device Test**
   - [ ] Login on Browser A
   - [ ] Login same user on Browser B
   - [ ] Try API call on Browser A
   - [ ] Verify "logged out elsewhere" message on Browser A
   - [ ] Verify warning shown on Browser B during login

5. **Logout Test**
   - [ ] Login
   - [ ] Click logout
   - [ ] Verify cookies cleared
   - [ ] Verify token deleted from file
   - [ ] Verify cannot make API calls

### Automated Test (Python)

```python
import requests
import time

# Test login and token generation
def test_login():
    response = requests.post('http://localhost:5000/auth/login', 
        json={
            'auth_username': 'test_user',
            'auth_password': 'password123'
        },
        headers={'X-Session-ID': 'test-session-uuid'}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert 'token' in data
    assert len(data['token']) == 512  # 2048 bits
    assert 'auth_token' in response.cookies
    
    return response.cookies

# Test API call with token
def test_api_with_token(cookies):
    response = requests.post('http://localhost:5000/api/some_method',
        cookies=cookies,
        headers={'X-Session-ID': 'test-session-uuid'},
        json={}
    )
    
    assert response.status_code == 200
    # Verify cookie was refreshed
    assert 'auth_token' in response.cookies

# Test multi-device login
def test_multi_device():
    # Login on device 1
    cookies1 = test_login()
    
    # Login same user on device 2
    cookies2 = test_login()
    
    # Try API call with device 1 cookies (should fail)
    response = requests.post('http://localhost:5000/api/some_method',
        cookies=cookies1,
        headers={'X-Session-ID': 'test-session-uuid'},
        json={}
    )
    
    assert response.status_code == 401
    data = response.json()
    assert data['logged_out_elsewhere'] == True

if __name__ == '__main__':
    print("Running token system tests...")
    test_login()
    print("✓ Login test passed")
    # Add more tests...
```

## Troubleshooting

### "未找到认证令牌"
- Check browser cookies (DevTools > Application > Cookies)
- Verify `credentials: 'include'` in fetch requests
- Check if cookies are blocked by browser settings

### Token 验证失败
- Check token file exists in `tokens/` directory
- Verify username hash matches
- Check system time is synchronized

### Cookies 不生效
- Verify `httponly` cookies are enabled in browser
- Check `samesite` attribute compatibility
- For production: ensure `secure: True` with HTTPS

### 多设备登录未检测
- Check `detect_multi_device_login()` is called in `/auth/login`
- Verify token files are properly saved
- Check session cleanup is working

## Additional Notes

- Tokens are stored in plain text in JSON files (consider encryption for sensitive data)
- Token directory should have restricted permissions (chmod 700)
- Consider adding rate limiting to prevent brute force attacks
- Monitor token storage disk usage and implement cleanup of very old files
- Consider using Redis or database for high-traffic production systems
