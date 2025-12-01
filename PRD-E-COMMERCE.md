
# 📦 מסמך אפיון מוצר (PRD) - מערכת E-Commerce מבוססת RabbitMQ

## 🧭 חלק א: תקציר מנהלים

**מטרה:**  
בניית מערכת המדמה תהליך עיבוד הזמנות מקצה לקצה במודל Event-Driven תוך שימוש ב-RabbitMQ וארכיטקטורת Microservices.  
המערכת תאפשר הדמיה של תהליך עיבוד הזמנה - מהקליטה, דרך תשלום ומלאי, ועד למשלוח והתראה ללקוח.

---

## ⚙️ חלק ב: סקירה מערכתית

המערכת תכלול מספר שירותים עצמאיים (microservices) אשר מתקשרים ביניהם באמצעות RabbitMQ.  
כל שירות מטפל בתחום אחר בתהליך, ומעביר אירועים לאחרים דרך תורים (queues).

**תרשים ארכיטקטורה:**  
Frontend (React) → API Gateway (FastAPI) → RabbitMQ → Services (Order, Payment, Inventory, Shipping, Notification)

---

## 🧩 חלק ג: אפיון שירותים מרכזיים

| שירות | תיאור | Endpoints | Events |
|--------|--------|------------|---------|
| **API Gateway** | נקודת כניסה למערכת. מקבל בקשות מה-Frontend ומפרסם order.created. | `POST /orders`, `GET /orders/{id}` | Publish: `order.created` |
| **Order Service** | אחראי על שמירת ההזמנה ב-MongoDB, ומעקב אחרי מצבה. | `GET /orders`, `PUT /orders/{id}/status` | Consume: `order.created`, Publish: `order.updated` |
| **Payment Service** | מדמה חיוב תשלום עבור ההזמנה. | Worker only | Consume: `order.created`, Publish: `payment.succeeded` / `payment.failed` |
| **Inventory Service** | בודק מלאי ומוריד כמות לאחר אישור תשלום. | `GET /inventory` | Consume: `payment.succeeded`, Publish: `inventory.reserved` / `inventory.failed` |
| **Shipping Service** | מבצע תהליך משלוח לאחר שכל התנאים מולאו. | Worker only | Consume: `payment.succeeded`, `inventory.reserved`, Publish: `shipping.completed` |
| **Notification Service** | שולח הודעות על סטטוס ההזמנה ללקוח (מדומה). | N/A | Consume: `payment.failed`, `shipping.completed` |

---

## 📊 תרשים רצף בסיסי (Sequence Diagram)

```
Client → API Gateway → RabbitMQ → Payment Service → Inventory Service → Shipping Service → Notification Service
```

1. הלקוח שולח הזמנה (`POST /orders`)  
2. API יוצר הזמנה ושולח אירוע `order.created`  
3. Payment Service צורך האירוע, מנסה לחייב, ושולח `payment.succeeded`  
4. Inventory Service צורך האירוע, מוריד מלאי ושולח `inventory.reserved`  
5. Shipping Service מקבל את שני האירועים ומתחיל משלוח  
6. Notification Service שולח עדכון סופי ללקוח  

---

## 🧱 חלק ד: דרישות טכניות

**Backend:** Python, FastAPI, aio-pika, MongoDB (motor/beanie), pydantic, pytest  
**Frontend:** React + Vite, Axios  
**Infrastructure:** Docker, RabbitMQ (management plugin), MongoDB  
**Monitoring:** Prometheus + Grafana (אופציונלי)

---

## מבנה תיקיות הפרויקט

```bash
ecommerce/
├── docker-compose.yml
├── infra/
│   ├── grafana/
│   │   ├── dashboards/
│   ├── prometheus.yml
│   └── rabbitmq_definitions.json
├── api/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── services/
│   ├── orders/
│   ├── payment/
│   ├── inventory/
│   ├── shipping/
│   └── notification/
├── workers/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   └── utils/
│   └── Dockerfile
└── README.md
```


## ✅ סיכום

מסמך זה מתאר את האפיון המלא למערכת E-Commerce מבוססת RabbitMQ בארכיטקטורת Microservices.  
ניתן להשתמש בו לצורך פיתוח בפועל או להמשך הרחבה עם רכיבים נוספים כגון Authentication, Tracing ו-Metrics.
