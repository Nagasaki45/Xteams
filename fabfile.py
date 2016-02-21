from fabric.api import run, cd, env

env.hosts = ['nagasaki45@nagasaki45.com']
env.deploy_dir = '/home/nagasaki45/sites/xteams.nagasaki45.com/'


def docker_compose(cmd):
    run('docker-compose -f docker-compose-prod.yml {}'.format(cmd))


def deploy():
    with cd(env.deploy_dir):
        run('git pull')
        docker_compose('build')
        docker_compose('run --rm web python manage.py migrate')
        docker_compose('stop')
        docker_compose('rm --force web')
        docker_compose('up -d')
