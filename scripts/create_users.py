from django.contrib.auth.models import User

users = [
    'adent',
    'bbolling',
    'hprynne',
    'mtulliver',
    'ymakioka',
    'ctinajero',
    'jgatz',
    'dbrooks',
    'ebovary',
    'swestern',
    'narcher',
    'mpierce',
    'ctrask',
    'jeyre',
    'jlfinch',
    'scarton',
    'mwormwood',
    'earroway',
    'dschwartz',
    'jbrown'
]

for username in users:
    user=User.objects.create_user(username, password='1234')
    user.is_superuser=False
    user.is_staff=False
    user.save()
