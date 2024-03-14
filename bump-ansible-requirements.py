import click

import requests

from ruamel.yaml import YAML


@click.command()
@click.option('--requirements-file', default='requirements.yml')
def main(requirements_file):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(requirements_file, 'r') as file:
        data = yaml.load(file)

    for (i, collection) in enumerate(data['collections']):
        namespace, name = collection['name'].split('.')
        url = f'https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/index/{ namespace }/{ name }/'
        r = requests.get(url)
        highest_version = r.json()['highest_version']['version']
        data['collections'][i]['version'] = highest_version

    with open(requirements_file, 'w') as file:
        yaml.dump(data, file)


if __name__ == '__main__':
    main()
