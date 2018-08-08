# Send SMS

This module use for send sms from odoo. You need a sms gatway to setup for trigger sms. We can use multiple getway in multiple sms template. Also you can send sms mannualy usind wizard.

You can find send sms functionality under Settings. You will get that menu in debug mode.
Settings > Technical > Send SMS.


SMS Getway Setup
=================
1. This module support only GET method for integrate sms getway.
2. For mobile, use {mobile} as a variable and add this variable in url. Some getway support country code (like 91 for india) or some getway not support country code. If your getway support country code use country code before {mobile} (like 91{mobile}) .
3. For message, use {message} as a variable in url.
4. If you want to test after getway setup, So go to SMS Test tab in form view of getway setup.

Template Setup
==============
You can choose Getway, model, put mobile no. as a variable like ${object.mobile}, Write message in body field.

SMS Track
=========
Track History of all message responce. Also that history contain mobile no., message, getway.

SMS Wizard
===========
You can add sms template to Action as a wizard. Also you can modify message content in wizard, but that one not reflect in orginal template.
# Send-SMS
