  #!/bin/bash
  set -e
  LOGFILE=/var/www/logs/gunicorn/access.log
  LOGDIR=$(dirname $LOGFILE)
  NUM_WORKERS=3
  # user/group to run as
  USER=ubuntu
  GROUP=ubuntu
  cd "/var/www/ufadhili"
  source /var/www/ufadhili/pombola-virtualenv/bin activate
  
  test -d $LOGDIR || mkdir -p $LOGDIR
  exec /usr/local/bin/gunicorn_django pombola.wsgi:application \
     -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE

    

   