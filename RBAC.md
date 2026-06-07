# 🔐 מערכת הרשאות (RBAC)  TON Israel
## תפקידים
- **super_admin**: מנהל-על (אתה). יכול להוסיף/להסיר מנהלים, לראות הכל.
- **admin**: מנהל. יכול להשתמש ב-/export, /admin, /debug.
- **moderator**: מנחה (בעתיד).
- **user**: משתמש רגיל.

## איך זה עובד
1. **super_admin** מוסיף מנהל דרך:
   `/addadmin <telegram_id> <role> <password>`
   → הבוט שולח הודעה למשתמש עם הסיסמה.
2. **המנהל** יכול להתחבר דרך:
   `/login <password>` (או `/admin` + סיסמה).
3. **שינוי סיסמה**:
   `/setpassword <old> <new>`  המנהל מחליף סיסמה.
4. **הסרת מנהל**:
   `/removeadmin <telegram_id>`  super_admin בלבד.

## אבטחה
- סיסמאות נשמרות כ-hash (bcrypt)  אי אפשר לשחזר.
- רק super_admin יכול לראות רשימת מנהלים (ללא סיסמאות).
