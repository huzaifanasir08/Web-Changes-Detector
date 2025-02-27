# Web Change Detector 🔍

## Overview

Web Change Detector is a Django-based tool that **monitors websites for content changes**. It uses asynchronous web crawling, hashes the HTML content, and compares it to detect modifications over time. This is useful for **tracking updates, detecting unauthorized changes, and monitoring competitors' websites.**

## Features

✅ **Asynchronous Web Crawling** using `crawl4ai`\
✅ **Content Hashing** for accurate change detection\
✅ **Automated Website Monitoring**\
✅ **Email Notifications** for detected changes\
✅ **Django ORM Integration** for database storage\
✅ **Logging and Status Tracking**

## How It Works

1. **Fetch Website List**: Retrieves URLs from the database.
2. **Generate Hash**: Computes a hash for each webpage's content.
3. **Compare Hashes**: Checks for changes between old and new content.
4. **Trigger Alerts**: Sends email notifications if changes are found.
5. **Store Results**: Saves check history in the database for review.

## Installation

### **1. Clone the Repository**

```bash
git clone https://github.com/huzaifanasir08/Web-Changes-Detector.git  
cd Web-Changes-Detector  
```

### **2. Create a Virtual Environment (Recommended)**

```bash
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt  
```

### **4. Set Up the Database**

```bash
python manage.py migrate  
```

### **5. Run the Django Development Server**

```bash
python manage.py runserver  
```

## Configuration

### **Database Settings**

Update `DATABASES` in `settings.py` if you're using PostgreSQL, MySQL, or another database.

### **Email Notifications**

To enable email alerts for detected changes, configure your email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
EMAIL_HOST = 'smtp.example.com'  
EMAIL_PORT = 587  
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = 'your_email@example.com'  
EMAIL_HOST_PASSWORD = 'your_password'  
```

Replace with your **SMTP provider details** (Gmail, AWS SES, SendGrid, etc.).

## Running the Web Change Detector

### **1. Start the Check Process**

Inside Django’s shell (`python manage.py shell`), you can manually run the detector:

```python
from detector_app.views import check_start  
check_start()  
```

Or automate it using **Celery** or **a cron job**.

## Technologies Used

- **Django** – Web framework
- **AsyncWebCrawler (crawl4ai)** – Asynchronous web crawling
- **Requests** – HTTP requests
- **Hashlib** – Content hashing
- **Celery** (optional) – Background task handling
- **PostgreSQL/MySQL** (optional) – Database support

## Future Enhancements 🚀

🔹 **Web-based Dashboard** for monitoring results\
🔹 **Slack/Telegram Notifications**\
🔹 **Multi-threaded Crawling** for better performance\
🔹 **Customizable Check Intervals**

## Contribution Guidelines

Contributions are welcome! To contribute:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature-branch`)
3. **Commit your changes** (`git commit -m "New feature added"`)
4. **Push to GitHub** (`git push origin feature-branch`)
5. **Create a Pull Request**

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details. is licensed under the **MIT License**.

---

**🔗 GitHub Repo:** [Web Change Detector](https://github.com/huzaifanasir08/Web-Changes-Detector)


