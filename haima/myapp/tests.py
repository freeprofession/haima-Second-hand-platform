from django.test import TestCase

import numpy
# Create your tests here.
import re

a = re.compile(r'^\w+$')
b = '31313321'
c = a.match(b)
print(c)
if c is None:
    print(0)
else:
    if len(b) in range(6, 17):
        print(1)
    else:
        print(0)
