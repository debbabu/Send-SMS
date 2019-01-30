# Send SMS

This module use for send sms from odoo. You need a sms gateway to setup for trigger sms. You can use multiple gateway for multiple sms template. Also you can send sms manually using wizard.

You can find send sms functionality under Settings. You will get that menu in debug mode.

Settings > Technical > Send SMS.


SMS Gateway Setup
=================
1. This module support only GET method for integrate sms gateway.
2. For mobile, use {mobile} as a variable and add this variable in url. Some gateway support country code (like 91 for india) or some gateway not support country code. If your gateway support country code use country code before {mobile} (like 91{mobile}) .
3. For message, use {message} as a variable in url.
4. If you want to test after gateway setup, So go to SMS Test tab in form view of gateway setup.

Template Setup
==============
You can choose Gateway, model, put mobile no. as a variable like ${object.mobile}, Write message in body field.

SMS Track
=========
Track History of all message responce. Also that history contain mobile no., message, gateway.

SMS Wizard
===========
You can add sms template to Action as a wizard. Also you can modify message content in wizard, but that one not reflect in orginal template.

SMS Server Action and Automated Action
======================================
You can use SMS Template in Automated Action using Server Action. So that you can trigger SMS automatic as per trigger condition.
