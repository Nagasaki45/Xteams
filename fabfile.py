from fabric.api import run, cd


def docker_compose(cmd):
    run('docker-compose -f docker-compose-prod.yml {}'.format(cmd))


def deploy():
    with cd('~/sites/xteams.nagasaki45.com/'):
        run('git pull')
        docker_compose('build')
        docker_compose('run --rm web python manage.py migrate')
        docker_compose('stop')
        docker_compose('rm web --force')
        docker_compose('up -d')
