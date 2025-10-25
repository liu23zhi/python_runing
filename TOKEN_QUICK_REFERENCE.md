# Token Authentication System - Quick Reference

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER LOGIN FLOW                                  │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────┐
│  User    │───▶│ Enter        │───▶│  POST           │───▶│  Backend   │
│  Browser │    │ Credentials  │    │  /auth/login    │    │  Auth      │
└──────────┘    └──────────────┘    └─────────────────┘    └────────────┘
                                                                    │
                                                                    ▼
                                            ┌────────────────────────────────┐
                                            │ 1. Verify credentials          │
                                            │ 2. Generate 2048-bit token     │
                                            │ 3. Store in tokens/{hash}.json │
                                            │ 4. Detect multi-device login   │
                                            │ 5. Invalidate old tokens       │
                                            └────────────────────────────────┘
                                                                    │
                                                                    ▼
┌──────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────┐
│  User    │◀───│ Set Cookie   │◀───│  Response with  │◀───│  Backend   │
│  Browser │    │ auth_token   │    │  token + info   │    │  Auth      │
└──────────┘    │ (1h expire)  │    └─────────────────┘    └────────────┘
                └──────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                         API CALL FLOW                                    │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────┐
│  User    │───▶│ API Request  │───▶│  POST           │───▶│  Backend   │
│  Action  │    │ + Cookie     │    │  /api/method    │    │  API       │
└──────────┘    └──────────────┘    └─────────────────┘    └────────────┘
                                                                    │
                                                                    ▼
                                            ┌────────────────────────────────┐
                                            │ 1. Extract token from cookie   │
                                            │ 2. Verify token is valid       │
                                            │ 3. Check expiration < 1h       │
                                            │ 4. Refresh expiration (+1h)    │
                                            │ 5. Update last_activity        │
                                            │ 6. Execute API method          │
                                            └────────────────────────────────┘
                                                                    │
                                                                    ▼
┌──────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────┐
│  User    │◀───│ Refresh      │◀───│  Response +     │◀───│  Backend   │
│  Browser │    │ Cookie       │    │  Refreshed      │    │  API       │
└──────────┘    │ (new 1h)     │    │  Cookie         │    └────────────┘
                └──────────────┘    └─────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MULTI-DEVICE LOGIN FLOW                               │
└─────────────────────────────────────────────────────────────────────────┘

Device A (Already logged in)              Device B (New login)
┌──────────────────┐                      ┌──────────────────┐
│ Active Session   │                      │ User Login       │
│ Valid Token      │                      │ Same Account     │
└──────────────────┘                      └──────────────────┘
         │                                          │
         │                                          ▼
         │                              ┌────────────────────────────┐
         │                              │ Backend detects existing   │
         │                              │ active session for user    │
         │                              └────────────────────────────┘
         │                                          │
         │                                          ▼
         │                              ┌────────────────────────────┐
         │                              │ Invalidate Device A token  │
         │                              │ Kick Device A session      │
         │                              │ Generate new token for B   │
         │                              └────────────────────────────┘
         │                                          │
         ▼                                          ▼
┌──────────────────┐                      ┌──────────────────┐
│ Next API Call    │                      │ Login Success    │
│ Token Invalid    │                      │ New Token        │
└──────────────────┘                      └──────────────────┘
         │                                          │
         ▼                                          ▼
┌──────────────────┐                      ┌──────────────────┐
│ Error Response:  │                      │ Warning Shown:   │
│ logged_out_      │                      │ "已自动登出      │
│ elsewhere: true  │                      │  X个旧设备"      │
└──────────────────┘                      └──────────────────┘
         │
         ▼
┌──────────────────┐
│ Show Alert:      │
│ "账号在其他      │
│  设备登录"       │
│ Auto Redirect    │
└──────────────────┘
```

## Token Storage Structure

```
tokens/
├── {user1_hash}_tokens.json
│   {
│     "session-uuid-1": {
│       "token": "abc123...xyz789",  # 512 chars (2048 bits)
│       "session_id": "session-uuid-1",
│       "created_at": 1698765432.0,
│       "expires_at": 1698769032.0,  # +1 hour
│       "last_activity": 1698765432.0
│     },
│     "session-uuid-2": { ... }
│   }
├── {user2_hash}_tokens.json
│   { ... }
└── {user3_hash}_tokens.json
    { ... }
```

## Cookie Structure

```
Browser Cookies (for each session):

auth_token: "abc123...xyz789"  (512 chars, 2048 bits)
  - httponly: true              # Prevents JavaScript access (XSS protection)
  - max-age: 3600              # 1 hour expiration
  - samesite: Lax              # CSRF protection
  - secure: false              # Set to true in production (HTTPS)

session_id: "session-uuid-abc123"
  - httponly: false            # Frontend needs to read
  - max-age: 3600              # Same as token
  - samesite: Lax
  - secure: false
```

## Error Response Examples

### Token Expired
```json
{
  "success": false,
  "message": "令牌已过期，请重新登录",
  "need_login": true
}
```
**Frontend Action**: Show message → Redirect to login after 2s

### Multi-Device Logout
```json
{
  "success": false,
  "message": "令牌验证失败，可能账号在其他设备登录",
  "need_login": true,
  "logged_out_elsewhere": true
}
```
**Frontend Action**: Show "账号已在其他设备登录，本设备已自动登出" → Redirect

### Token Not Found
```json
{
  "success": false,
  "message": "未找到认证令牌，请重新登录",
  "need_login": true
}
```
**Frontend Action**: Show message → Redirect to login

## Token Lifecycle States

```
┌──────────┐
│ CREATED  │  Token generated at login
└────┬─────┘  - created_at: now
     │        - expires_at: now + 1h
     │
     ▼
┌──────────┐
│ ACTIVE   │  User making API calls
└────┬─────┘  - last_activity: updated
     │        - expires_at: extended +1h each call
     │
     ├───────▶ (User inactive >1h)
     │                │
     │                ▼
     │        ┌──────────┐
     │        │ EXPIRED  │  Automatic expiration
     │        └────┬─────┘  - time > expires_at
     │             │
     │             ▼
     │        ┌──────────┐
     │        │ REJECTED │  Next API call fails
     │        └──────────┘  - Returns 401 + need_login
     │
     ├───────▶ (User logs out)
     │                │
     │                ▼
     │        ┌──────────┐
     │        │INVALIDATED│ Manual logout
     │        └────┬─────┘  - Token deleted from file
     │             │        - Cookie cleared
     │             ▼
     │        ┌──────────┐
     │        │ DELETED  │  Token removed
     │        └──────────┘
     │
     └───────▶ (Multi-device login)
                      │
                      ▼
              ┌──────────┐
              │ KICKED   │  Another device logged in
              └────┬─────┘  - Token invalidated
                   │        - Session cleaned
                   ▼
              ┌──────────┐
              │ DELETED  │  Old token removed
              └──────────┘
```

## Security Checklist

- [x] Tokens are cryptographically random (secrets.token_hex)
- [x] Tokens are 2048-bit (256 bytes)
- [x] Cookies are httponly (XSS protection)
- [x] Cookies have expiration (1 hour)
- [x] Cookies use samesite (CSRF protection)
- [x] Tokens automatically refresh on activity
- [x] Old sessions invalidated on multi-device login
- [x] Expired tokens rejected with clear errors
- [x] Token files stored securely (should be chmod 700 in production)
- [x] Logout properly cleans up tokens and cookies

## Production Deployment Notes

### Required Changes
1. **Enable HTTPS**: Set `secure=True` in cookie settings
2. **File Permissions**: `chmod 700 tokens/` directory
3. **Database Migration**: Consider moving from files to Redis/DB for scale
4. **Rate Limiting**: Add to /auth/login to prevent brute force
5. **Monitoring**: Log token generation/validation failures
6. **Backup**: Include tokens/ in backup strategy (or exclude if using DB)

### Performance Considerations
- File I/O on every API call (consider caching)
- Lock contention with many concurrent users
- Disk space for token storage
- Consider Redis for high-traffic scenarios

### Monitoring Metrics
- Token generation rate
- Token validation failures
- Multi-device login frequency
- Token expiration events
- Average token lifetime
