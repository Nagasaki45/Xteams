from fabric.api import run, cd, env, local

env.hosts = ['nagasaki45@nagasaki45.com']
env.deploy_dir = '/home/nagasaki45/sites/xteams.nagasaki45.com/'


def _docker_compose(cmd, execute_using):
    execute_using('docker-compose -f docker-compose-prod.yml {}'.format(cmd))


def _build_and_run_app(locally=False):
    execute_using = local if locally else run
    _docker_compose('build', execute_using)
    _docker_compose('run --rm web python manage.py migrate', execute_using)
    _docker_compose('up -d', execute_using)


def deploy():
    with cd(env.deploy_dir):
        run('git pull')
        _build_and_run_app()


def stage():
    _build_and_run_app(locally=True)
