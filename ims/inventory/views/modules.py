import logging
import re
from collections import defaultdict
from datetime import datetime

import pytz
from django.contrib import messages
from django.contrib.auth.models import Group, User, auth
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models
from django.db.models import Q
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# use below given imports, in case to use the ifm ldap server
from ims.settings import base
from ims.settings.base import InventoryManagementSystem_version
from inventory.decorators import *
from inventory.forms import *
from inventory.helpers import *
from inventory.models import *
from inventory.user_login import check_credentials
