# 🛒 E-Commerce Event-Driven System (RabbitMQ + FastAPI + MongoDB + React)

## 🎯 מטרת הפרויקט
מערכת מיקרו־סרוויסים המדמה חנות אונליין,
כאשר כל פעולה (הזמנה, תשלום, משלוח וכו’) מתבצעת בצורה **אסינכרונית** דרך **RabbitMQ**.

---

## 🧱 שלב 1 – הגדרת תשתית בסיסית
**מטרה:** להרים סביבה מלאה ב־Docker Compose

- [ ] הגדרת מבנה תיקיות
- [ ] יצירת קובץ `.gitignore`
- [ ] כתיבת `docker-compose.yml`
- [ ] קובץ `rabbitmq_definitions.json` בסיסי
- [ ] קובץ `prometheus.yml`
- [ ] בדיקת ריצה ראשונית של כל הקונטיינרים

---

## 🐇 שלב 2 – RabbitMQ Configuration
**מטרה:** להבין לעומק Exchanges, Queues ו־Routing

- [ ] הסבר + תרשים על RabbitMQ (Direct, Fanout, Topic)
- [ ] יצירת קובץ הגדרות לתורים (`infra/rabbitmq_definitions.json`)
- [ ] הגדרת Dead Letter Queue (DLQ)
- [ ] חיבור בסיסי בין Producer ל־Consumer לדוגמה
- [ ] בדיקה בלוח הבקרה של RabbitMQ (http://localhost:15672)

---

## ⚙️ שלב 3 – Backend Architecture
**מטרה:** בניית השירותים עצמם (FastAPI + Workers)

- [ ] יצירת שירות `api-gateway` ב־FastAPI
- [ ] שירות `order-service` (שליחת הודעה ל־RabbitMQ)
- [ ] שירות `payment-service` (צרכן שקורא הודעות ומעדכן DB)
- [ ] שירות `notification-service` (שולח מייל/הודעה על אישור הזמנה)
- [ ] חיבור למונגו (שמירת סטטוס הזמנה, לקוח, סכום וכו’)

---

## 🍃 שלב 4 – MongoDB Integration
**מטרה:** חיבור למסד נתונים + ORM קל

- [ ] החלטה על מבנה הקולקציות (orders, users, payments)
- [ ] חיבור ל־MongoDB דרך Motor או PyMongo
- [ ] כתיבת פונקציות CRUD בסיסיות
- [ ] בדיקה מקומית של שמירה ושליפה

---

## 🧭 שלב 5 – Frontend (React)
**מטרה:** דשבורד פשוט לניהול ההזמנות

- [ ] תצוגה של הזמנות קיימות (GET /orders)
- [ ] טופס ליצירת הזמנה חדשה (POST /orders)
- [ ] עדכון סטטוס בזמן אמת באמצעות polling או websocket
- [ ] עיצוב בסיסי עם Tailwind CSS

---

## 📈 שלב 6 – Monitoring & Metrics
**מטרה:** להבין מה קורה במערכת שלך

- [ ] הגדרת Prometheus ל־RabbitMQ ו־API
- [ ] הוספת Grafana Dashboard
- [ ] מדדים: תורים, הודעות מעובדות, זמן תגובה

---

## 🚀 שלב 7 – שיפורים ו-Advanced Features
**מטרה:** לשלב קונספטים מתקדמים של RabbitMQ

- [ ] Priority Queues (עדיפות לאירועים חשובים)
- [ ] Delayed Messages (הודעות עם השהיה)
- [ ] Retry Strategy + Dead Letter Queue
- [ ] Fanout Exchange לשליחת אירועים למספר שירותים

---

## 📦 שלב 8 – Deployment
**מטרה:** הכנה ל־Production

- [ ] Docker Compose Production Mode
- [ ] שימוש ב־.env מאובטח
- [ ] תיעוד מלא ב־README

---

## 💡 שלבים אופציונליים בהמשך
- אינטגרציה עם Kafka להשוואה בין RabbitMQ ↔ Kafka
- מעבר ל־Kubernetes
- חיבור ל־CI/CD (GitHub Actions)

---

🧭 **עקרון עבודה:**  
בכל שלב נבין לעומק את התיאוריה → ניישם אותה בקוד → נבדוק בפועל → נמשיך הלאה.

