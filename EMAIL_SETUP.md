# How to Configure Email for Production

To send real emails (OTPs) to users when deployed, you need to configure an SMTP server.

## 1. Get SMTP Credentials

### Option A: Gmail (Easiest)
1.  Go to your Google Account > Security.
2.  Enable **2-Step Verification**.
3.  Search for **App Passwords**.
4.  Create a new app password named "ScamBank".
5.  Copy the 16-character password.

### Option B: SendGrid / Mailgun (Professional)
1.  Sign up for SendGrid or Mailgun.
2.  Get your API Key and SMTP Host details.

## 2. Set Environment Variables on Render

When deploying on Render (or any cloud provider), adding passwords directly to code is insecure. Instead, use **Environment Variables**.

1.  Go to your Render Dashboard > Select your Service.
2.  Click **Environment** > **Add Environment Variable**.
3.  Add the following keys and values:

| Key | Value |
| :--- | :--- |
| `EMAIL_HOST_USER` | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | `your-16-char-app-password` |

## 3. That's it!
Your app will automatically read these values and start sending real emails.
