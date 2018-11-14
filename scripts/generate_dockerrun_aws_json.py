import json
import os
import argparse
import subprocess


def generate_gunicorn_cmd(log_level='debug'):
    return [
        '/usr/local/bin/gunicorn',
        'config.wsgi:application',
        '-w=2',
        '-b=:8000',
        '--log-level={}'.format(log_level),
        '--log-file=-',
        '--access-logfile=-'
    ]


def load_template(template_file):
    with open(template_file, 'r') as f:
        return json.load(f)


def get_container_indices(template_data):
    """
    Generate mapping between container label and its 0-index in the container definition
    :param template_data: dict representation of Dockerrun.aws.json data
    :return: dict, e.g. dict(web=0, nginx=1)
    """
    return {definition['name']: i for i,definition in enumerate(template_data['containerDefinitions'])}


def generate_dockerrun_config(*, template_file, app_image, nginx_image, debug_level='debug'):
    """
    Assumes containers are named either web, nginx, or worker
    :param template_file: template file location
    :param app_image: app image uri/tag to use
    :param nginx_image: nginx image uri/tag to use
    :param debug_level: debug level for gunicorn logging level
    :return: dict
    """

    config = load_template(template_file)
    containers = get_container_indices(config)

    # specify image/tag version
    config['containerDefinitions'][containers['web']]['image'] = app_image
    config['containerDefinitions'][containers['nginx']]['image'] = nginx_image
    # generate gunicorn, and specify log level
    config['containerDefinitions'][containers['web']]['command'] = generate_gunicorn_cmd(debug_level)
    if 'worker' in containers:
        config['containerDefinitions'][containers['worker']]['image'] = app_image
    return config


def get_head_commit():
    """
    Get current commit hash
    :return:
    """
    return subprocess.run('{}/bin/head_commit'.format(os.environ['EBDOCKER_CONTEXT']).split(), stdout=subprocess.PIPE).stdout.decode('utf-8').strip()


def get_env():
    """
    Populate env variables from values in .env file
    """
    with open('.env') as f:
        os.environ.update(line.strip().split('=', 1) for line in f if line.strip())


def main(filename, template, tag=None):
    """
    Generate a Dockerrun.aws.json for the specified environment (and optionally, tag)
    Placed in
    :param filename: destination of file to write to
    :param tag: (optional) tag to append to image uris
    :return:
    """
    get_env()
    tag = tag or get_head_commit()
    config = generate_dockerrun_config(
            app_image="{}:{}".format(os.environ['APP_IMAGE'], tag),
            nginx_image="{}:{}".format(os.environ['NGINX_IMAGE'], tag),
            template_file=template
    )
    with open(filename, 'w') as outfile:
        json.dump(config, outfile, indent=2)
    print("Generated file {} with tag {}".format(filename, tag))


parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str,
                    help='destination of file to write to, e.g. dockerrun/Dockerrun.aws.engine-prod.json')
parser.add_argument('--tag', type=str, help='(optional) tag to append to image uris')
parser.add_argument('--template', type=str, help="json template file, e.g. dockerrun/Dockerrun.aws.template.json")

args = parser.parse_args()
main(args.filename, args.template, tag=args.tag)
