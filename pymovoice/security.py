USERS = {'editor': 'editor',
         'viewer': 'viewer'}
GROUPS = {'editor': ['group:editors'],
          'viewer': ['group:viewer']}


def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])